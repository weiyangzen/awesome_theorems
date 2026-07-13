#!/usr/bin/env python3
"""Fail-closed narrow validator for S56-M-0061-VALIDATION."""

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
HERE = ROOT / "Stage1_Instances" / "THM-M-0061"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM = "S56-M-0061-VALIDATION"
THEOREM = "THM-M-0061"
BASE_REVISION = "250f9e73cbbb3ebd2da9d0cefff78f0ab8c0d056"
BASE_TREE = "b6e8138c58e31e82f8209cb70fbc0fb253f3654a"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_REMOTE = "https://github.com/leanprover-community/mathlib4.git"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
EXPRESSION_SHA256 = "adff72e9052ea17e3b6e4349c23028f35f4b8e3c610ea5f9f3b4fc02fe136836"
DENOMINATOR_SHA256 = "2d426a22d370fa53b308df9aa74a4cbaa69b1b30864da4ec30e1c8c31ba330d7"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
EXPECTED_AXIOM_LIST = ["propext", "Classical.choice", "Quot.sound"]
EXPECTED_INPUTS = {
    "Statement.lean": "386d2d25cc7fe5f55f26438e1bc749eb5953e251b48591d3e47247b733bfdc7d",
    "ObligationTree.lean": "0a603a22ffdc4b54147b085b680a4de025e185fe740da7a1eda4ebf537c7885b",
    "Proof.lean": "d9843be41f6ddb7c6cf335a1e242fb0444d37e478f7f7d5b9cb488e86f50fe94",
    "Validation.lean": "f0715d0a281586aaa3436c22cc66ba104afa5a0554d80c6f5241056550e0699a",
    "proof-receipt.json": "0719b7584fef820bf61e2eedbf31635c60dde58182f39f16727ebaed02bd48c0",
    "statement.json": "b27ab2139df6f5a8dd45ad146c70438c93372e0039796466b34be5957c10f25b",
    "obligation-registry.json": "9eb5592fa68b33d6dbb9003607a34c13236f9f78dbb8ea9a0d3df7ff47195451",
    "typed-graphs.json": "ed8113cfc8540530a5f6743ca8a340fe116597f42a362101f7e4ecbf81d162a3",
    "validation-specs.json": "093ed99e12e3f41fb3e3c1e5b3311c58987bb9751134890b7d4d6eb0d5e9559f",
    "anchor-audit.json": "0c7a435881d484fd898b34c86c8c6cb2e19ed31ccc91038133680f67e1e99e6c",
}
EXPECTED_TOOL_INPUTS = {
    "lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
SOURCE_BOUNDARY = {
    "Mathlib/Algebra/Group/Subgroup/Finite.lean": (
        "a7c019909ae433f7aeb0ac605e7e442282f90163",
        "f6b8c03be67cd42c56ed60499ff8f4c86af20caa4ea2e3eb3f7663535a9f4ac5",
        "2bc75463e7ca3dfb3da662325ec257e03e02c6abada36ad211765397062eb153",
    ),
    "Mathlib/GroupTheory/Coset/Card.lean": (
        "4419736cb7b1155a4080699f1f47e8f1fae09dc2",
        "cb3efb11057211d161637ba7e6c75d64271faa95e5bdafff96f82168329b236e",
        "496e9fa216229dc7198442344d8ee1e76a96d80268c3b55b2a068b6d2147f315",
    ),
    "Mathlib/GroupTheory/Coset/Basic.lean": (
        "d2bdff6aca9c86ce95d2f7eca2dc284ef4ff6172",
        "82a0bd5bdb5d5d0ee0f3378efbcd38109926384399473c97e202e6f40239d8e6",
        "a176a626305ad783ea81906dfeac9f17ee4004d4e5cb37a9197f484dca818779",
    ),
    "Mathlib/SetTheory/Cardinal/Finite.lean": (
        "a5a8ff161386385b22e445cc4c9444b4e98a54bc",
        "8de62ef138473b4c4b77917aa453f67b8e203cfb1d2e2c6cb6ebbabf62a9356f",
        "522d9805643fa6818be576c9d0ae1df0694d9a87db1de943a5d99a7e73a6bace",
    ),
}
PROOF_IDS = [
    "M0061-ROOT",
    "M0061-S-INTERFACE",
    "M0061-S-BOUNDARY",
    "M0061-S-FINTYPE-TRANSPORT",
    "M0061-T-FINITE-SCOPE",
    "M0061-A-LAGRANGE",
    "M0061-L-CARD-PRODUCT",
    "M0061-L-NATCARD-PROD",
    "M0061-L-NATCARD-CONGR",
    "M0061-C-COSET-PRODUCT-EQUIV",
    "M0061-C-FIBER-DECOMPOSITION",
    "M0061-T-FIBER-TO-COSET",
    "M0061-C-LEFT-COSET-EQUIV",
    "M0061-T-SIGMA-PRODUCT",
]
PROOF_DECLARATIONS = (
    "fiberDecomposition",
    "fiberToLeftCoset",
    "leftCosetEquivalence",
    "sigmaProductEquivalence",
    "cosetProductEquivalence",
    "natCardProduct",
    "natCardCongruence",
    "cardProductIdentity",
    "pinnedCardProductIdentity",
    "arbitraryGroupDivisibility",
    "pinnedArbitraryGroupDivisibility",
    "finiteGroupDivisibility",
    "lagrangeDivisibility",
    "lagrangeDivisibility_mathlib",
)
COMPOSITION_DECLARATIONS = (
    "cosetProduct_of_fiber_engines",
    "cardProduct_of_engines",
    "divisibility_of_cardProduct",
    "finiteScope_of_arbitraryGroup",
    "root_of_finiteScope",
)
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/Validation.lean",
    f"Stage1_Instances/{THEOREM}/check_validation.py",
    f"Stage1_Instances/{THEOREM}/validation-phase.md",
    f"Stage1_Instances/{THEOREM}/validation-receipt.json",
    f"Stage1_Instances/{THEOREM}/validation-spec.json",
}
SUMMARY_LINES = (
    "PASS THM-M-0061 narrow validation",
    "PASS kernel replay: exact statement, all proof declarations, frozen compositions, two proof roots, and alternate exact-root adapter elaborated",
    "PASS trust observation: checked declarations depend only on propext, Classical.choice, and Quot.sound",
    "PASS selected provenance: frozen hashes, four source/blob/olean boundaries, clean mathlib pin, remote, license, and tool identities agree",
    "PASS hygiene: Lean assert_no_sorry plus a supplemental prohibited-construct scan passed",
    "FAIL CLOSED authority: proof master acceptance and structured state reconciliation are pending; accepted root remains H1/M3/R4",
    "FAIL CLOSED trust: no accepted theorem-specific foundation policy or complete transitive declaration/TCB/SBOM closure exists",
    "FAIL CLOSED hermetic/independent: shared warm .lake and same-worker adapter are neither cold offline replay nor distinct signed verification",
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


def run(argv: list[str], *, cwd: Path = ROOT, env: dict[str, str] | None = None) -> str:
    remaining = RECIPE_TIMEOUT_SECONDS - (time.monotonic() - VALIDATION_STARTED)
    if remaining <= 0:
        raise TimeoutError("validation recipe exceeded its 180-second wall-clock bound")
    result = subprocess.run(
        argv,
        cwd=cwd,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=remaining,
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


def printed_axioms(output: str, declaration: str) -> set[str]:
    pattern = re.compile(
        rf"'[^'\n]*{re.escape(declaration)}' depends on axioms:\s*\[([^]]+)]",
        re.DOTALL,
    )
    match = pattern.search(output)
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
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    manifest = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    instance = load(HERE / "instance.json")
    local_dag = load(HERE / "task-dag.json")
    statement = load(HERE / "statement.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    proof_receipt = load(HERE / "proof-receipt.json")
    frozen_specs = load(HERE / "validation-specs.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    target = next(row for row in manifest["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 1093 and target["baseline"] == "L0"
    assert target["lifecycle_mode"] == "planned"
    assert target["rework_required"] is True and target["theorem_complete"] is False
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 1093,
        "phase": "validation",
        "layer": 5,
        "state": "[ ]",
        "depends_on": ["S56-M-0061-PROOF"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Run hermetic kernel, trust, provenance, and independent validation gates.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    predecessor = next(
        row for row in execution["items"] if row["id"] == "S56-M-0061-PROOF"
    )
    assert predecessor["state"] == "[_]"
    local_task = next(row for row in local_dag["tasks"] if row["id"] == ITEM)
    assert local_task["state"] == "open"
    assert local_task["depends_on"] == ["S56-M-0061-PROOF"]

    assert instance["root_vector"] == {"H": "H1", "M": "M3", "R": "R4"}
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == []
    assert instance["audit_complete"] is instance["theorem_complete"] is False
    closure = graphs["closure_boundary"]
    assert closure["accepted_closed_obligations"] == []
    assert closure["root_closed"] is False and closure["root_machine_debt"] == "M3"
    assert closure["audit_complete"] is closure["theorem_complete"] is False

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
    assert proof_receipt["canonical_target_expression_sha256"] == EXPRESSION_SHA256
    assert proof_receipt["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert proof_receipt["proof_body"]["source_sha256"] == EXPECTED_INPUTS["Proof.lean"]
    assert proof_receipt["closed_obligation_ids"] == PROOF_IDS
    assert proof_receipt["accepted_closed_obligation_ids"] == []
    assert proof_receipt["result"]["root_kernel_closed"] is True
    assert proof_receipt["result"]["accepted_root_closed"] is False
    assert proof_receipt["result"]["axioms"] == EXPECTED_AXIOM_LIST
    assert proof_receipt["accepted"] is False

    assert frozen_specs["item_id"] == "S56-M-0061-OBLIGATION_TREE"
    assert all(row["argv"][-1].endswith("check_obligation_tree.py") for row in frozen_specs["recipes"])
    assert all(row["covered_obligation_ids"] == [] for row in frozen_specs["recipes"])
    assert all("no M0 or proof-closure credit" in row["coverage_boundary"] for row in frozen_specs["recipes"])

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
    for forbidden in ("import Proof", "import ObligationTree", "Proof.", "lagrangeDivisibility_mathlib"):
        assert forbidden not in differential, forbidden
    assert "Subgroup.card_subgroup_dvd_card H" in differential
    assert "assert_no_sorry independentlyReconstructedTarget" in differential

    manifest_record = load(LEAN_ROOT / "lake-manifest.json")
    mathlib_entry = next(row for row in manifest_record["packages"] if row["name"] == "mathlib")
    assert mathlib_entry["rev"] == mathlib_entry["inputRev"] == MATHLIB_REVISION
    assert MATHLIB.is_dir(), "pinned mathlib artifacts are unavailable"
    assert git("rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert git("status", "--porcelain=v1", cwd=MATHLIB) == ""
    assert git("remote", "get-url", "origin", cwd=MATHLIB) == MATHLIB_REMOTE
    assert sha256(MATHLIB / "LICENSE") == (
        "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1"
    )
    for source_name, (blob_hash, source_hash, olean_hash) in SOURCE_BOUNDARY.items():
        assert git("rev-parse", f"HEAD:{source_name}", cwd=MATHLIB) == blob_hash
        assert sha256(MATHLIB / source_name) == source_hash, source_name
        olean_name = source_name.removesuffix(".lean") + ".olean"
        olean = MATHLIB / ".lake" / "build" / "lib" / "lean" / olean_name
        assert sha256(olean) == olean_hash

    lean = run(["lake", "env", "which", "lean"], cwd=LEAN_ROOT).strip()
    lake = run(["lake", "env", "which", "lake"], cwd=LEAN_ROOT).strip()
    lean_path = run(["lake", "env", "printenv", "LEAN_PATH"], cwd=LEAN_ROOT).strip()
    python = Path(os.path.realpath(os.sys.executable))
    git_path = shutil.which("git")
    assert git_path is not None
    git_executable = Path(os.path.realpath(git_path))
    assert LEAN_COMMIT in run([lean, "--version"])
    assert "5.0.0-src+98dc76e" in run([lake, "--version"])
    assert sha256(Path(lean)) == "3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf"
    assert sha256(Path(lake)) == "a608ff084d7e2af228b92a29d7c2fd083ba0580e46889175ec74a81678c98359"
    assert sha256(python) == "b8d8288faefdd300201f43fcf00f6f539a27218eeed3a3dff5ab10b9c4c99700"
    assert sha256(git_executable) == "8a48eefa306b9a2a9c3e576784a74ad7485779279e5a46ec43361a1864760e45"

    with tempfile.TemporaryDirectory(prefix="m0061-validation-") as tmp_name:
        tmp = Path(tmp_name)
        for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
            (tmp / name).write_bytes((HERE / name).read_bytes())
        base_env = {
            "HOME": os.environ.get("HOME", ""),
            "PATH": os.environ.get("PATH", ""),
            "LANG": "C.UTF-8",
            "LC_ALL": "C.UTF-8",
            "TZ": "UTC",
            "LEAN_PATH": lean_path,
        }
        run([lean, "-t", "0", "-o", "Statement.olean", "Statement.lean"], cwd=tmp, env=base_env)
        module_env = dict(base_env)
        module_env["LEAN_PATH"] = f"{tmp}:{lean_path}"
        obligation_output = run(
            [lean, "-t", "0", "-o", "ObligationTree.olean", "ObligationTree.lean"],
            cwd=tmp,
            env=module_env,
        )
        proof_output = run([lean, "-t", "0", "Proof.lean"], cwd=tmp, env=module_env)
        validation_output = run([lean, "-t", "0", "Validation.lean"], cwd=tmp, env=module_env)

    for declaration in COMPOSITION_DECLARATIONS:
        assert printed_axioms(obligation_output, declaration) <= EXPECTED_AXIOMS
    for declaration in PROOF_DECLARATIONS:
        assert printed_axioms(proof_output, declaration) <= EXPECTED_AXIOMS
    assert printed_axioms(validation_output, "Subgroup.card_subgroup_dvd_card") == EXPECTED_AXIOMS
    assert printed_axioms(validation_output, "independentlyReconstructedTarget") == EXPECTED_AXIOMS
    assert proof_output.count("Declarations are sorry-free!") == len(PROOF_DECLARATIONS)
    assert validation_output.count("Declarations are sorry-free!") == 2
    assert "sorryAx" not in obligation_output + proof_output + validation_output

    assert spec["schema_version"] == "stage1-validation-recipe/1.0"
    assert spec["item_id"] == ITEM and spec["theorem_id"] == THEOREM
    assert spec["cwd"] == "."
    assert spec["argv"] == ["python3", "-B", f"Stage1_Instances/{THEOREM}/check_validation.py"]
    assert spec["env_allowlist"] == {} and spec["timeout_seconds"] == 180
    assert spec["network_policy"] == "denied" and spec["expected_exit"] == 0
    assert "cannot provision a kernel network namespace" in spec["network_enforcement"]
    assert spec["covered_obligation_ids"] == PROOF_IDS

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["phase"] == "validation" and receipt["intent"] == "validate"
    assert receipt["depends_on"] == ["S56-M-0061-PROOF"]
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["release_grade"] is receipt["content_addressed_release_evidence"] is False
    for name, expected in EXPECTED_INPUTS.items():
        assert receipt["inputs"][name] == expected, name
    assert receipt["inputs"]["validation-spec.json"] == sha256(HERE / "validation-spec.json")
    assert receipt["inputs"]["check_validation.py"] == sha256(HERE / "check_validation.py")
    assert receipt["target"]["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert receipt["target"]["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert receipt["environment"]["platform"] == f"{platform.system()} {platform.release()} {platform.machine()}"
    assert receipt["environment"]["lean_executable_sha256"] == sha256(Path(lean))
    assert receipt["environment"]["lake_executable_sha256"] == sha256(Path(lake))
    assert receipt["environment"]["python_executable_sha256"] == sha256(python)
    assert receipt["environment"]["git_executable_sha256"] == sha256(git_executable)
    assert receipt["environment"]["mathlib_revision"] == MATHLIB_REVISION
    assert receipt["environment"]["mathlib_tree"] == MATHLIB_TREE
    assert receipt["result"]["provisional_exact_root_kernel_closed"] is True
    assert receipt["result"]["accepted_root_kernel_closed"] is False
    assert receipt["result"]["accepted_closed_obligation_ids"] == []
    assert receipt["result"]["observed_axioms"] == EXPECTED_AXIOM_LIST
    assert receipt["result"]["hermetic_release_gate"] == "fail_closed"
    assert receipt["result"]["independent_distinct_runner_gate"] == "fail_closed"
    assert receipt["result"]["audit_complete"] is receipt["result"]["theorem_complete"] is False
    assert receipt["first_failed_gate"] == "dependency.S56-M-0061-PROOF.master_acceptance"
    assert receipt["first_failed_release_gate"] == "S56-10.6-HERMETIC-COLD-BUILD"
    assert receipt["recipe"]["argv"] == spec["argv"]
    assert receipt["recipe"]["covered_obligation_ids"] == PROOF_IDS
    expected_stdout = ("\n".join(SUMMARY_LINES) + "\n").encode("utf-8")
    assert receipt["output_evidence"] == {
        "stdout_semantic_sha256": hashlib.sha256(expected_stdout).hexdigest(),
        "expected_line_count": len(SUMMARY_LINES),
        "exit_code": 0,
    }

    assert set(packet) == {
        "item_id",
        "changed_paths",
        "commands",
        "output_summary",
        "base_revision",
        "known_failures",
        "state",
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
    for relative in CHANGED_PATHS:
        assert_text_hygiene(ROOT / relative)

    print("\n".join(SUMMARY_LINES))


if __name__ == "__main__":
    main()
