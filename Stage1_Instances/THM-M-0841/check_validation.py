#!/usr/bin/env python3
"""Fail-closed narrow validator for S56-M-0841-VALIDATION."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import platform
import re
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0841"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
ITEM = "S56-M-0841-VALIDATION"
THEOREM = "THM-M-0841"
BASE_REVISION = "6bf9ee93a322e7d25cf9249226222095f95d1cff"
BASE_TREE = "24acf86e69ab2e6fca9480c6269b6429874ba295"
TOOLCHAIN = "leanprover/lean4:v4.29.0"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_REMOTE = "https://github.com/leanprover-community/mathlib4.git"
MATHLIB_LICENSE_SHA256 = "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1"
THEOREM_DAG_SHA256 = "73e99d2276c8ba9fec8f89ed41b712308d7f5667e95ba8185e49f1f5bfd40eca"
DEPENDENCY_CONTEXT_SHA256 = "068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c"
TOOLCHAIN_SHA256 = "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2"
MANIFEST_SHA256 = "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81"
LEAN_SHA256 = "3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf"
LAKE_SHA256 = "a608ff084d7e2af228b92a29d7c2fd083ba0580e46889175ec74a81678c98359"
ELAN_SHA256 = "840179e70803ef373c2ec53342d6a45ea7d022533e4145489fc1278b4f716385"
BWRAP_SHA256 = "0abea81db798ebf6b4742ac0664802d97521547a353c2a0dbdc21d76cbbfd2c0"
PYTHON_SHA256 = "b8d8288faefdd300201f43fcf00f6f539a27218eeed3a3dff5ab10b9c4c99700"
GIT_SHA256 = "5516c9f362c29376ab9a499a33082f9f611941d8c75930c880e30ad109e39c9a"
EXPRESSION_SHA256 = "ed4a8b422615bfafc69ab9f770dc99b77d308d78bca30e67790206426799a733"
DENOMINATOR_SHA256 = "9e59690364fbc34301457900dd8ba573bce76a64a8dbeb9dca38d77e19953617"
ROOT_VECTOR = {"H": "H1", "M": "M3", "R": "R4"}
OPEN_ROOT_CUT = [
    "M0841-S-COMPLEMENT-TRANSPORT",
    "M0841-B-R-TWO",
    "M0841-B-R-GE-THREE",
]
FORMAL_PREMISE_CUT = ["M0841-B-R-TWO", "M0841-B-R-GE-THREE"]
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
PROOF_DECLARATIONS = (
    "Stage1Instances.THM_M_0841_Proof.cast_choose_two",
    "Stage1Instances.THM_M_0841_Proof.card_edgeFinset_compl",
    "Stage1Instances.THM_M_0841_Proof.sparseFromDense",
    "Stage1Instances.THM_M_0841_Proof.denseFamily_of_base_step",
    "Stage1Instances.THM_M_0841_Proof.erdosStone_of_dense_base_step",
)
DIFFERENTIAL_DECLARATION = (
    "Stage1Instances.THM_M_0841_Validation.rootFromDenseProducts"
)
COVERED_OBLIGATIONS = [
    "M0841-ROOT",
    "M0841-S-COMPLEMENT-TRANSPORT",
    "M0841-B-R-TWO",
    "M0841-B-R-GE-THREE",
    "M0841-T-DENSE-ASSEMBLE",
    "M0841-T-ROOT-COMPOSE",
    "M0841-X-PROVENANCE",
    "M0841-X-TRUST",
]
EXPECTED_INPUTS = {
    "Statement.lean": "897dcc398df34c0dd6ad02dc2092a08f46a6cafc908c2e9f8497a895aa66663d",
    "AnchorAudit.lean": "74c99cd0748b040749e2dbaa1ce20a85cfece451987cf84d6e2612a6b1026010",
    "ObligationTree.lean": "35b5fb5dd8e85b83b0d86f75b29b601401d3f92f0a8b258ef800a8a732fcabc1",
    "Proof.lean": "f99031e19bcba0ef08f2bb135d6a8ff19ed586fc356e7f9f6ad8cfd573acb4e1",
    "statement.json": "667a81a44bc2d7d5a822141426396e3c23b83a94a802cb4d385af38eb41d4ec8",
    "anchor-audit.json": "10275b8946fb134c2788e7104f39c1cf0dbeb6e28bbf293303846726a4f0cc4b",
    "obligation-registry.json": "bb7f423225520286e0942afd1553a37c718ff1a98a14c928d9f716ff3b67c694",
    "typed-graphs.json": "494e39a93037052dd903ca1f75f50a80ceee6574fb0cf5cc61ade75429ac48b1",
    "validation-specs.json": "d90668ee9c899782c4725afd90bd34528f308bc38d5412fb99222348c9c63003",
    "proof-receipt.json": "0cd8f806cbed0e67d2cdc2dde4482325a99f67141cf27f4ae63861d53c4f01e4",
    "proof-blocker.json": "8074709ca4e2f10c1ee3ff88e4ebbe65c7da877e85dd0b3ffaea159669145a00",
    "statement-receipt.json": "1afbd23c7fff4f9e72335a76184def964990ab00dbecbdedab30ae62daeadd07",
    "anchor-audit-receipt.json": "b7df9a8afd3b0e664e41abb2cb6cf1454deefc63772bd2b7bb6538c9c7b0e447",
    "obligation-tree-receipt.json": "062474853cbf2fbfe9fe92454c709a1fba54cffc9eaf1ef3da58515b86b2f7d0",
    "instance.json": "c9f17e399829068f9d0ca6c59074b7efc0cad15869a38f826e20ec4faf78bf88",
    "task-dag.json": "d34e479eb0f236087a8c01dc04f866a74e4cc7a1cd706bebebafda55df7aabe5",
}
EXPECTED_V2_ARTIFACTS = {
    "Stage1_Instances/THM-M-0841/AnchorAudit.lean": "74c99cd0748b040749e2dbaa1ce20a85cfece451987cf84d6e2612a6b1026010",
    "Stage1_Instances/THM-M-0841/IntakeProbe.lean": "b33f4571e3166003ce399c8827c9e4835c74b08a63ff4ead5917c432389da78d",
    "Stage1_Instances/THM-M-0841/ObligationTree.lean": "35b5fb5dd8e85b83b0d86f75b29b601401d3f92f0a8b258ef800a8a732fcabc1",
    "Stage1_Instances/THM-M-0841/Proof.lean": "f99031e19bcba0ef08f2bb135d6a8ff19ed586fc356e7f9f6ad8cfd573acb4e1",
    "Stage1_Instances/THM-M-0841/Statement.lean": "897dcc398df34c0dd6ad02dc2092a08f46a6cafc908c2e9f8497a895aa66663d",
    "Stage1_Instances/THM-M-0841/anchor-audit-receipt.json": "b7df9a8afd3b0e664e41abb2cb6cf1454deefc63772bd2b7bb6538c9c7b0e447",
    "Stage1_Instances/THM-M-0841/intake-receipt.json": "0bba475036399da8189bfb4ba4151cd2f8b9b709a956a7aeac8e12b6311a8c3a",
    "Stage1_Instances/THM-M-0841/obligation-tree-receipt.json": "062474853cbf2fbfe9fe92454c709a1fba54cffc9eaf1ef3da58515b86b2f7d0",
    "Stage1_Instances/THM-M-0841/proof-receipt.json": "0cd8f806cbed0e67d2cdc2dde4482325a99f67141cf27f4ae63861d53c4f01e4",
    "Stage1_Instances/THM-M-0841/statement-receipt.json": "1afbd23c7fff4f9e72335a76184def964990ab00dbecbdedab30ae62daeadd07",
}
SOURCE_PROVENANCE = {
    "Mathlib/Analysis/SpecialFunctions/Log/Basic.lean": {
        "source_git_blob": "c62c90eeb1a2b306651e8a46addd560f2681a890",
        "source_sha256": "d6caebfcc45de74cf22aeff92815e30596697c39ddb2bd83927b06dccf14e216",
        "olean_sha256": "096b203af6f9590d61effba77df8f8633df17bccedf65e89fb74f7e137cbd15e",
    },
    "Mathlib/Combinatorics/SimpleGraph/CompleteMultipartite.lean": {
        "source_git_blob": "d8c46737a0c7ac4062b7d0704c2a84a368aff314",
        "source_sha256": "47d5f3f6aeef27940353ed98341de68673139973198de234482adbc139afb236",
        "olean_sha256": "1fc771201717ad6ebfb78ba8d76833b7e217d164a89712ec568494bf24ee181c",
    },
    "Mathlib/Combinatorics/SimpleGraph/Finite.lean": {
        "source_git_blob": "a111f858a1b79cae5c68eaa94bfdf104c50063cf",
        "source_sha256": "968b2c58d0e77e91c69815bf1ed5e3fafa7302eaebc08139d9fdbb323ad910e8",
        "olean_sha256": "07aa71c7c0cb4dc2a1d6c98f710e6f1dd10b5083bdd896d033a3dadf61f09185",
    },
    "Mathlib/Data/Nat/Choose/Basic.lean": {
        "source_git_blob": "15a5c95dae82b6fc0ae14eebe85215f89853f7ee",
        "source_sha256": "b3c40f47d39427428d70518b48adaaf16d3622698b32406fa7745749f1387170",
        "olean_sha256": "057f7b9cc9a9d24c4d1e2d7fcdec76cf6909fd0ee0439bbe59c25a823efcbf10",
    },
    "Mathlib/Algebra/Group/Nat/Even.lean": {
        "source_git_blob": "635aa8eb39216683e54b47cc0dbda31e4dc129a1",
        "source_sha256": "02750b43587d8531c35fbd857c1c3553fa422c85b86c5611910fdd911c65e77a",
        "olean_sha256": "c6c12e91e3a8bea8595102dd5009de5226bc680dea026931bb71da8f2c7810ac",
    },
    "Mathlib/Algebra/Order/Archimedean/Basic.lean": {
        "source_git_blob": "12aada448a6a8f4b9d5ff4c45514e0b35f0a6118",
        "source_sha256": "eea25795220c723c3dfdb55aa9ab5c62c4aec21947bc9f12732fde95bd7cadc0",
        "olean_sha256": "152ecdb674dd499267046355b0b801327b430e376d950c490d8ce4e86cbead79",
    },
    "Mathlib/Order/BooleanAlgebra/Basic.lean": {
        "source_git_blob": "6c1dc1ef1ecfaa4420943069182ccf68661b7874",
        "source_sha256": "70bd2dff4beea732ee74989b333c59e491ce568fbcfdb38cf7f8718f82ea23f9",
        "olean_sha256": "c3da919fea8815bf23c8b9901bfe414b3d04955852ee785221857168b852635e",
    },
    "Mathlib/Util/AssertNoSorry.lean": {
        "source_git_blob": "060d8a764d2a6d1d2963d9c500b6084a05bed534",
        "source_sha256": "aa9f7bebacafc688c894ef2171930e51ed19e0dfe722581848a2414d28900d4d",
        "olean_sha256": "c8bf37753d9bad47b9fe67e32436da8b9af516a4abbbe14e74726f01ba2fb30b",
    },
    "Mathlib/Util/PrintSorries.lean": {
        "source_git_blob": "24d72cc680fa8b07f0d1062f670a5a824934a227",
        "source_sha256": "03670b0b0007740e5390dadd49c3d10a02b7d0919092d2b3214ef8a6a8cf798f",
        "olean_sha256": "9bcc4076e0aee5febb2eea5cf9dc959f38526e9f974afdfdd8658bfd318d5bb7",
    },
}
CHANGED_PATHS = [
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/Validation.lean",
    f"Stage1_Instances/{THEOREM}/check_validation.py",
    f"Stage1_Instances/{THEOREM}/dependency-reuse-ledger.json",
    f"Stage1_Instances/{THEOREM}/validation-blocker.json",
    f"Stage1_Instances/{THEOREM}/validation-phase.md",
    f"Stage1_Instances/{THEOREM}/validation-receipt.json",
    f"Stage1_Instances/{THEOREM}/validation-spec.json",
]
RECIPE_ARGV = [
    "/usr/bin/python3",
    "-I",
    "-B",
    f"Stage1_Instances/{THEOREM}/check_validation.py",
    "--worker-packet",
    ".stage1-worker-selftest.json",
]
RECIPE_COMMAND = {"argv": RECIPE_ARGV, "exit_code": 0}
SUMMARY_LINES = [
    "PASS narrow replay: exact statement, anchor probes, conditional architecture, five proof bodies, and differential composition elaborate at trust zero with network denied",
    "PASS trust observation: six checked roots are sorry-free and use only propext, Classical.choice, and Quot.sound",
    "PASS selected provenance: frozen inputs, empty v2 dependency context, clean mathlib pin, selected sources and oleans, toolchain, and license agree",
    "OPEN exact root: DenseBase and DenseStep have no proof bodies; accepted root remains M3 with three frozen cut obligations",
    "FAIL CLOSED validation authority: proof is worker-provisional, graph closure is zero, and complete foundation, provenance, and TCB acceptance are absent",
    "FAIL CLOSED release gates: shared warm cache is not cold hermetic evidence and this worker is not a distinct signed verifier",
]

if not __debug__:
    raise RuntimeError("validation requires Python assertions; optimized mode is forbidden")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path) -> dict:
    def reject_duplicates(pairs: list[tuple[str, object]]) -> dict:
        result: dict[str, object] = {}
        for key, value in pairs:
            assert key not in result, f"duplicate JSON key in {path}: {key}"
            result[key] = value
        return result

    value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates)
    assert isinstance(value, dict), path
    return value


def run(
    argv: list[str],
    *,
    cwd: Path = ROOT,
    env: dict[str, str] | None = None,
    timeout: int = 600,
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
    if result.returncode != 0:
        raise RuntimeError(f"command failed ({result.returncode}): {argv!r}\n{result.stdout}")
    return result.stdout


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["/usr/bin/git", *args], cwd=cwd).strip()


def code_without_comments(source: str) -> str:
    """Remove nested Lean comments, line comments, and string contents."""
    output: list[str] = []
    index = 0
    depth = 0
    in_string = False
    while index < len(source):
        if depth:
            if source.startswith("/-", index):
                depth += 1
                index += 2
            elif source.startswith("-/", index):
                depth -= 1
                index += 2
            else:
                index += 1
        elif in_string:
            if source[index] == "\\" and index + 1 < len(source):
                index += 2
            elif source[index] == '"':
                in_string = False
                output.append('"')
                index += 1
            else:
                index += 1
        elif source.startswith("/-", index):
            depth = 1
            index += 2
        elif source.startswith("--", index):
            end = source.find("\n", index)
            index = len(source) if end < 0 else end
        elif source[index] == '"':
            in_string = True
            output.append('"')
            index += 1
        else:
            output.append(source[index])
            index += 1
    assert depth == 0 and not in_string, "unterminated Lean comment or string"
    return "".join(output)


def printed_axioms(output: str, declaration: str) -> set[str]:
    match = re.search(
        rf"'[^']*{re.escape(declaration.rsplit('.', 1)[-1])}' depends on axioms:\s*\[(.*?)\]",
        output,
        flags=re.DOTALL,
    )
    if match is None:
        assert f"'{declaration}' does not depend on any axioms" in output
        return set()
    return {
        part.strip()
        for part in match.group(1).replace("\n", "").split(",")
        if part.strip()
    }


def assert_text_hygiene(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data, path
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines()), path


def compiled_roots() -> list[Path]:
    roots = sorted(
        (path / ".lake" / "build" / "lib" / "lean").resolve()
        for path in (LEAN_ROOT / ".lake" / "packages").iterdir()
        if path.is_dir() and (path / ".lake" / "build" / "lib" / "lean").is_dir()
    )
    assert roots, "no pre-existing pinned compiled artifacts"
    return roots


def sandboxed_replay(lean: Path, bwrap: Path) -> dict[str, str]:
    with tempfile.TemporaryDirectory(prefix="m0841-validation-", dir="/tmp") as tmp_name:
        tmp = Path(tmp_name).resolve()
        names = (
            "Statement.lean",
            "AnchorAudit.lean",
            "ObligationTree.lean",
            "Proof.lean",
            "Validation.lean",
        )
        for name in names:
            (tmp / name).write_bytes((HERE / name).read_bytes())
        dependency_path = ":".join(str(path) for path in compiled_roots())
        base = [
            str(bwrap),
            "--ro-bind",
            "/",
            "/",
            "--bind",
            str(tmp),
            str(tmp),
            "--dev",
            "/dev",
            "--proc",
            "/proc",
            "--unshare-net",
            "--die-with-parent",
            "--clearenv",
            "--setenv",
            "HOME",
            str(tmp),
            "--setenv",
            "TMPDIR",
            str(tmp),
            "--setenv",
            "LANG",
            "C.UTF-8",
            "--setenv",
            "LC_ALL",
            "C.UTF-8",
            "--setenv",
            "TZ",
            "UTC",
            "--setenv",
            "LEAN_NUM_THREADS",
            "1",
            "--chdir",
            str(tmp),
        ]

        def lean_run(name: str, local_imports: bool, emit_olean: bool) -> str:
            lean_path = f"{tmp}:{dependency_path}" if local_imports else dependency_path
            argv = base + ["--setenv", "LEAN_PATH", lean_path, str(lean), "--trust=0", "-t0"]
            if emit_olean:
                argv += ["-o", Path(name).with_suffix(".olean").name]
            argv.append(name)
            return run(argv, timeout=600)

        return {
            "statement": lean_run("Statement.lean", False, True),
            "anchor_audit": lean_run("AnchorAudit.lean", True, False),
            "obligation_tree": lean_run("ObligationTree.lean", True, True),
            "proof": lean_run("Proof.lean", True, True),
            "validation": lean_run("Validation.lean", True, False),
        }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--probe", action="store_true")
    parser.add_argument("--worker-packet", type=Path)
    args = parser.parse_args()

    execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")
    targets = load(ROOT / "Docs" / "Stage1_Targets_rev-5.6.json")
    theorem_dag_path = ROOT / "Docs" / "Stage1_Theorem_DAG_v2.json"
    theorem_dag = load(theorem_dag_path)
    statement = load(HERE / "statement.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    proof_receipt = load(HERE / "proof-receipt.json")
    proof_blocker = load(HERE / "proof-blocker.json")
    instance = load(HERE / "instance.json")
    local_tasks = load(HERE / "task-dag.json")
    dependency_ledger = load(HERE / "dependency-reuse-ledger.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 1398 and target["baseline"] == "L0"
    assert target["lifecycle_mode"] == "planned"
    assert target["rework_required"] is True and target["theorem_complete"] is False
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 1398,
        "phase": "validation",
        "layer": 5,
        "state": "[ ]",
        "depends_on": ["S56-M-0841-PROOF"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Run hermetic kernel, trust, provenance, and independent validation gates.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    predecessor = next(row for row in execution["items"] if row["id"] == "S56-M-0841-PROOF")
    assert predecessor["state"] == "[_]" and predecessor["attempts"] == 1
    assert local_tasks["accepted_states"] == []
    assert all(task["state"] == "open" for task in local_tasks["tasks"])

    assert sha256(theorem_dag_path) == THEOREM_DAG_SHA256
    theorem_node = next(row for row in theorem_dag["theorems"] if row["theorem_id"] == THEOREM)
    assert theorem_node["dependency_context_sha256"] == DEPENDENCY_CONTEXT_SHA256
    assert theorem_node["direct_hard_parents"] == []
    assert theorem_node["transitive_hard_ancestors"] == []
    assert theorem_node["direct_reuse_hint_ids"] == []
    assert theorem_node["shared_lemma_group_ids"] == []
    observed_artifacts = {
        row["path"]: row["sha256"] for row in theorem_node["reusable_artifacts"]
    }
    assert observed_artifacts == EXPECTED_V2_ARTIFACTS
    assert dependency_ledger == {
        "schema_version": "stage1-dependency-reuse-ledger/1.1",
        "consumer_theorem_id": THEOREM,
        "observed_theorem_dag_sha256": THEOREM_DAG_SHA256,
        "dependency_context_sha256": DEPENDENCY_CONTEXT_SHA256,
        "repository_revision": BASE_REVISION,
        "direct_parent_ids": [],
        "transitive_ancestor_ids": [],
        "hard_edge_ids": [],
        "reuse_hint_ids": [],
        "shared_group_ids": [],
        "inspections": [],
        "reuse_decisions": [],
        "unresolved_compatibility_obligations": [],
    }

    for name, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"stale validation input: {name}"
    assert sha256(LEAN_ROOT / "lean-toolchain") == TOOLCHAIN_SHA256
    assert sha256(LEAN_ROOT / "lake-manifest.json") == MANIFEST_SHA256
    canonical = statement["canonical_formal_target"]
    assert canonical["declaration_or_expression"] == (
        "Stage1Instances.THM_M_0841.ErdosStoneTarget"
    )
    assert canonical["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert canonical["statement_file_sha256"] == EXPECTED_INPUTS["Statement.lean"]
    assert registry["frozen_against_statement_sha256"] == EXPECTED_INPUTS["Statement.lean"]
    assert registry["frozen_against_anchor_audit_sha256"] == EXPECTED_INPUTS["anchor-audit.json"]
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    root = next(node for node in graphs["nodes"] if node["obligation_id"] == "M0841-ROOT")
    assert {
        "H": root["human_debt"],
        "M": root["machine_debt"],
        "R": root["readability_debt"],
    } == ROOT_VECTOR
    closure = graphs["closure_boundary"]
    assert closure["closed_obligations"] == [] and closure["root_closed"] is False
    assert closure["remaining_machine_root_cut_set"] == [
        "M0841-B-R-TWO",
        "M0841-B-R-GE-THREE",
        "M0841-S-COMPLEMENT-TRANSPORT",
    ]
    assert closure["audit_complete"] is closure["theorem_complete"] is False
    assert len(graphs["unverified_decomposition_plans"]) == 25
    assert instance["root_vector"] == ROOT_VECTOR
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == []
    assert instance["audit_complete"] is instance["theorem_complete"] is False
    assert proof_receipt["item_id"] == "S56-M-0841-PROOF"
    assert proof_receipt["accepted"] is False
    assert proof_receipt["provisionally_closed_obligation_ids"] == []
    assert proof_receipt["accepted_closed_obligation_ids"] == []
    assert proof_receipt["result"]["root_kernel_closed"] is False
    assert proof_receipt["remaining_root_cut_set"] == OPEN_ROOT_CUT
    assert proof_receipt["formal_premise_cut_using_direct_body"] == FORMAL_PREMISE_CUT
    assert proof_blocker["root_closed"] is proof_blocker["theorem_complete"] is False

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by|extern|run_tac)\b|"
        r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
        r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
        r"(?:axiom|constant|opaque|unsafe)\b",
        flags=re.MULTILINE,
    )
    for name in (
        "IntakeProbe.lean",
        "Statement.lean",
        "AnchorAudit.lean",
        "ObligationTree.lean",
        "Proof.lean",
        "Validation.lean",
    ):
        source = code_without_comments((HERE / name).read_text(encoding="utf-8"))
        assert prohibited.search(source) is None, name
    validation_source = code_without_comments((HERE / "Validation.lean").read_text())
    assert "theorem rootFromDenseProducts" in validation_source
    assert "(base : DenseBase) (step : DenseStep)" in validation_source
    assert "theorem erdosStoneTarget" not in validation_source

    manifest = load(LEAN_ROOT / "lake-manifest.json")
    mathlib_entry = next(row for row in manifest["packages"] if row["name"] == "mathlib")
    assert mathlib_entry["rev"] == mathlib_entry["inputRev"] == MATHLIB_REVISION
    assert (LEAN_ROOT / ".lake").is_symlink()
    mathlib = (LEAN_ROOT / ".lake" / "packages" / "mathlib").resolve()
    assert git("rev-parse", "HEAD", cwd=mathlib) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == MATHLIB_TREE
    assert git("remote", "get-url", "origin", cwd=mathlib) == MATHLIB_REMOTE
    assert git("status", "--porcelain=v1", cwd=mathlib) == ""
    assert sha256(mathlib / "LICENSE") == MATHLIB_LICENSE_SHA256
    for relative, expected in SOURCE_PROVENANCE.items():
        source = mathlib / relative
        olean = mathlib / ".lake" / "build" / "lib" / "lean" / Path(relative).with_suffix(
            ".olean"
        )
        assert git("rev-parse", f"HEAD:{relative}", cwd=mathlib) == expected["source_git_blob"]
        assert sha256(source) == expected["source_sha256"]
        assert sha256(olean) == expected["olean_sha256"]

    fixed_env = {
        "ELAN_TOOLCHAIN": TOOLCHAIN,
        "LANG": "C.UTF-8",
        "LC_ALL": "C.UTF-8",
        "TZ": "UTC",
        "LEAN_NUM_THREADS": "1",
    }
    elan = Path("/home/sansha-2/.elan/bin/elan")
    bwrap = Path("/usr/bin/bwrap")
    python = Path("/usr/bin/python3").resolve()
    git_executable = Path("/usr/bin/git")
    tool_root = Path.home() / ".elan" / "toolchains" / "leanprover--lean4---v4.29.0" / "bin"
    lean = tool_root / "lean"
    lake = tool_root / "lake"
    assert sha256(lean) == LEAN_SHA256
    assert sha256(lake) == LAKE_SHA256
    assert sha256(elan) == ELAN_SHA256
    assert sha256(bwrap) == BWRAP_SHA256
    assert sha256(python) == PYTHON_SHA256
    assert sha256(git_executable) == GIT_SHA256
    assert LEAN_COMMIT in run([str(lean), "--version"], env=fixed_env)
    assert "5.0.0-src+98dc76e" in run([str(lake), "--version"], env=fixed_env)

    outputs = sandboxed_replay(lean, bwrap)
    for declaration in PROOF_DECLARATIONS:
        assert printed_axioms(outputs["proof"], declaration) == EXPECTED_AXIOMS
        assert printed_axioms(outputs["validation"], declaration) == EXPECTED_AXIOMS
    assert printed_axioms(outputs["validation"], DIFFERENTIAL_DECLARATION) == EXPECTED_AXIOMS
    assert outputs["proof"].count("Declarations are sorry-free!") == 1
    assert outputs["validation"].count("Declarations are sorry-free!") == 1
    combined = "\n".join(outputs.values())
    assert "sorryAx" not in combined and "declaration uses 'sorry'" not in combined
    closure_match = re.search(
        r"VALIDATION_CLOSURE roots=(\d+) declarations=(\d+) modules=(\d+)",
        outputs["validation"],
    )
    assert closure_match is not None and int(closure_match.group(1)) == 6
    assert "VALIDATION_CLOSURE axioms=[propext, Classical.choice, Quot.sound]" in outputs[
        "validation"
    ]
    assert "VALIDATION_CLOSURE bodyless_nonaxioms=[]" in outputs["validation"]
    assert "VALIDATION_CLOSURE unsafe=[]" in outputs["validation"]
    observation = {
        "lean_output_sha256": {
            name: hashlib.sha256(output.encode()).hexdigest() for name, output in outputs.items()
        },
        "closure": {
            "roots": 6,
            "declarations": int(closure_match.group(2)),
            "modules": int(closure_match.group(3)),
            "axioms": sorted(EXPECTED_AXIOMS),
            "bodyless_nonaxioms": [],
            "unsafe_declarations": [],
        },
    }
    if args.probe:
        print(json.dumps(observation, sort_keys=True))
        return

    spec = load(HERE / "validation-spec.json")
    receipt = load(HERE / "validation-receipt.json")
    blocker = load(HERE / "validation-blocker.json")
    assert spec["schema_version"] == "stage1-validation-spec/1.0"
    assert spec["item_id"] == receipt["item_id"] == blocker["item_id"] == ITEM
    assert spec["theorem_id"] == receipt["theorem_id"] == blocker["theorem_id"] == THEOREM
    assert spec["depends_on"] == receipt["depends_on"] == ["S56-M-0841-PROOF"]
    assert len(spec["recipes"]) == 1
    recipe = spec["recipes"][0]
    assert recipe["cwd"] == "." and recipe["argv"] == RECIPE_ARGV
    assert recipe["env_allowlist"] == {}
    assert recipe["network_policy"] == "denied" and recipe["expected_exit"] == 0
    assert recipe["covered_obligation_ids"] == COVERED_OBLIGATIONS
    assert recipe["covered_declarations"] == [
        "Stage1Instances.THM_M_0841.ErdosStoneTarget",
        *PROOF_DECLARATIONS,
        DIFFERENTIAL_DECLARATION,
    ]
    assert receipt["recipe"] == recipe
    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["phase"] == "validation" and receipt["intent"] == "validate"
    assert receipt["verdict"] == "no_state_change"
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["selftest_status"] == "passed"
    assert receipt["selftest_result"] == {
        "exit_code": 0,
        "commands": [RECIPE_COMMAND],
    }
    assert receipt["release_grade"] is False and receipt["accepted_receipt_ids"] == []
    assert receipt["root_vector_before"] == receipt["root_vector_after"] == ROOT_VECTOR
    assert receipt["target"]["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert receipt["target"]["registry_denominator_sha256"] == DENOMINATOR_SHA256
    for name, expected in EXPECTED_INPUTS.items():
        assert receipt["inputs"][name] == expected, name
    for name in (
        "Validation.lean",
        "check_validation.py",
        "dependency-reuse-ledger.json",
        "validation-spec.json",
    ):
        assert receipt["inputs"][name] == sha256(HERE / name), name
    assert receipt["environment"]["platform"] == (
        f"{platform.system()} {platform.release()} {platform.machine()}"
    )
    assert receipt["environment"]["lean_executable_sha256"] == sha256(lean)
    assert receipt["environment"]["lake_executable_sha256"] == sha256(lake)
    assert receipt["environment"]["mathlib_revision"] == MATHLIB_REVISION
    assert receipt["environment"]["mathlib_tree"] == MATHLIB_TREE
    assert receipt["selected_provenance"]["origins"] == SOURCE_PROVENANCE
    assert receipt["result"]["lean_output_sha256"] == observation["lean_output_sha256"]
    assert receipt["result"]["trust_closure_observation"] == observation["closure"]
    assert receipt["result"]["narrow_kernel_replay"] == "pass_nonrelease"
    assert receipt["result"]["network_isolation"] == "pass_for_all_five_lean_invocations"
    assert receipt["result"]["proof_dependency_master_acceptance"] == "fail_closed"
    assert receipt["result"]["root_kernel_closed"] is False
    assert receipt["result"]["accepted_closed_obligation_ids"] == []
    assert receipt["result"]["open_root_cut_set"] == OPEN_ROOT_CUT
    assert receipt["result"]["complete_trust_provenance_gate"] == "fail_closed"
    assert receipt["result"]["hermetic_release_gate"] == "fail_closed"
    assert receipt["result"]["independent_distinct_runner_gate"] == "fail_closed"
    assert receipt["result"]["validation_phase_complete"] is False
    assert receipt["result"]["audit_complete"] is receipt["result"]["theorem_complete"] is False
    assert receipt["remaining_root_cut_set"] == OPEN_ROOT_CUT
    assert receipt["first_failed_gate"] == "dependency.S56-M-0841-PROOF.master_acceptance"
    assert blocker["first_failed_gate"] == receipt["first_failed_gate"]
    assert blocker["root_kernel_closed"] is blocker["theorem_complete"] is False
    assert blocker["validation_phase_complete"] is False
    assert receipt["changed_paths"] == blocker["changed_paths"] == CHANGED_PATHS

    if args.worker_packet is not None:
        packet = load(args.worker_packet.resolve())
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
        assert packet["changed_paths"] == CHANGED_PATHS
        assert packet["commands"] == receipt["commands"] == [RECIPE_COMMAND]
        assert packet["output_summary"] == receipt["output_summary"]
        assert packet["known_failures"] == receipt["known_failures"]
        status = git("status", "--short", "--untracked-files=all")
        actual = {
            line[3:]
            for line in status.splitlines()
            if line[3:] != "Formalizations/Lean/.lake"
        }
        assert actual == set(CHANGED_PATHS), (actual, set(CHANGED_PATHS))

    for relative in CHANGED_PATHS:
        assert_text_hygiene(ROOT / relative)
    for line in SUMMARY_LINES:
        print(line)


if __name__ == "__main__":
    main()
