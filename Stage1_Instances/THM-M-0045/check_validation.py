#!/usr/bin/env python3
"""Fail-closed narrow validator for S56-M-0045-VALIDATION."""

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
HERE = ROOT / "Stage1_Instances" / "THM-M-0045"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM = "S56-M-0045-VALIDATION"
THEOREM = "THM-M-0045"
BASE_REVISION = "eb9c2192f79a480deff66d2c0f8e31032bcc2d9f"
BASE_TREE = "57b76c2fceacd8819b0ec8b9abcd42cfcc74b8e2"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
EXPECTED_INPUTS = {
    "Statement.lean": "1964c3edcb6c802bf15183733e98dbfa947d0d20ee125e29b687cf13cd2531f5",
    "ObligationTree.lean": "6d410104478d6466fae6d0924685c266722bcb0742f27443baeebe47afdc7f3a",
    "SchurPort.lean": "808342069df1e424bcc157c2245317458f63cb9d47ed402324c07021a474f09d",
    "Proof.lean": "62cca2b905895d9c2ac3763e0178ec4cc3ff745be7110a200a6cf1bce507248f",
    "proof-receipt.json": "faa5b54a33cd939df8f9f49956a453bdf05137120fb3973271c3b15e4fac01a7",
    "obligation-registry.json": "d38d6028caf7d3f52ced9655c1623526ff19477f179962de7edc7135635b8478",
    "typed-graphs.json": "c69409550f84e55a959e314d688744925468ba6d74e4f06d3f2b51beb2c0a244",
    "validation-specs.json": "b858f62394f0f13795527ff317547e8b19fb0b8bb93b69b60b86d972411f8b5d",
    "anchor-audit.json": "beaebc82bf469cf1f2d35179ba4b537dbdc64655f9a1c5bb19c6ef18344f12e1",
    "Validation.lean": "60bf15edfb5c6d4a5b8848a36ba0fea8449787baa72131ed3cd4e37354d80e00",
}
EXPECTED_TOOL_INPUTS = {
    "lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
SOURCE_BOUNDARY = {
    "Mathlib/Data/Complex/Basic.lean": (
        "b26f6e653e122ea18e2dc1f790e46f6e3218b23bacd5d6b441324f11277c978b",
        "885095e16814e6cc314a4db8c9490cc654c95e892571b112dc0b9ac9d22da229",
    ),
    "Mathlib/Analysis/InnerProductSpace/Adjoint.lean": (
        "08218f9c59623e93818c293000810a2d15a9b543340feaba3b1a58b4749831a6",
        "3be11d32be2df343d8845b0eabe6d0dbe553509b68cfd15b31bf75525f97bf29",
    ),
    "Mathlib/Analysis/Complex/Polynomial/Basic.lean": (
        "f6159d7625ca323846088b04ae89fca501bb040fcdce982f8f24c453e587d491",
        "340d8729a9064d04fb7a67a0871bd5a13a9e68175cfcc0ed651d0c1c3540e8aa",
    ),
    "Mathlib/LinearAlgebra/Eigenspace/Triangularizable.lean": (
        "c441e191010aedfb7bbc7e65bcfafa9ec7da27474f96d29a3f1550613cc03c0d",
        "d796cd31ec604995701ad7d31c1abc808ffbf3dc2fe6b323e8e0962bd1f1ea8c",
    ),
    "Mathlib/LinearAlgebra/Matrix/Block.lean": (
        "bdbdc046f6f10fdd634028259bbaae5dce9da670d8b95e37950f0a39390e3762",
        "69f3ee660fdb31878cf5a80cdcfdc4180949f503e65102d742a9c670d51caf1b",
    ),
    "Mathlib/LinearAlgebra/UnitaryGroup.lean": (
        "0136abe584007ffe1b9e9b0016b792ed92bc2de36fa710e87af9cb87d0808f93",
        "2f02f7cedf8b9e2fe6513cd585655f566eef466f48818e165874ad8626539313",
    ),
}
HISTORICAL_REVISION = "0a539f0ce764fd16726509b62ed7b870461070eb"
HISTORICAL_PATH = "Mathlib/LinearAlgebra/Matrix/SchurTriangulation.lean"
HISTORICAL_SHA256 = "8fc4d47249d8bcc75c02fedc6d9b0008f7c0127c501f608d4226a7f5872f4bc3"
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
        rf"'[^'\n]*{re.escape(declaration)}' depends on axioms:\s*\[([^]]+)]",
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
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    manifest = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    instance = load(HERE / "instance.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    proof_receipt = load(HERE / "proof-receipt.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    target = next(row for row in manifest["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 1085 and target["baseline"] == "L0"
    assert target["rework_required"] is True and target["theorem_complete"] is False
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item["theorem_id"] == THEOREM and item["execution_rank"] == 1085
    assert item["phase"] == "validation" and item["layer"] == 5
    assert item["state"] == "[ ]" and item["attempts"] == 0
    assert item["depends_on"] == ["S56-M-0045-PROOF"]
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM}"]
    predecessor = next(
        row for row in execution["items"] if row["id"] == "S56-M-0045-PROOF"
    )
    assert predecessor["state"] == "[_]"

    assert instance["root_vector"] == {"H": "H1", "M": "M3", "R": "R4"}
    assert instance["accepted_proof_state"] == []
    assert instance["accepted_receipt_ids"] == []
    assert instance["audit_complete"] is instance["theorem_complete"] is False
    closure = graphs["closure_boundary"]
    assert closure["closed_obligations"] == [] and closure["root_closed"] is False
    assert closure["accepted_root_machine_debt"] == "M3"
    assert closure["remaining_root_cut_set"] == ["M0045-T-PACKAGE"]
    assert closure["audit_complete"] is closure["theorem_complete"] is False
    assert registry["denominator_sha256"] == (
        "47fc5062b82b1a06eb2ca0ce6379dc5ea7f6ec15481a1144fe24f11724baad1a"
    )
    assert proof_receipt["result"]["root_kernel_closed"] is True
    assert proof_receipt["accepted"] is False
    assert proof_receipt["accepted_closed_obligation_ids"] == []

    for name, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == expected, name
    for name, expected in EXPECTED_TOOL_INPUTS.items():
        assert sha256(LEAN_ROOT / name) == expected, name

    prohibited = re.compile(
        r"\b(sorry|admit|sorryAx|implemented_by|native_decide|extern|opaque)\b|"
        r"^[ \t]*(axiom|constant|unsafe)[ \t]+",
        re.MULTILINE,
    )
    for name in ("Statement.lean", "ObligationTree.lean", "SchurPort.lean", "Proof.lean", "Validation.lean"):
        source = code_without_comments((HERE / name).read_text(encoding="utf-8"))
        assert prohibited.search(source) is None, name
    validation_source = code_without_comments(
        (HERE / "Validation.lean").read_text(encoding="utf-8")
    )
    assert "import Proof" not in validation_source
    assert "import ObligationTree" not in validation_source
    assert "differentialSchurTriangularization" in validation_source

    assert MATHLIB.is_dir(), "pinned mathlib artifacts are unavailable"
    assert git("rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert git("status", "--porcelain=v1", cwd=MATHLIB) == ""
    assert git("remote", "get-url", "origin", cwd=MATHLIB) == (
        "https://github.com/leanprover-community/mathlib4.git"
    )
    assert sha256(MATHLIB / "LICENSE") == (
        "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1"
    )
    for source_name, (source_hash, olean_hash) in SOURCE_BOUNDARY.items():
        assert sha256(MATHLIB / source_name) == source_hash, source_name
        olean_name = source_name.removesuffix(".lean") + ".olean"
        olean = MATHLIB / ".lake" / "build" / "lib" / "lean" / olean_name
        assert sha256(olean) == olean_hash, olean_name
    historical = subprocess.check_output(
        ["git", "show", f"{HISTORICAL_REVISION}:{HISTORICAL_PATH}"], cwd=MATHLIB
    )
    assert hashlib.sha256(historical).hexdigest() == HISTORICAL_SHA256

    lean = run(["lake", "env", "which", "lean"], cwd=LEAN_ROOT).strip()
    lake = run(["lake", "env", "which", "lake"], cwd=LEAN_ROOT).strip()
    lean_path = run(["lake", "env", "printenv", "LEAN_PATH"], cwd=LEAN_ROOT).strip()
    assert LEAN_COMMIT in run([lean, "--version"])
    assert "5.0.0-src+98dc76e" in run([lake, "--version"])
    assert sha256(Path(lean)) == (
        "3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf"
    )
    assert sha256(Path(lake)) == (
        "a608ff084d7e2af228b92a29d7c2fd083ba0580e46889175ec74a81678c98359"
    )

    with tempfile.TemporaryDirectory(prefix="m0045-validation-") as tmp_name:
        tmp = Path(tmp_name)
        for name in ("Statement.lean", "ObligationTree.lean", "SchurPort.lean", "Proof.lean", "Validation.lean"):
            (tmp / name).write_bytes((HERE / name).read_bytes())
        base_env = {
            "HOME": os.environ.get("HOME", ""),
            "PATH": os.environ.get("PATH", ""),
            "LANG": "C.UTF-8",
            "LC_ALL": "C.UTF-8",
            "TZ": "UTC",
            "LEAN_PATH": lean_path,
        }
        run([lean, "-o", "Statement.olean", "Statement.lean"], cwd=tmp, env=base_env)
        local_env = dict(base_env)
        local_env["LEAN_PATH"] = f"{tmp}:{lean_path}"
        obligation_output = run(
            [lean, "-o", "ObligationTree.olean", "ObligationTree.lean"],
            cwd=tmp,
            env=local_env,
        )
        run(
            [lean, "-o", "SchurPort.olean", "SchurPort.lean"],
            cwd=tmp,
            env=local_env,
        )
        proof_output = run([lean, "Proof.lean"], cwd=tmp, env=local_env)
        validation_output = run([lean, "Validation.lean"], cwd=tmp, env=local_env)

    for declaration in (
        "equationWitness_implies_targetAt",
        "root_of_equationPackage",
    ):
        assert_axioms(obligation_output, declaration)
    for declaration in (
        "schurEquationPackage",
        "schurTriangularization",
    ):
        assert_axioms(proof_output, declaration)
    for declaration in (
        "Matrix.schur_triangulation",
        "differentialSchurTriangularization",
    ):
        assert_axioms(validation_output, declaration)
    assert proof_output.count("Declarations are sorry-free!") == 2
    assert validation_output.count("Declarations are sorry-free!") == 2
    assert "sorryAx" not in obligation_output + proof_output + validation_output

    assert spec["schema_version"] == "stage1-validation-recipe/1.0"
    assert spec["item_id"] == ITEM and spec["theorem_id"] == THEOREM
    assert spec["argv"] == ["python3", "-B", f"Stage1_Instances/{THEOREM}/check_validation.py"]
    assert spec["expected_exit"] == 0 and spec["network_policy"] == "denied"
    assert set(spec["covered_obligation_ids"]) == set(proof_receipt["closed_obligation_ids"])

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["release_grade"] is False
    for name, expected in EXPECTED_INPUTS.items():
        assert receipt["inputs"][name] == expected, name
    assert receipt["inputs"]["validation-spec.json"] == sha256(HERE / "validation-spec.json")
    assert receipt["inputs"]["check_validation.py"] == sha256(HERE / "check_validation.py")
    assert receipt["environment"]["platform"] == f"{platform.system()} {platform.machine()}"
    assert receipt["environment"]["lean_executable_sha256"] == sha256(Path(lean))
    assert receipt["environment"]["lake_executable_sha256"] == sha256(Path(lake))
    assert receipt["environment"]["mathlib_revision"] == MATHLIB_REVISION
    assert receipt["environment"]["mathlib_tree"] == MATHLIB_TREE
    assert receipt["result"]["provisional_exact_root_kernel_closed"] is True
    assert receipt["result"]["accepted_root_kernel_closed"] is False
    assert receipt["result"]["accepted_closed_obligation_ids"] == []
    assert receipt["result"]["hermetic_release_gate"] == "fail_closed"
    assert receipt["result"]["independent_distinct_runner_gate"] == "fail_closed"
    assert receipt["result"]["audit_complete"] is receipt["result"]["theorem_complete"] is False
    assert receipt["first_failed_gate"] == "dependency.S56-M-0045-PROOF.master_acceptance"
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
        line[3:] for line in status.splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual_changed == CHANGED_PATHS, (actual_changed, CHANGED_PATHS)
    for relative in CHANGED_PATHS:
        assert_text_hygiene(ROOT / relative)

    print("PASS THM-M-0045 narrow validation")
    print("PASS kernel replay: exact proof, frozen composition, and alternate exact-root adapter elaborated")
    print("PASS trust observation: checked declarations report only propext, Classical.choice, and Quot.sound")
    print("PASS local provenance: frozen hashes, direct source/olean boundary, historical lineage, clean pin, remote, and license agree")
    print("PASS hygiene: Lean assert_no_sorry plus a supplemental prohibited-construct scan passed")
    print("FAIL CLOSED authority: proof/master reconciliation is pending; accepted root remains H1/M3/R4")
    print("FAIL CLOSED hermetic release: shared warm .lake is not an empty-cache offline replay or complete TCB/SBOM archive")
    print("FAIL CLOSED independent release: alternate adapter shares the proof body, worker, and cache; no distinct signed runner")
    print("audit_complete=false; theorem_complete=false")


if __name__ == "__main__":
    main()
