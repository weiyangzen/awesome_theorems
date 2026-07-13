#!/usr/bin/env python3
"""Fail-closed narrow validator for S56-M-1011-VALIDATION."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-1011"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM = "S56-M-1011-VALIDATION"
THEOREM = "THM-M-1011"
BASE_REVISION = "e6c4d56e017f77b02752e6c1325f0298dfb7f4d4"
BASE_TREE = "3aa71b6797c53e65f39bbac295dabcd2fff8e0a6"
EXPRESSION_SHA256 = "5711575e18ff4a1eecd2ce047a29817d876a6e44cb86c724b476414314f9e812"
DENOMINATOR_SHA256 = "3dd41addcf34fd9ca7d89e9d2231337be0e01df77f497acdcefff743020bdd90"
LEAN_TOOLCHAIN = "leanprover/lean4:v4.29.0"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_REMOTE = "https://github.com/leanprover-community/mathlib4.git"
TOOLCHAIN_SHA256 = "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2"
MANIFEST_SHA256 = "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81"
LICENSE_SHA256 = "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
SOURCE_PROVENANCE = {
    "Mathlib/MeasureTheory/Measure/Prokhorov.lean": {
        "source_sha256": "b8bf3ca4bba9f313270a384088abc17dcfa7e8484d382af55d758159d30a434c",
        "git_blob": "2473371ca5c75ae600f3cb37eb1f61115f46d63a",
        "olean_sha256": "0258296834e5c72eb8f14eba83e6a6807ae7c72c05086ff02fea782810a142ba",
    },
    "Mathlib/MeasureTheory/Measure/Tight.lean": {
        "source_sha256": "8adda2a29a13ef3877a4a343efa71da379f0adda6c615b0186338be89f11eb0b",
        "git_blob": "2b761edc282f39e95c380984c7149caca8cc4330",
        "olean_sha256": "e539e19b58be5a330818db5a57277f3ebfb0ccabc06aab9e455165e48b2a4cf6",
    },
    "Mathlib/MeasureTheory/Measure/ProbabilityMeasure.lean": {
        "source_sha256": "f8e505e1d388a65ef1f0f8e19916a1a673872fa373a922ca78ec05aa807b856d",
        "git_blob": "a3db8bac502b3fd452588271964fe99f90c8e8e0",
        "olean_sha256": "69a9a38958c00f21be94f37e4d628d19da4476ddbfbe5093abcbfa5ffdf6f81e",
    },
    "Mathlib/Topology/Inseparable.lean": {
        "source_sha256": "4b2a40f3fcecdfecd1ca3d36fe3651504dc6eb228fe6ea80ac646dd1437d98c7",
        "git_blob": "49536ae6c422c5e622c7e1e611400fec3498d2fc",
        "olean_sha256": "cc330abb60b46244e900cdc0954fbc8dec5ed45c24a86e3230746a3b88579385",
    },
}
TIMEOUT_SECONDS = 600


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path) -> dict:
    def reject_duplicates(pairs: list[tuple[str, object]]) -> dict:
        value: dict[str, object] = {}
        for key, item in pairs:
            assert key not in value, f"duplicate JSON key in {path}: {key}"
            value[key] = item
        return value

    result = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates)
    assert isinstance(result, dict), path
    return result


def run(
    argv: list[str],
    *,
    cwd: Path = ROOT,
    env: dict[str, str] | None = None,
    timeout: int = TIMEOUT_SECONDS,
    expected_exit: int = 0,
) -> str:
    result = subprocess.run(
        argv,
        cwd=cwd,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=timeout,
        check=False,
    )
    if result.returncode != expected_exit:
        raise RuntimeError(
            f"command exited {result.returncode}, expected {expected_exit}: {argv!r}\n"
            f"{result.stdout}"
        )
    return result.stdout


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["git", *args], cwd=cwd).rstrip()


def source_without_comments(source: str) -> str:
    output: list[str] = []
    index = 0
    depth = 0
    while index < len(source):
        if depth == 0 and source.startswith("--", index):
            newline = source.find("\n", index)
            if newline < 0:
                break
            output.append("\n")
            index = newline + 1
        elif source.startswith("/-", index):
            depth += 1
            index += 2
        elif depth and source.startswith("-/", index):
            depth -= 1
            index += 2
        elif depth:
            if source[index] == "\n":
                output.append("\n")
            index += 1
        else:
            output.append(source[index])
            index += 1
    assert depth == 0, "unterminated Lean block comment"
    return "".join(output)


def reported_axioms(output: str, declaration: str) -> set[str]:
    pattern = re.compile(
        rf"'{re.escape(declaration)}' depends on axioms:\s*\[(?P<axioms>.*?)\]",
        re.DOTALL,
    )
    match = pattern.search(output)
    assert match is not None, f"missing axiom report for {declaration}"
    return {part.strip() for part in match.group("axioms").split(",") if part.strip()}


def assert_text_hygiene(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines()), path


def main() -> None:
    if not __debug__:
        raise RuntimeError("validation requires Python assertions")

    spec = load(HERE / "validation-spec.json")
    receipt = load(HERE / "validation-receipt.json")
    statement = load(HERE / "statement.json")
    instance = load(HERE / "instance.json")
    local_dag = load(HERE / "task-dag.json")
    anchor = load(HERE / "anchor-audit.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    frozen_specs = load(HERE / "validation-specs.json")
    proof_receipt = load(HERE / "proof-receipt.json")
    execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")
    targets = load(ROOT / "Docs" / "Stage1_Targets_rev-5.6.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert BASE_TREE == git("rev-parse", "HEAD^{tree}")
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 260 and target["baseline"] == "L0"
    assert target["lifecycle_mode"] == "planned"
    assert target["rework_required"] is True and target["theorem_complete"] is False
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 260,
        "phase": "validation",
        "layer": 5,
        "state": "[ ]",
        "depends_on": ["S56-M-1011-PROOF"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Run hermetic kernel, trust, provenance, and independent validation gates.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    predecessor = next(row for row in execution["items"] if row["id"] == "S56-M-1011-PROOF")
    assert predecessor["state"] == "[_]" and predecessor["attempts"] == 1
    local_task = next(row for row in local_dag["tasks"] if row["id"] == ITEM)
    assert local_task["state"] == "open"
    assert local_task["depends_on"] == ["S56-M-1011-PROOF"]

    assert instance["lifecycle"] == "planned"
    assert instance["root_vector"] == {"H": "H1", "M": "M5", "R": "R4"}
    assert instance["accepted_proof_state"] == []
    assert instance["audit_complete"] is instance["theorem_complete"] is False
    assert statement["canonical_formal_target"]["declaration_or_expression"] == (
        "Stage1Instances.THM_M_1011.CanonicalStatement"
    )
    assert statement["canonical_formal_target"]["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert statement["canonical_formal_target"]["statement_file_sha256"] == sha256(HERE / "Statement.lean")
    assert registry["frozen_against_statement_sha256"] == sha256(HERE / "Statement.lean")
    assert registry["frozen_against_anchor_audit_sha256"] == sha256(HERE / "anchor-audit.json")
    assert registry["denominator_sha256"] == graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert registry["root_obligation_id"] == graphs["root_node_id"] == "M1011-ROOT"
    assert graphs["closure_boundary"] == {
        "root_closed": False,
        "root_machine_debt": "M5",
        "theorem_complete": False,
        "first_failed_gate": "exact statement match / missing T2Space X",
        "remaining_root_cut_set": ["M1011-N-SEPARATION"],
        "conditional_composition": "Stage1Instances.THM_M_1011.ObligationTree.canonical_of_t2",
    }

    assert proof_receipt["item_id"] == "S56-M-1011-PROOF"
    assert proof_receipt["canonical_target_expression_sha256"] == EXPRESSION_SHA256
    assert proof_receipt["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert proof_receipt["proof_body"]["source_sha256"] == sha256(HERE / "Proof.lean")
    for key, name in (
        ("statement_sha256", "Statement.lean"),
        ("obligation_tree_sha256", "ObligationTree.lean"),
        ("obligation_registry_sha256", "obligation-registry.json"),
        ("typed_graphs_sha256", "typed-graphs.json"),
        ("anchor_audit_sha256", "anchor-audit.json"),
        ("validation_specs_sha256", "validation-specs.json"),
    ):
        assert proof_receipt["inputs"][key] == sha256(HERE / name)
    assert proof_receipt["accepted"] is False
    assert proof_receipt["accepted_closed_obligation_ids"] == []
    assert proof_receipt["result"]["root_kernel_closed"] is True
    assert proof_receipt["result"]["frozen_graph_closed"] is False
    assert proof_receipt["result"]["axioms"] == [
        "propext", "Classical.choice", "Quot.sound",
    ]
    assert proof_receipt["result"]["theorem_complete"] is False

    assert frozen_specs["item_id"] == "S56-M-1011-OBLIGATION_TREE"
    assert len(frozen_specs["recipes"]) == 14
    assert {tuple(row["argv"]) for row in frozen_specs["recipes"]} == {
        ("python3", f"Stage1_Instances/{THEOREM}/check_obligation_tree.py")
    }
    assert all(row["covered_declarations"] == [] for row in frozen_specs["recipes"])

    validation_source = source_without_comments((HERE / "Validation.lean").read_text(encoding="utf-8"))
    assert "import Proof" not in validation_source and "import ObligationTree" not in validation_source
    assert "Proof." not in validation_source and "ObligationTree." not in validation_source
    assert "independentlyReconstructedCanonical" in validation_source
    assert "assert_no_sorry independentlyReconstructedCanonical" in validation_source
    assert sha256(HERE / "Validation.lean") != sha256(HERE / "Proof.lean")
    all_source = "\n".join(
        source_without_comments((HERE / name).read_text(encoding="utf-8"))
        for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean")
    )
    for pattern in (
        r"\bsorry\b",
        r"\badmit\b",
        r"\bsorryAx\b",
        r"^[ \t]*(?:axiom|constant|unsafe|opaque|extern)\b",
        r"\bimplemented_by\b",
        r"\bnative_decide\b",
    ):
        assert re.search(pattern, all_source, re.MULTILINE) is None, pattern

    assert sha256(LEAN_ROOT / "lean-toolchain") == TOOLCHAIN_SHA256
    assert sha256(LEAN_ROOT / "lake-manifest.json") == MANIFEST_SHA256
    manifest = load(LEAN_ROOT / "lake-manifest.json")
    mathlib_entry = next(row for row in manifest["packages"] if row["name"] == "mathlib")
    assert mathlib_entry["rev"] == mathlib_entry["inputRev"] == MATHLIB_REVISION
    assert MATHLIB.resolve().is_dir(), "canonical pinned mathlib artifact missing"
    assert git("rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert git("remote", "get-url", "origin", cwd=MATHLIB) == MATHLIB_REMOTE
    assert git("status", "--porcelain=v1", "--untracked-files=all", cwd=MATHLIB) == ""
    assert sha256(MATHLIB / "LICENSE") == LICENSE_SHA256
    for source, expected in SOURCE_PROVENANCE.items():
        source_path = MATHLIB / source
        olean_path = MATHLIB / ".lake" / "build" / "lib" / "lean" / source.replace(".lean", ".olean")
        assert sha256(source_path) == expected["source_sha256"]
        assert git("rev-parse", f"HEAD:{source}", cwd=MATHLIB) == expected["git_blob"]
        assert sha256(olean_path) == expected["olean_sha256"]

    fixed_env = os.environ.copy()
    fixed_env.update({
        "ELAN_TOOLCHAIN": LEAN_TOOLCHAIN,
        "LANG": "C.UTF-8",
        "LC_ALL": "C.UTF-8",
        "TZ": "UTC",
        "LEAN_NUM_THREADS": "1",
    })
    lean = Path(run(["lake", "env", "which", "lean"], cwd=LEAN_ROOT, env=fixed_env).strip())
    lake = Path(run(["lake", "env", "which", "lake"], cwd=LEAN_ROOT, env=fixed_env).strip())
    lean_path = run(["lake", "env", "printenv", "LEAN_PATH"], cwd=LEAN_ROOT, env=fixed_env).strip()
    python = Path(os.path.realpath(os.sys.executable))
    git_path = Path(os.path.realpath(shutil.which("git") or ""))
    bwrap = Path(shutil.which("bwrap") or "")
    assert all(path.is_file() for path in (lean, lake, python, git_path, bwrap))
    assert LEAN_COMMIT in run([str(lean), "--version"], env=fixed_env)
    assert "5.0.0-src+98dc76e" in run([str(lake), "--version"], env=fixed_env)
    assert receipt["environment"]["python_version"] in run(
        [str(python), "--version"], env=fixed_env
    )
    assert receipt["environment"]["bubblewrap_version"] in run(
        [str(bwrap), "--version"], env=fixed_env
    )
    assert sha256(lean) == receipt["environment"]["lean_executable_sha256"]
    assert sha256(lake) == receipt["environment"]["lake_executable_sha256"]
    assert sha256(python) == receipt["environment"]["python_executable_sha256"]
    assert sha256(git_path) == receipt["environment"]["git_executable_sha256"]
    assert sha256(bwrap) == receipt["environment"]["bubblewrap_executable_sha256"]

    tmp = Path(tempfile.mkdtemp(prefix="stage1-m1011-validation-", dir="/tmp"))
    try:
        for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
            shutil.copy2(HERE / name, tmp / name)
        (tmp / "home").mkdir()

        def isolated_lean(args: list[str], *, use_tmp_path: bool) -> str:
            path = f"{tmp}:{lean_path}" if use_tmp_path else lean_path
            return run(
                [
                    str(bwrap),
                    "--ro-bind", "/", "/",
                    "--bind", str(tmp), str(tmp),
                    "--dev", "/dev",
                    "--proc", "/proc",
                    "--unshare-net",
                    "--die-with-parent",
                    "--setenv", "HOME", str(tmp / "home"),
                    "--setenv", "ELAN_TOOLCHAIN", LEAN_TOOLCHAIN,
                    "--setenv", "LANG", "C.UTF-8",
                    "--setenv", "LC_ALL", "C.UTF-8",
                    "--setenv", "TZ", "UTC",
                    "--setenv", "LEAN_NUM_THREADS", "1",
                    "--setenv", "LEAN_PATH", path,
                    "--chdir", str(tmp),
                    str(lean), "--trust=0", "-t0", "--root", str(tmp),
                    *args,
                ],
                env=fixed_env,
            )

        statement_output = isolated_lean(["-o", "Statement.olean", "Statement.lean"], use_tmp_path=False)
        obligation_output = isolated_lean(
            ["-o", "ObligationTree.olean", "ObligationTree.lean"], use_tmp_path=True
        )
        proof_output = isolated_lean(["Proof.lean"], use_tmp_path=True)
        validation_output = isolated_lean(["Validation.lean"], use_tmp_path=True)
    finally:
        shutil.rmtree(tmp)

    combined_output = "\n".join(
        (statement_output, obligation_output, proof_output, validation_output)
    )
    assert "sorryAx" not in combined_output
    assert "Declarations are sorry-free!" in validation_output
    for output, declaration in (
        (proof_output, "Stage1Instances.THM_M_1011.Proof.canonical"),
        (
            validation_output,
            "Stage1Instances.THM_M_1011.Validation.independentlyReconstructedCanonical",
        ),
        (validation_output, "isCompact_closure_of_isTightMeasureSet"),
        (validation_output, "MeasureTheory.isTightMeasureSet_of_isCompact_closure"),
    ):
        assert reported_axioms(output, declaration) == EXPECTED_AXIOMS

    assert spec["schema_version"] == "stage1-validation-recipe/1.0"
    assert spec["item_id"] == ITEM and spec["theorem_id"] == THEOREM
    assert spec["cwd"] == "."
    assert spec["argv"] == ["python3", "-I", "-B", f"Stage1_Instances/{THEOREM}/check_validation.py"]
    assert spec["env_allowlist"] == {} and spec["timeout_seconds"] == TIMEOUT_SECONDS
    assert spec["network_policy"] == "denied" and spec["expected_exit"] == 0
    assert set(spec["covered_obligation_ids"]) == set(receipt["covered_obligation_ids"])
    assert spec["covered_declarations"] == receipt["covered_declarations"]

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["phase"] == "validation" and receipt["intent"] == "validate"
    assert receipt["depends_on"] == ["S56-M-1011-PROOF"]
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["release_grade"] is False and receipt["content_addressed"] is False
    assert receipt["accepted_closed_obligation_ids"] == []
    assert receipt["canonical_target"]["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert receipt["canonical_target"]["registry_denominator_sha256"] == DENOMINATOR_SHA256
    for name, expected in receipt["inputs"].items():
        if name not in {"check_validation.py", "validation-receipt.json"}:
            assert sha256(HERE / name) == expected, name
    assert receipt["inputs"]["check_validation.py"] == sha256(Path(__file__).resolve())
    assert receipt["result"]["kernel_replay"] == "provisional_pass"
    assert receipt["result"]["network_isolated_warm_replay"] == "pass"
    assert receipt["result"]["differential_exact_root"] == (
        "provisional_pass_same_worker_same_route_and_terminal_bodies"
    )
    assert set(receipt["result"]["observed_axioms"]) == EXPECTED_AXIOMS
    assert receipt["result"]["accepted_root_closed"] is False
    assert receipt["result"]["audit_complete"] is receipt["result"]["theorem_complete"] is False
    assert receipt["first_failed_gate"] == "dependency.S56-M-1011-PROOF.master_acceptance"
    assert receipt["first_failed_release_gate"] == "S56-10.6-HERMETIC-COLD-BUILD"

    selftest_path = ROOT / ".stage1-worker-selftest.json"
    if selftest_path.exists():
        selftest = load(selftest_path)
        assert set(selftest) == {
            "item_id", "changed_paths", "commands", "output_summary",
            "base_revision", "known_failures", "state",
        }
        assert selftest["item_id"] == ITEM and selftest["state"] == "[_]"
        assert selftest["base_revision"] == BASE_REVISION
        assert selftest["known_failures"] == receipt["known_failures"]

    for name in (
        "Validation.lean", "check_validation.py", "validation-spec.json",
        "validation-receipt.json", "validation-phase.md",
    ):
        assert_text_hygiene(HERE / name)

    summary = (
        "PASS S56-M-1011-VALIDATION: network-isolated trust-zero warm replay checked "
        "the exact proof root and a same-worker differential quotient reconstruction; both "
        "roots are transitively sorry-free and use exactly propext, Classical.choice, and "
        "Quot.sound; proof acceptance, frozen-route reconciliation, complete TCB/provenance, "
        "cold offline replay, and distinct-runner verification fail closed"
    )
    assert receipt["recipe"]["stdout_semantic_sha256"] == hashlib.sha256(
        (summary + "\n").encode("utf-8")
    ).hexdigest()
    print(summary)


if __name__ == "__main__":
    main()
