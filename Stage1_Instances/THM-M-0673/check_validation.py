#!/usr/bin/env python3
"""Fail-closed validation for S56-M-0673-VALIDATION."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM = "S56-M-0673-VALIDATION"
THEOREM = "THM-M-0673"
BASE_REVISION = "c887c8e5d7afe589d4b90386654421a60e998f51"
BASE_TREE = "7a1298612a32286e2a542ffc410cf4de9bb1fabd"
PROOF_BASE = "310be814cb307a91263e232acf691a6b3eded70e"
TREE_BASE = "f3b9f5fc99b4675558801fcc47f610b046eb5d14"
EXPRESSION_SHA256 = "3b541698da0e2b40d0cef5ea0f03ebd62538d330293e4e393ce053e000906cba"
DENOMINATOR_SHA256 = "4266ee40d8be778685c48d8781aab55dd6d57301e7d9ded13523ea4353c58fe6"
REGISTRY_SHA256 = "aefa3236248ea7500e3dd48e01e953f978f8425c78ac11103364ce9cabce3e77"
TOOLCHAIN_SHA256 = "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2"
MANIFEST_SHA256 = "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81"
LEAN_SHA256 = "3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf"
LAKE_SHA256 = "a608ff084d7e2af228b92a29d7c2fd083ba0580e46889175ec74a81678c98359"
BWRAP_SHA256 = "0abea81db798ebf6b4742ac0664802d97521547a353c2a0dbdc21d76cbbfd2c0"
PYTHON_SHA256 = "b8d8288faefdd300201f43fcf00f6f539a27218eeed3a3dff5ab10b9c4c99700"
GIT_SHA256 = "5516c9f362c29376ab9a499a33082f9f611941d8c75930c880e30ad109e39c9a"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_REMOTE = "https://github.com/leanprover-community/mathlib4.git"
MATHLIB_SOURCE = "ba32a045647e55dee5bc5b4534ede125eb6cc7bef523aec77dea5e980dfacd54"
MATHLIB_BLOB = "8c436697c7c071261251d3369b70e3882d46673a"
MATHLIB_OLEAN = "1ee005283e38f3d6a64eb931f3452702a4a9ba33e2fc850ef48cf665008e2865"
MATHLIB_LICENSE = "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1"
BOUNDED_BODY = "89d7f530554a721ab6431f151ecee1f8a2e5c4c21f71e47d38ba39bc4320f0bf"
SENTENCE_BODY = "77fb5684a9cc762a6b3c0a563cd28b6c27cd5a7b76f767cb21605a8130956746"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
ROOT_VECTOR = {"H": "H1", "M": "M3", "R": "R4"}
OBSERVED_IDS = [
    "M0673-ROOT", "M0673-T-ADAPTER", "M0673-A-SENTENCE",
    "M0673-A-FORMULA", "M0673-A-BOUNDED",
]
SOURCE_MAPPED_IDS = [
    "M0673-B-FALSUM", "M0673-B-EQUALITY", "M0673-B-RELATION",
    "M0673-B-IMPLICATION", "M0673-B-UNIVERSAL", "M0673-T-TERM",
    "M0673-C-PRESTRUCTURE", "M0673-L-FUNMAP", "M0673-L-QUOT-EQ",
    "M0673-L-QUOT-REL", "M0673-L-ULTRAFILTER-IMP",
    "M0673-L-QUOT-FORALL", "M0673-T-SNOC", "M0673-C-EPSILON",
    "M0673-L-EVENTUAL-SET",
]
GRAPH_CUT = [
    "M0673-A-BOUNDED", "M0673-S-FOUNDATION", "M0673-X-SOURCE",
    "M0673-X-PROVENANCE", "M0673-X-TRUST", "M0673-X-READABLE",
    "M0673-X-WORKFLOW",
]
EXPECTED_INPUTS = {
    "instance.json": "c24eb53d67563203d997de2a068bda05cbef1aa56ab76826c6e93455b4798029",
    "Statement.lean": "131cab45507a3d3c7249d02f52f8cfbaf9d7b1c004a542e24f1bdb36be9ca424",
    "ObligationTree.lean": "11ffc582120eb2d6ca0dffdbd602c52a136f6970c7d1a56246bd00a4c99e6714",
    "Proof.lean": "cacb2a7f66bdeca3823b154e31d6a891d89a1751e78cf4cb73d20ef5b61a28fa",
    "Validation.lean": "faa7e299b8a90bef6fe554a3b15659c944bcfedd47e12f90d9fe42725e9122a3",
    "statement.json": "81468c229e682d4a3490c4275caa5dcbbc55b598a48d5e93bab1ae9b2016170e",
    "anchor-audit.json": "81b0bdc3e507f19efa0c51f0aee86de4d2d31e0360c5b8454dc76e4e4e4e3350",
    "obligation-registry.json": "2c5af493b744470bfcf09feb9fb4c13bbdff20ed434799b0d2c34e6db8fbfbb0",
    "typed-graphs.json": "7bd03ea0943661d43a4c02c0b711998f50a786bbb744412ba7cc4d557ce581fb",
    "validation-specs.json": "0d2c46e6da48e5ade1a7cad6a6526ac34385acfa035868be591f1d8bd2f3ba42",
    "proof-receipt.json": "b9e7a86f93d0ebf46860fb20207e480463639b9202b81ece262a875d5ea51f62",
    "proof-validation.md": "8ef27f93c6c0dc52f240e8b587718f0af81cc12eecbfdf0fde60df80d1fe683c",
    "check_proof.sh": "b07099cfe335c8274f68e7ba1d0ad28697bd39fd240d3dc70ffeaa0840921867",
    "validation-spec.json": "a9ed7c9ddc61f9fb00ba0cd5497d7b4c49d85fc7c1511583a0c73d1a835974e8",
    "validation-phase.md": "139b63e4af6812ec280c3313fafa1ebba32bfe2b3c48a9531fc272c441a6afca",
}
PROOF_DECLARATIONS = (
    "FirstOrder.Language.Ultraproduct.funMap_cast",
    "FirstOrder.Language.Ultraproduct.term_realize_cast",
    "FirstOrder.Language.Ultraproduct.boundedFormula_realize_cast",
    "FirstOrder.Language.Ultraproduct.realize_formula_cast",
    "FirstOrder.Language.Ultraproduct.sentence_realize",
    "Stage1Instances.THM_M_0673_Proof.boundedFormulaRealize_pinned",
    "Stage1Instances.THM_M_0673_Proof.formulaRealize_via_frozen",
    "Stage1Instances.THM_M_0673_Proof.sentenceRealize_via_frozen",
    "Stage1Instances.THM_M_0673_Proof.terminalRoot_via_frozen",
    "Stage1Instances.THM_M_0673_Proof.losSentence_via_frozen",
    "Stage1Instances.THM_M_0673_Proof.losSentence_pinned",
)
VALIDATION_DECLARATIONS = (
    "FirstOrder.Language.Ultraproduct.funMap_cast",
    "FirstOrder.Language.Ultraproduct.term_realize_cast",
    "FirstOrder.Language.Ultraproduct.boundedFormula_realize_cast",
    "FirstOrder.Language.Ultraproduct.realize_formula_cast",
    "FirstOrder.Language.Ultraproduct.sentence_realize",
    "Stage1Instances.THM_M_0673.principal_boundary",
    "Stage1Instances.THM_M_0673.Validation.independentlyReconstructedRoot",
)
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/Validation.lean",
    f"Stage1_Instances/{THEOREM}/check_validation.py",
    f"Stage1_Instances/{THEOREM}/validation-phase.md",
    f"Stage1_Instances/{THEOREM}/validation-receipt.json",
    f"Stage1_Instances/{THEOREM}/validation-spec.json",
}
SUMMARY_LINES = [
    "PASS narrow kernel replay: exact statement, frozen composition, proof roots, and no-import differential root elaborated at trust zero",
    "PASS trust observation: all checked declarations use only propext, Classical.choice, and Quot.sound; proof and differential closures have no bodyless nonaxiom or unsafe declaration",
    "PASS selected provenance: local hashes, terminal body hashes, mathlib source/blob/olean/license, clean immutable pin, and executable identities agree",
    "FAIL CLOSED recorded obligation recipes: all 28 share a checker bound to the historical obligation-tree snapshot and current-HEAD replay exits at that freshness assertion",
    "BLOCKED node acceptance: the proof prerequisite is provisional and unaccepted; authoritative accepted state remains H1/M3/R4 with an empty closure",
    "FAIL CLOSED complete trust and hermeticity: no accepted foundation/TCB/SBOM or clean cold empty-cache offline replay exists",
    "FAIL CLOSED independent verification: the separate adapter shares this worker, checkout, toolchain, and warm cache",
]

if not __debug__:
    raise RuntimeError("validation requires Python assertions; optimized mode is forbidden")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def load(path: Path) -> dict:
    def reject_duplicates(pairs: list[tuple[str, object]]) -> dict:
        value: dict[str, object] = {}
        for key, item in pairs:
            assert key not in value, f"duplicate JSON key in {path}: {key}"
            value[key] = item
        return value

    value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates)
    assert isinstance(value, dict), path
    return value


def run(
    argv: list[str], *, cwd: Path = ROOT, env: dict[str, str] | None = None,
    timeout: int = 600, require_success: bool = True,
) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        argv, cwd=cwd, env=env, text=True, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, timeout=timeout, check=False,
    )
    if require_success and result.returncode != 0:
        raise RuntimeError(f"command failed ({result.returncode}): {argv!r}\n{result.stdout}")
    return result


BASE_ENV = {
    "HOME": os.environ["HOME"],
    "PATH": f"{os.environ['HOME']}/.elan/bin:/usr/bin:/bin",
    "LANG": "C.UTF-8",
    "LC_ALL": "C.UTF-8",
    "TZ": "UTC",
    "LEAN_NUM_THREADS": "1",
}


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["/usr/bin/git", *args], cwd=cwd, env=BASE_ENV).stdout.strip()


def source_without_comments_and_strings(source: str) -> str:
    output: list[str] = []
    index = 0
    depth = 0
    quoted = False
    escaped = False
    while index < len(source):
        pair = source[index:index + 2]
        char = source[index]
        if depth:
            if pair == "/-":
                depth += 1
                output.extend("  ")
                index += 2
            elif pair == "-/":
                depth -= 1
                output.extend("  ")
                index += 2
            else:
                output.append("\n" if char == "\n" else " ")
                index += 1
        elif quoted:
            output.append("\n" if char == "\n" else " ")
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                quoted = False
            index += 1
        elif pair == "/-":
            depth = 1
            output.extend("  ")
            index += 2
        elif pair == "--":
            newline = source.find("\n", index)
            newline = len(source) if newline < 0 else newline
            output.extend(" " * (newline - index))
            index = newline
        elif char == '"':
            quoted = True
            output.append(" ")
            index += 1
        else:
            output.append(char)
            index += 1
    assert depth == 0 and not quoted
    return "".join(output)


def reported_axioms(output: str, declaration: str) -> set[str]:
    pattern = re.compile(
        re.escape(f"'{declaration}' depends on axioms: [") + r"(.*?)]",
        re.DOTALL,
    )
    matches = pattern.findall(output)
    assert len(matches) == 1, f"missing or duplicate axiom report: {declaration}"
    return {part.strip() for part in matches[0].split(",") if part.strip()}


def assert_text_hygiene(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines()), path


def pinned_lean_path(lean: Path) -> str:
    package_names = (
        "batteries", "Qq", "aesop", "proofwidgets", "importGraph",
        "LeanSearchClient", "plausible", "mathlib",
    )
    roots = [
        (LEAN_ROOT / ".lake/packages" / name / ".lake/build/lib/lean").resolve()
        for name in package_names
    ]
    assert all(path.is_dir() for path in roots)
    local = (LEAN_ROOT / ".lake/build/lib/lean").resolve()
    assert local.is_dir()
    return ":".join([str(local), *(str(path) for path in roots), str(lean.parent.parent / "lib/lean")])


def isolated_replay(lean: Path, bwrap: Path, lean_path: str) -> dict[str, str]:
    with tempfile.TemporaryDirectory(prefix="stage1-m0673-validation-", dir="/tmp") as name:
        tmp = Path(name).resolve()
        for source in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
            (tmp / source).write_bytes((HERE / source).read_bytes())
        (tmp / "home").mkdir()
        base = [
            str(bwrap), "--ro-bind", "/", "/", "--bind", str(tmp), str(tmp),
            "--dev", "/dev", "--proc", "/proc", "--unshare-net",
            "--die-with-parent", "--clearenv", "--setenv", "HOME", str(tmp / "home"),
            "--setenv", "TMPDIR", str(tmp), "--setenv", "LANG", "C.UTF-8",
            "--setenv", "LC_ALL", "C.UTF-8", "--setenv", "TZ", "UTC",
            "--setenv", "LEAN_NUM_THREADS", "1", "--chdir", str(tmp),
        ]

        def lean_run(source: str, module_path: str, emit_olean: bool) -> str:
            argv = base + [
                "--setenv", "LEAN_PATH", module_path, str(lean), "--trust=0", "-t0",
                "--root", str(tmp),
            ]
            if emit_olean:
                argv += ["-o", source.replace(".lean", ".olean")]
            argv.append(source)
            return run(argv).stdout

        modules = f"{tmp}:{lean_path}"
        return {
            "statement": lean_run("Statement.lean", lean_path, True),
            "obligation_tree": lean_run("ObligationTree.lean", modules, True),
            "proof": lean_run("Proof.lean", modules, False),
            "validation": lean_run("Validation.lean", modules, False),
        }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--probe", action="store_true")
    parser.add_argument("--worker-packet", type=Path)
    args = parser.parse_args()

    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    targets = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    instance = load(HERE / "instance.json")
    task_dag = load(HERE / "task-dag.json")
    statement = load(HERE / "statement.json")
    anchor = load(HERE / "anchor-audit.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    frozen_specs = load(HERE / "validation-specs.json")
    spec = load(HERE / "validation-spec.json")
    proof_receipt = load(HERE / "proof-receipt.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    assert run(["/usr/bin/git", "merge-base", "--is-ancestor", PROOF_BASE, "HEAD"]).returncode == 0
    assert run(["/usr/bin/git", "merge-base", "--is-ancestor", TREE_BASE, "HEAD"]).returncode == 0
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 717 and target["baseline"] == "L0"
    assert target["lifecycle_mode"] == "planned"
    assert target["rework_required"] is True and target["theorem_complete"] is False
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item == {
        "id": ITEM, "theorem_id": THEOREM, "execution_rank": 717,
        "phase": "validation", "layer": 5, "state": "[ ]",
        "depends_on": ["S56-M-0673-PROOF"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Run hermetic kernel, trust, provenance, and independent validation gates.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0, "children": [],
    }
    predecessor = next(row for row in execution["items"] if row["id"] == "S56-M-0673-PROOF")
    assert predecessor["state"] == "[_]" and predecessor["attempts"] == 1

    for filename, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / filename) == expected, f"stale validation input: {filename}"
    formal = statement["canonical_formal_target"]
    assert formal["declaration_or_expression"] == "Stage1Instances.THM_M_0673.LosSentenceTarget"
    assert formal["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert formal["statement_file_sha256"] == EXPECTED_INPUTS["Statement.lean"]
    assert registry["root_obligation_id"] == graphs["root_obligation_id"] == "M0673-ROOT"
    assert registry["denominator_sha256"] == graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert registry["registry_sha256"] == graphs["registry_sha256"] == REGISTRY_SHA256
    assert registry["frozen_denominators"]["required_machine"] == OBSERVED_IDS + SOURCE_MAPPED_IDS
    closure = graphs["closure_boundary"]
    assert closure["accepted_closed_obligations"] == []
    assert closure["root_closed"] is closure["audit_complete"] is closure["theorem_complete"] is False
    assert closure["root_machine_debt"] == "M3" and closure["remaining_root_cut_set"] == GRAPH_CUT
    assert instance["root_vector"] == ROOT_VECTOR
    assert instance["accepted_proof_state"] == []
    assert instance["audit_complete"] is instance["theorem_complete"] is False
    local_validation = next(row for row in task_dag["tasks"] if row["id"] == ITEM)
    assert local_validation["state"] == "open" and task_dag["accepted_states"] == []

    assert proof_receipt["item_id"] == "S56-M-0673-PROOF"
    assert proof_receipt["base_revision"] == PROOF_BASE
    assert proof_receipt["accepted"] is False and proof_receipt["proposed_state"] == "[_]"
    assert proof_receipt["canonical_target"]["expression_sha256"] == EXPRESSION_SHA256
    assert proof_receipt["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert proof_receipt["registry_sha256"] == REGISTRY_SHA256
    assert proof_receipt["proof_body"]["source_sha256"] == EXPECTED_INPUTS["Proof.lean"]
    assert proof_receipt["kernel_inhabited_obligation_ids_observed"] == OBSERVED_IDS
    assert proof_receipt["source_mapped_not_individually_closed_ids"] == SOURCE_MAPPED_IDS
    assert proof_receipt["accepted_closed_obligation_ids"] == []
    assert proof_receipt["result"]["root_kernel_inhabitant_observed"] is True
    assert proof_receipt["result"]["accepted_root_closed"] is False
    assert proof_receipt["result"]["theorem_complete"] is False

    assert spec["schema_version"] == "stage1-validation-spec/1.0"
    assert spec["item_id"] == ITEM and spec["theorem_id"] == THEOREM
    assert spec["depends_on"] == ["S56-M-0673-PROOF"] and len(spec["recipes"]) == 1
    recipe = spec["recipes"][0]
    assert recipe["argv"][-3:] == [
        "Stage1_Instances/THM-M-0673/check_validation.py",
        "--worker-packet", ".stage1-worker-selftest.json",
    ]
    assert recipe["network_policy"] == "denied" and recipe["expected_exit"] == 0
    assert recipe["covered_obligation_ids"] == OBSERVED_IDS
    historical = spec["historical_recipe_policy"]
    assert historical["recipe_count"] == len(frozen_specs["recipes"]) == 28
    assert {tuple(row["argv"]) for row in frozen_specs["recipes"]} == {
        tuple(historical["shared_argv"])
    }

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by|run_tac|oracle)\b|"
        r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
        r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
        r"(?:axiom|constant|opaque|unsafe|extern)\b", re.MULTILINE,
    )
    sources = ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean")
    clean_source = {
        name: source_without_comments_and_strings((HERE / name).read_text(encoding="utf-8"))
        for name in sources
    }
    assert prohibited.search("\n".join(clean_source.values())) is None
    imports = (HERE / "Validation.lean").read_text(encoding="utf-8").split("/-!", 1)[0]
    assert "import Proof" not in imports and "import ObligationTree" not in imports
    assert "FirstOrder.Language.Ultraproduct.sentence_realize phi" in clean_source["Validation.lean"]
    assert "#print_validation_closure" in clean_source["Validation.lean"]

    assert sha256(LEAN_ROOT / "lean-toolchain") == TOOLCHAIN_SHA256
    assert sha256(LEAN_ROOT / "lake-manifest.json") == MANIFEST_SHA256
    manifest = load(LEAN_ROOT / "lake-manifest.json")
    mathlib_entry = next(row for row in manifest["packages"] if row["name"] == "mathlib")
    assert mathlib_entry["rev"] == mathlib_entry["inputRev"] == MATHLIB_REVISION
    assert mathlib_entry["url"] == MATHLIB_REMOTE
    assert (LEAN_ROOT / ".lake").is_symlink() and MATHLIB.resolve().is_dir()
    assert len(manifest["packages"]) == 11
    for package in manifest["packages"]:
        directory = package["name"].removeprefix("«").removesuffix("»")
        checkout = (LEAN_ROOT / ".lake/packages" / directory).resolve()
        assert checkout.is_dir(), directory
        assert git("rev-parse", "HEAD", cwd=checkout) == package["rev"], directory
        assert git("status", "--porcelain=v1", "--untracked-files=all", cwd=checkout) == "", directory
    assert git("rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert git("remote", "get-url", "origin", cwd=MATHLIB) == MATHLIB_REMOTE
    assert git("status", "--porcelain=v1", "--untracked-files=all", cwd=MATHLIB) == ""
    source = MATHLIB / "Mathlib/ModelTheory/Ultraproducts.lean"
    olean = MATHLIB / ".lake/build/lib/lean/Mathlib/ModelTheory/Ultraproducts.olean"
    assert git("rev-parse", "HEAD:Mathlib/ModelTheory/Ultraproducts.lean", cwd=MATHLIB) == MATHLIB_BLOB
    assert sha256(source) == MATHLIB_SOURCE and sha256(olean) == MATHLIB_OLEAN
    assert olean.stat().st_size == 50344 and sha256(MATHLIB / "LICENSE") == MATHLIB_LICENSE
    source_lines = source.read_bytes().splitlines(keepends=True)
    assert sha256_bytes(b"".join(source_lines[93:144])) == BOUNDED_BODY
    assert sha256_bytes(b"".join(source_lines[151:158])) == SENTENCE_BODY

    toolchain_root = Path(os.environ["HOME"]) / ".elan/toolchains/leanprover--lean4---v4.29.0"
    lean = toolchain_root / "bin/lean"
    lake = toolchain_root / "bin/lake"
    bwrap = Path("/usr/bin/bwrap")
    assert sha256(lean) == LEAN_SHA256 and sha256(lake) == LAKE_SHA256
    assert sha256(bwrap) == BWRAP_SHA256
    assert sha256(Path("/usr/bin/python3")) == PYTHON_SHA256
    assert sha256(Path("/usr/bin/git")) == GIT_SHA256
    lean_path = pinned_lean_path(lean)
    outputs = isolated_replay(lean, bwrap, lean_path)
    for declaration in PROOF_DECLARATIONS:
        assert reported_axioms(outputs["proof"], declaration) == EXPECTED_AXIOMS
    for declaration in VALIDATION_DECLARATIONS:
        assert reported_axioms(outputs["validation"], declaration) == EXPECTED_AXIOMS
    assert outputs["proof"].count("Declarations are sorry-free!") >= 1
    assert outputs["validation"].count("Declarations are sorry-free!") >= 1
    assert "PROOF_CLOSURE declarations=5088 modules=192" in outputs["proof"]
    assert "PROOF_CLOSURE bodyless_nonaxioms=[]" in outputs["proof"]
    assert "PROOF_CLOSURE unsafe=[]" in outputs["proof"]
    assert "VALIDATION_CLOSURE declarations=5086 modules=191" in outputs["validation"]
    assert "VALIDATION_CLOSURE bodyless_nonaxioms=[]" in outputs["validation"]
    assert "VALIDATION_CLOSURE unsafe=[]" in outputs["validation"]
    assert "sorryAx" not in "".join(outputs.values())
    assert "error:" not in "".join(outputs.values())

    historical_run = run(
        historical["shared_argv"], cwd=ROOT, env=BASE_ENV, require_success=False,
    )
    assert historical_run.returncode != 0
    assert "AssertionError" in historical_run.stdout
    assert "output(\"git\", \"rev-parse\", \"HEAD\") == BASE_REVISION" in historical_run.stdout

    if args.probe:
        for line in SUMMARY_LINES:
            print(line)
        return

    assert args.worker_packet is not None
    receipt = load(HERE / "validation-receipt.json")
    packet = load((ROOT / args.worker_packet).resolve())
    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["verdict"] == "blocked" and receipt["release_grade"] is False
    assert receipt["target"]["canonical_target_expression_sha256"] == EXPRESSION_SHA256
    assert receipt["target"]["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert receipt["inputs"] == {
        **EXPECTED_INPUTS,
        "check_validation.py": sha256(Path(__file__)),
    }
    assert receipt["recipe"] == recipe
    result = receipt["result"]
    assert result["root_kernel_inhabitant_observed"] is True
    assert result["accepted_root_closed"] is False
    assert result["accepted_closed_obligation_ids"] == []
    assert result["observed_axioms"] == ["propext", "Classical.choice", "Quot.sound"]
    assert result["proof_closure"] == {
        "declarations": 5088, "modules": 192,
        "bodyless_nonaxioms": [], "unsafe_declarations": [],
    }
    assert result["validation_closure"] == {
        "declarations": 5086, "modules": 191,
        "bodyless_nonaxioms": [], "unsafe_declarations": [],
    }
    assert result["lean_output_sha256"] == {
        name: sha256_bytes(output.encode()) for name, output in outputs.items()
    }
    assert result["recorded_obligation_recipe_replay"] == "fail_closed_historical_base_binding"
    assert result["audit_complete"] is result["theorem_complete"] is False
    assert receipt["output_evidence"]["stdout_semantic_sha256"] == sha256_bytes(
        ("\n".join(SUMMARY_LINES) + "\n").encode()
    )
    assert receipt["first_failed_gate"] == "dependency.S56-M-0673-PROOF.master_acceptance"
    assert receipt["first_failed_validation_gate"] == "validation_specs.current_head_snapshot_binding"
    assert receipt["first_failed_release_gate"] == "hermetic.cold_empty_cache_offline_replay"
    assert receipt["root_vector_before"] == receipt["root_vector_after"] == ROOT_VECTOR
    assert receipt["accepted_receipt_ids"] == []
    assert receipt["environment"]["manifest_materialization"] == (
        "all 11 git packages rechecked at their exact manifest revisions with clean worktrees"
    )
    assert receipt["provenance"]["origin"]["source_sha256"] == sha256(source)
    assert receipt["provenance"]["origin"]["compiled_module_sha256"] == sha256(olean)
    assert receipt["provenance"]["transitive_trust_closure_hash"] is None
    assert receipt["trust"]["accepted_foundation_profile"] is False
    assert receipt["trust"]["complete_transitive_trust_closure"] is False
    assert receipt["hermeticity"]["decision"] == "fail_closed_nonrelease_warm_cache_replay"
    assert receipt["independent_validation"]["decision"] == "fail_closed"
    assert set(receipt["changed_paths"]) == CHANGED_PATHS
    assert packet == {
        "item_id": ITEM,
        "changed_paths": receipt["changed_paths"],
        "commands": receipt["commands"],
        "output_summary": receipt["output_summary"],
        "base_revision": BASE_REVISION,
        "known_failures": receipt["known_failures"],
        "state": "[_]",
    }
    status = git("status", "--short", "--untracked-files=all")
    actual = {
        line[3:] for line in status.splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual == CHANGED_PATHS
    for relative in CHANGED_PATHS:
        assert_text_hygiene(ROOT / relative)

    for line in SUMMARY_LINES:
        print(line)


if __name__ == "__main__":
    main()
