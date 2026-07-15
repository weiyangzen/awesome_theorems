#!/usr/bin/env python3
"""Fail-closed release reconciliation for S56-M-0890-RELEASE."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile


if not __debug__:
    raise SystemExit("check_release.py requires Python assertions")


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0890"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM = "S56-M-0890-RELEASE"
THEOREM = "THM-M-0890"
BASE_REVISION = "471e4458269351ee096972776c478d019941b679"
BASE_TREE = "e30e1cefce39148420ccc4525b726d57f58ee94b"
TOOLCHAIN = "leanprover/lean4:v4.29.0"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
LEAN_SHA256 = "3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf"
LAKE_SHA256 = "a608ff084d7e2af228b92a29d7c2fd083ba0580e46889175ec74a81678c98359"
PYTHON_SHA256 = "b8d8288faefdd300201f43fcf00f6f539a27218eeed3a3dff5ab10b9c4c99700"
GIT_SHA256 = "5516c9f362c29376ab9a499a33082f9f611941d8c75930c880e30ad109e39c9a"
BWRAP_SHA256 = "0abea81db798ebf6b4742ac0664802d97521547a353c2a0dbdc21d76cbbfd2c0"
ELAN_LAKE_SHA256 = "840179e70803ef373c2ec53342d6a45ea7d022533e4145489fc1278b4f716385"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_REMOTE = "https://github.com/leanprover-community/mathlib4.git"
EXPRESSION_SHA256 = "512ebe658ca83b7fb4bb3d3565122d065e3bc6e589898b4f3cf74ab2e12ea54d"
DENOMINATOR_SHA256 = "259c6e160437f0fc2646c6f1e302441c3e129c6d3e70346d04438ea3f7a45169"
VALIDATION_RECEIPT_SHA256 = (
    "b4cdac35defe3b1d7ffef65383acd279a35b759d5089c9d56caac1daa8a07df1"
)
ROOT_VECTOR = {"H": "H1", "M": "M3", "R": "R4"}
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
EXPECTED_AXIOM_LIST = ["propext", "Classical.choice", "Quot.sound"]
INVENTORY_IDS = [
    "M0890-ROOT", "M0890-S-TARGET", "M0890-S-LEAST",
    "M0890-S-INDEPENDENCE", "M0890-S-BOUNDARY", "M0890-S-TRANSPORT",
    "M0890-S-FOUNDATION", "M0890-N-MAX-WITNESS", "M0890-N-LEAST-MIN",
    "M0890-L-LEAST-NEGATIVE", "M0890-N-DENOMINATOR",
    "M0890-L-REGULAR-ONES", "M0890-L-ONES-ORTHOGONAL",
    "M0890-C-HOFFMAN-MATRIX", "M0890-L-COMMON-EIGENBASIS",
    "M0890-L-HOFFMAN-PSD", "M0890-C-PRINCIPAL", "M0890-L-PSD-PRINCIPAL",
    "M0890-L-INDEPENDENT-ZERO", "M0890-T-RESTRICTED-FORM",
    "M0890-C-ONES-VECTOR", "M0890-L-QUADRATIC-EVAL",
    "M0890-B-ALPHA-POSITIVE", "M0890-L-SCALAR-ESTIMATE",
    "M0890-T-DIVISION-FREE", "M0890-T-ASSEMBLE", "M0890-X-MATHLIB",
    "M0890-X-SOURCE", "M0890-X-PROVENANCE", "M0890-X-EVIDENCE",
    "M0890-X-TRUST", "M0890-X-READABLE", "M0890-X-WORKFLOW",
]
UNRECONCILED_PARENT_IDS = [
    "M0890-N-DENOMINATOR", "M0890-L-LEAST-NEGATIVE",
    "M0890-L-SCALAR-ESTIMATE", "M0890-L-QUADRATIC-EVAL",
    "M0890-L-PSD-PRINCIPAL", "M0890-T-RESTRICTED-FORM",
    "M0890-C-PRINCIPAL", "M0890-L-HOFFMAN-PSD",
    "M0890-L-COMMON-EIGENBASIS", "M0890-B-ALPHA-POSITIVE",
]
PROOF_DECLARATIONS = (
    "Stage1Instances.THM_M_0890_Proof.leastAdjacencyEigenvalue_le_eigenvalue",
    "Stage1Instances.THM_M_0890_Proof.leastAdjacencyEigenvalue_neg",
    "Stage1Instances.THM_M_0890_Proof.denominatorPositive_proof",
    "Stage1Instances.THM_M_0890_Proof.shiftedAdjacency_posSemidef",
    "Stage1Instances.THM_M_0890_Proof.independentSet_adjacency_quadratic_zero",
    "Stage1Instances.THM_M_0890_Proof.independentSet_characteristic_norm",
    "Stage1Instances.THM_M_0890_Proof.regular_adjacency_mulVec_one",
    "Stage1Instances.THM_M_0890_Proof.independentSet_adjacency_one",
    "Stage1Instances.THM_M_0890_Proof.one_dotProduct_one_real",
    "Stage1Instances.THM_M_0890_Proof.centered_shifted_quadratic",
    "Stage1Instances.THM_M_0890_Proof.independentSet_scalar_nonnegative",
    "Stage1Instances.THM_M_0890_Proof.indepNum_pos",
    "Stage1Instances.THM_M_0890_Proof.maximumIndependentSetEstimate_proof",
    "Stage1Instances.THM_M_0890_Proof.divisionFreeInequality_proof",
    "Stage1Instances.THM_M_0890_Proof.ratioAssembly_proof",
    "Stage1Instances.THM_M_0890_Proof.hoffmanRatioBound_proof",
)
VALIDATION_DECLARATIONS = (
    "Stage1Instances.THM_M_0890_Validation.exactDivisionFreeReplay",
    "Stage1Instances.THM_M_0890_Validation.exactRootReplay",
)
EXPECTED_INPUTS = {
    "README.md": "d9da86725fec39f8aa1818f38cc78b31f77a00628e3c1d00409a6393aee3a01e",
    "Statement.lean": "beb6cbe0437f78f26188cc3ed1ebe82bed84d2a07f1f8ea1abd78468740a787f",
    "ObligationTree.lean": "6959e302e3676c172f1db7003014b56e153057f367ecaebb3b8c81a86bf27ff2",
    "Proof.lean": "b41705e275a454f9412a05b8f09b5be8701ff989840c7be216629824a5b08e68",
    "Validation.lean": "d61056333f26855318bce6ff50de8f71f133814c212bf56545a62880ab9bbdce",
    "instance.json": "030d142bc502f89b768709136ebac408d8fe02d2d779de272291944c0ada8101",
    "task-dag.json": "8540d20add89f3528bbf1d69969025828862dd3043d30eeae2f4db8890dd74c7",
    "statement.json": "dd9b94824f9f5e3a4f8627da05c132a69fcd18cdf476a11046d253ec4d78be21",
    "source-statement-crosswalk.md": "9d1bdd83df32c11c18262a16d5f20ce3e3ab29b2cd73b1e2e1efd14dee2bfebf",
    "anchor-audit.json": "b922f69cb16eed05e8f29f281460a928e787619a7c7f4c923ea312a1bf098549",
    "obligation-registry.json": "079b565a392e4e81e291e3bed8b45d4b6b77e51668a733bce7435b8c89857110",
    "typed-graphs.json": "8c9906787a3fe386d98ddef9442904ce43f63eeead34c15a4f17ca664eaf0903",
    "intake-receipt.json": "fef46633a7d18541a0d86cca82a89692916608723524192d0ec19c2ef2c95e08",
    "statement-receipt.json": "131c65a1eb57cfcada374b923ba00132c59e7c62cd7dc6cb3b4f852968d37086",
    "anchor-audit-receipt.json": "57867f698647a2dba7301f9327e1cbdcd0b11818f166671b67b89271d3797873",
    "obligation-tree-receipt.json": "07e2bd767a45a3225302aaf2ab9402d6aadfae9577fde19796adec63e0b442a8",
    "proof-receipt.json": "c78f5dac72be0e6e7eedeb1cd66b2d6ccb5a4df62634d859b9fc845328e76efa",
    "validation-spec.json": "d3070f767b6ece9ab23cd85eb419a783d20a768f64121311f1196d5b6fdb6949",
    "validation-receipt.json": VALIDATION_RECEIPT_SHA256,
    "check_validation.py": "59b3a21a9ea3af8b8d2ab13fd8a6be0c495e084b7eafbcf6359c4bef64a45917",
    "validation-phase.md": "83c311946a3227b5893870030acb1a772b8b98e142c18508da5eb46cb6f860bd",
}
EXPECTED_AUTHORITIES = {
    "Docs/Stage1_Blueprint_rev-5.6.md": "aef0b291a207679f4b78b8ffb1d625293e309dbaad1076a9d5c199804061b592",
    "Docs/Stage1_Targets_rev-5.6.json": "02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c",
    "Docs/Stage1_Execution_DAG_rev-5.6.json": "c77760eaaa01f64bf4fbfd6aabe72a44b874d04df5945102c0f363204198fe49",
    "Docs/Blueprint_Guidelines.md": "a06c07b5ca1b270b4935ad3dab893e9a0e078c29c8da2ef9dca1e71193310535",
    "skills/execute-stage1-rev56/SKILL.md": "26d47a66c6535feabb8bbf1051fd55d76a53fe761f4b3d953f86b97ec86152b8",
    "Formalizations/Lean/lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "Formalizations/Lean/lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
RELEASE_OUTPUTS = {
    "release-spec.json": "42b623192de887f71736845c71fce5c2d535fc889cf0acfc714c597b4d09a0ef",
    "release-decision.json": "2ce2ee4d556dd254dcee25d6ce212156446febafed5dcbbe1c952b4fc24f4797",
    "release-validation.md": "48e66ca23b5c37e6e93ffb7bf8c8f6dbd261f41c20ca54e599032e73185adb5c",
}
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/check_release.py",
    f"Stage1_Instances/{THEOREM}/release-decision.json",
    f"Stage1_Instances/{THEOREM}/release-receipt.json",
    f"Stage1_Instances/{THEOREM}/release-spec.json",
    f"Stage1_Instances/{THEOREM}/release-validation.md",
}
SUMMARY_LINES = [
    "PASS S56-M-0890-RELEASE reconciliation: authority, frozen inputs, and provisional receipts agree",
    "PASS current-base network-isolated replay: exact Hoffman root is sorry-free at trust zero with the recorded axiom ceiling",
    "BLOCKED S56-10.2-DEPENDENCY-ACCEPTANCE: validation is provisional and not master accepted",
    "BLOCKED accepted architecture: H1/M3/R4 remains open; ten internal composition plans have no accepted binding",
    "BLOCKED AUDIT-Z and THEOREM-Z: H0/R0, foundation, provenance, trust, and public-state reconciliation are absent",
    "BLOCKED release assurance: immutable cold/offline evidence, SBOM/archive, distinct runners, and minimal verifier are absent",
    "verdict=blocked lifecycle=planned audit_complete=false theorem_complete=false accepted_receipts=0",
]
KNOWN_FAILURES = [
    "S56-M-0890-VALIDATION and all transitive phase receipts remain provisional rather than dependency-ordered master accepted; the validation receipt is accepted=false and release_grade=false.",
    "The historical validation checker is correctly snapshot-bound to fd50bb07f6632a2ad0bdc17737c200432ee242c8 and rejects the current integrated release HEAD before Lean replay; its old recipe was not presented as fresh current-base evidence.",
    "A fresh current-base network-isolated trust-zero replay corroborates the exact root and eighteen sorry-free declarations with only propext, Classical.choice, and Quot.sound, but same-worker warm-cache corroboration is not accepted M0, E0/E1, or independent verification.",
    "The planned instance, task DAG, registry, and typed graph retain H1/M3/R4, root_closed=false, no accepted receipt or closed obligation, and ten source-architecture decompositions without accepted exact child-to-parent bindings.",
    "Pinpoint primary-source H0 remains unaccepted because the catalog Hoffman/1970 attribution conflicts with inspected modern history; no independently reviewed node-specific R0 reconstruction exists, so AUDIT-Z remains open.",
    "No accepted theorem-specific foundation profile or complete transitive declaration, proof-body, compiled-artifact, provenance, trust, TCB, computation, SBOM, license, and archive closure exists.",
    "The automation-provided shared warm .lake symlink was reused read-only, so this is not immutable clean input, an empty-cache cold build, offline restoration, or a deterministic content-addressed release bundle.",
    "No two distinct signed clean-runner attestations, independently implemented minimal verifier, protected adversarial CI, AUDIT-Z, THEOREM-Z, theorem completion, release, or master acceptance exists.",
]


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


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(
    argv: list[str], *, cwd: Path = ROOT, env: dict[str, str] | None = None,
    timeout: int = 600,
) -> str:
    result = subprocess.run(
        argv, cwd=cwd, env=env, text=True, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, timeout=timeout, check=False,
    )
    if result.returncode:
        raise RuntimeError(f"command failed ({result.returncode}): {argv!r}\n{result.stdout}")
    return result.stdout


HOME = os.environ["HOME"]
BASE_ENV = {
    "HOME": HOME,
    "PATH": f"{HOME}/.elan/bin:/usr/bin:/bin",
    "ELAN_TOOLCHAIN": TOOLCHAIN,
    "LANG": "C.UTF-8",
    "LC_ALL": "C.UTF-8",
    "TZ": "UTC",
    "LEAN_NUM_THREADS": "1",
}


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["/usr/bin/git", *args], cwd=cwd, env=BASE_ENV, timeout=60).strip()


def source_without_comments_and_strings(source: str) -> str:
    output: list[str] = []
    index = 0
    depth = 0
    in_string = False
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
        elif in_string:
            if char == "\\" and index + 1 < len(source):
                output.extend("  ")
                index += 2
            elif char == '"':
                in_string = False
                output.append(" ")
                index += 1
            else:
                output.append("\n" if char == "\n" else " ")
                index += 1
        elif pair == "/-":
            depth = 1
            output.extend("  ")
            index += 2
        elif pair == "--":
            while index < len(source) and source[index] != "\n":
                output.append(" ")
                index += 1
        elif char == '"':
            in_string = True
            output.append(" ")
            index += 1
        else:
            output.append(char)
            index += 1
    assert depth == 0 and not in_string
    return "".join(output)


def reported_axioms(output: str, declaration: str) -> set[str]:
    match = re.search(
        re.escape(f"'{declaration}' depends on axioms: [") + r"(.*?)]",
        output, re.DOTALL,
    )
    assert match is not None, f"missing axiom report: {declaration}"
    return {part.strip() for part in match.group(1).split(",") if part.strip()}


def assert_text_hygiene(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines()), path


def isolated_replay(lean: Path, lean_path: str) -> dict[str, object]:
    with tempfile.TemporaryDirectory(prefix="stage1-m0890-release-", dir="/tmp") as temp_name:
        temp = Path(temp_name).resolve()
        for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
            (temp / name).write_bytes((HERE / name).read_bytes())
        (temp / "home").mkdir()
        base = [
            "/usr/bin/bwrap", "--ro-bind", "/", "/", "--bind", str(temp), str(temp),
            "--dev", "/dev", "--proc", "/proc", "--unshare-net", "--die-with-parent",
            "--clearenv", "--setenv", "HOME", str(temp / "home"),
            "--setenv", "TMPDIR", str(temp), "--setenv", "LANG", "C.UTF-8",
            "--setenv", "LC_ALL", "C.UTF-8", "--setenv", "TZ", "UTC",
            "--setenv", "LEAN_NUM_THREADS", "1", "--chdir", str(temp),
        ]

        def lean_run(name: str, path: str) -> str:
            return run(base + [
                "--setenv", "LEAN_PATH", path, str(lean), "--trust=0", "-t0",
                "-o", name.replace(".lean", ".olean"), name,
            ])

        outputs: dict[str, object] = {}
        outputs["statement"] = lean_run("Statement.lean", lean_path)
        local_path = f"{temp}:{lean_path}"
        outputs["obligation_tree"] = lean_run("ObligationTree.lean", local_path)
        outputs["proof"] = lean_run("Proof.lean", local_path)
        outputs["validation"] = lean_run("Validation.lean", local_path)
        outputs["olean_sha256"] = {
            name: sha256(temp / name)
            for name in ("Statement.olean", "ObligationTree.olean", "Proof.olean", "Validation.olean")
        }
        return outputs


def replay_current_base() -> dict[str, object]:
    assert (LEAN_ROOT / ".lake").is_symlink()
    manifest = load(LEAN_ROOT / "lake-manifest.json")
    mathlib_entry = next(row for row in manifest["packages"] if row["name"] == "mathlib")
    assert mathlib_entry["rev"] == mathlib_entry["inputRev"] == MATHLIB_REVISION
    assert mathlib_entry["url"] == MATHLIB_REMOTE
    assert MATHLIB.resolve().is_dir()
    assert git("rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert git("remote", "get-url", "origin", cwd=MATHLIB) == MATHLIB_REMOTE
    assert git("status", "--porcelain=v1", "--untracked-files=all", cwd=MATHLIB) == ""

    launcher = Path(HOME) / ".elan/bin/lake"
    assert sha256(launcher) == ELAN_LAKE_SHA256
    lean = Path(run([str(launcher), "env", "which", "lean"], cwd=LEAN_ROOT, env=BASE_ENV).strip())
    lake = Path(run([str(launcher), "env", "which", "lake"], cwd=LEAN_ROOT, env=BASE_ENV).strip())
    assert sha256(lean) == LEAN_SHA256 and sha256(lake) == LAKE_SHA256
    assert sha256(Path("/usr/bin/python3").resolve()) == PYTHON_SHA256
    assert sha256(Path("/usr/bin/git")) == GIT_SHA256
    assert sha256(Path("/usr/bin/bwrap")) == BWRAP_SHA256
    lean_version = run([str(lean), "--version"], env=BASE_ENV)
    assert "4.29.0" in lean_version and LEAN_COMMIT in lean_version
    lean_path = run(
        [str(launcher), "env", "printenv", "LEAN_PATH"], cwd=LEAN_ROOT, env=BASE_ENV
    ).strip()

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by|run_tac)\b|"
        r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
        r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
        r"(?:axiom|constant|opaque|unsafe|extern)\b",
        re.MULTILINE,
    )
    for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
        source = source_without_comments_and_strings((HERE / name).read_text(encoding="utf-8"))
        assert prohibited.search(source) is None, f"prohibited Lean device in {name}"

    outputs = isolated_replay(lean, lean_path)
    proof_output = str(outputs["proof"])
    validation_output = str(outputs["validation"])
    for declaration in PROOF_DECLARATIONS:
        assert reported_axioms(proof_output + validation_output, declaration) == EXPECTED_AXIOMS
    for declaration in VALIDATION_DECLARATIONS:
        assert reported_axioms(validation_output, declaration) == EXPECTED_AXIOMS
    assert validation_output.count("Declarations are sorry-free!") == 18
    combined = "".join(str(outputs[key]) for key in (
        "statement", "obligation_tree", "proof", "validation"
    ))
    assert "sorryAx" not in combined and "declaration uses 'sorry'" not in combined
    closure_match = re.search(
        r"VALIDATION_CLOSURE declarations=(\d+) modules=(\d+)", validation_output
    )
    assert closure_match is not None
    assert "VALIDATION_CLOSURE axioms=[propext, Classical.choice, Quot.sound]" in validation_output
    assert "VALIDATION_CLOSURE unexpected_axioms=[]" in validation_output
    assert "VALIDATION_CLOSURE unsafe=[]" in validation_output
    return {
        "lean_output_sha256": {
            key: hashlib.sha256(str(outputs[key]).encode()).hexdigest()
            for key in ("statement", "obligation_tree", "proof", "validation")
        },
        "fresh_olean_sha256": outputs["olean_sha256"],
        "closure": {
            "declarations": int(closure_match.group(1)),
            "modules": int(closure_match.group(2)),
            "axioms": EXPECTED_AXIOM_LIST,
            "unexpected_axioms": [],
            "unsafe_declarations": [],
        },
    }


def main() -> None:
    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    for name, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"reconciled input drifted: {name}"
    for relative, expected in EXPECTED_AUTHORITIES.items():
        assert sha256(ROOT / relative) == expected, f"authority input drifted: {relative}"
    for name, expected in RELEASE_OUTPUTS.items():
        assert sha256(HERE / name) == expected, name

    targets = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    instance = load(HERE / "instance.json")
    tasks = load(HERE / "task-dag.json")
    statement = load(HERE / "statement.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    proof = load(HERE / "proof-receipt.json")
    validation = load(HERE / "validation-receipt.json")
    spec = load(HERE / "release-spec.json")
    decision = load(HERE / "release-decision.json")
    receipt = load(HERE / "release-receipt.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")

    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 1440 and target["baseline"] == "L0"
    assert target["rework_required"] is True and target["legacy_artifacts_accepted"] is False
    assert target["lifecycle_mode"] == "planned" and target["theorem_complete"] is False
    release_item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert release_item == {
        "id": ITEM, "theorem_id": THEOREM, "execution_rank": 1440,
        "phase": "release", "layer": 6, "state": "[ ]",
        "depends_on": ["S56-M-0890-VALIDATION"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Reconcile evidence and decide the exact theorem-completion verdict.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0, "children": [],
    }
    validation_item = next(
        row for row in execution["items"] if row["id"] == "S56-M-0890-VALIDATION"
    )
    assert validation_item["state"] == "[_]" and validation_item["attempts"] == 1
    local_task = next(row for row in tasks["tasks"] if row["id"] == ITEM)
    assert local_task["state"] == "open"
    assert local_task["depends_on"] == ["S56-M-0890-VALIDATION"]

    formal = statement["canonical_formal_target"]
    assert formal["declaration_or_expression"] == (
        "Stage1Instances.THM_M_0890.HoffmanRatioBoundTarget"
    )
    assert formal["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert registry["root_obligation_id"] == "M0890-ROOT"
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert registry["frozen_denominators"]["inventory"] == INVENTORY_IDS
    assert graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    closure = graphs["closure_boundary"]
    assert closure["closed_obligations"] == [] and closure["root_closed"] is False
    assert closure["accepted_root_machine_debt"] == "M3"
    assert closure["audit_complete"] is closure["theorem_complete"] is False
    assert [row["parent_obligation_id"] for row in graphs["unverified_decomposition_plans"]] == (
        UNRECONCILED_PARENT_IDS
    )

    assert instance["lifecycle"] == instance["lifecycle_mode"] == tasks["lifecycle"] == "planned"
    assert instance["root_vector"] == ROOT_VECTOR
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == []
    assert instance["audit_complete"] is instance["theorem_complete"] is False
    assert tasks["accepted_states"] == [] and all(row["state"] == "open" for row in tasks["tasks"])
    assert proof["accepted"] is False and proof["accepted_receipt_ids"] == []
    assert proof["accepted_closed_obligation_ids"] == []
    assert proof["result"]["root_kernel_closed"] is True
    assert proof["result"]["accepted_root_closed"] is proof["result"]["theorem_complete"] is False
    assert proof["unverified_internal_composition_count"] == 10

    assert sha256(HERE / "validation-receipt.json") == VALIDATION_RECEIPT_SHA256
    assert validation["support_state"] == "provisional_worker_selftest"
    assert validation["proposed_state"] == "[_]" and validation["verdict"] == "blocked"
    assert validation["accepted"] is validation["release_grade"] is False
    assert validation["accepted_receipt_ids"] == validation["accepted_closed_obligation_ids"] == []
    assert validation["result"]["exact_root_kernel_replay"] == "provisional_pass"
    assert validation["result"]["accepted_root_machine_debt"] == "M3"
    assert validation["result"]["accepted_root_closed"] is False
    assert validation["result"]["unreconciled_internal_composition_plans"] == 10
    assert validation["result"]["audit_complete"] is validation["result"]["theorem_complete"] is False
    assert validation["first_failed_gate"] == "dependency.S56-M-0890-PROOF.master_acceptance"

    assert decision["schema_version"] == "stage1-release-decision/1.0"
    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert decision["item_id"] == receipt["item_id"] == spec["item_id"] == packet["item_id"] == ITEM
    assert decision["theorem_id"] == receipt["theorem_id"] == spec["theorem_id"] == THEOREM
    assert decision["base_revision"] == receipt["base_revision"] == packet["base_revision"] == BASE_REVISION
    assert decision["base_tree"] == receipt["base_tree"] == BASE_TREE
    assert decision["proposed_state"] == receipt["proposed_state"] == packet["state"] == "[_]"
    assert decision["verdict"] == receipt["verdict"] == "blocked"
    assert decision["accepted"] is decision["release_grade"] is False
    assert receipt["accepted"] is receipt["release_grade"] is receipt["master_accepted"] is False
    assert decision["lifecycle_before"] == decision["lifecycle_after"] == "planned"
    assert decision["root_vector"]["accepted_before"] == ROOT_VECTOR
    assert decision["root_vector"]["accepted_after"] == ROOT_VECTOR
    assert decision["terminal_decisions"] == {
        "audit_complete": False, "theorem_complete": False,
        "audit_z": "blocked", "theorem_z": "blocked",
        "release_accepted": False, "master_acceptance": False,
    }
    assert decision["accepted_receipt_ids"] == receipt["accepted_receipt_ids"] == []
    assert decision["accepted_closed_obligation_ids"] == receipt["accepted_closed_obligation_ids"] == []
    assert decision["first_failed_gate"]["gate_id"] == "S56-10.2-DEPENDENCY-ACCEPTANCE"
    assert decision["first_failed_gate"]["dependency_gate"] == (
        "dependency.S56-M-0890-VALIDATION.master_acceptance"
    )
    assert decision["first_failed_release_gate"]["gate_id"] == (
        "S56-RELEASE-IMMUTABLE-CLEAN-INPUT"
    )
    assert decision["next_failed_release_gate"]["gate_id"] == (
        "S56-10.6-HERMETIC-COLD-EMPTY-CACHE"
    )
    assert decision["unreconciled_internal_composition_parent_ids"] == UNRECONCILED_PARENT_IDS
    assert receipt["dependency"]["receipt_sha256"] == VALIDATION_RECEIPT_SHA256
    assert receipt["dependency"]["accepted"] is receipt["dependency"]["release_grade"] is False
    assert receipt["decision_sha256"] == sha256(HERE / "release-decision.json")
    assert receipt["release_spec_sha256"] == sha256(HERE / "release-spec.json")
    assert receipt["public_projection_sha256"] == sha256(HERE / "release-validation.md")
    assert re.fullmatch(r"[0-9a-f]{64}", receipt["checker_sha256"])
    assert receipt["known_failures"] == decision["known_failures"] == packet["known_failures"] == KNOWN_FAILURES
    for relative, expected in receipt["input_bindings"].items():
        assert sha256(ROOT / relative) == expected, relative

    assert spec["schema_version"] == "stage1-release-recipe/1.0"
    assert spec["recipe_id"] == receipt["recipe"]["recipe_id"]
    assert spec["cwd"] == "." and spec["argv"] == [
        "/usr/bin/python3", "-I", "-B", f"Stage1_Instances/{THEOREM}/check_release.py"
    ]
    assert spec["network_policy"] == "denied" and spec["expected_exit"] == 0
    assert "--unshare-net" in spec["network_enforcement"]
    assert spec["covered_obligation_ids"] == INVENTORY_IDS
    assert spec["covered_decisions"] == ["AUDIT-Z", "THEOREM-Z"]
    assert receipt["recipe"] == spec

    observation = replay_current_base()
    assert receipt["result"]["lean_output_sha256"] == observation["lean_output_sha256"]
    assert receipt["result"]["fresh_olean_sha256"] == observation["fresh_olean_sha256"]
    assert receipt["result"]["transitive_environment_observation"] == observation["closure"]
    assert receipt["result"]["exact_root_kernel_replay"] == "provisional_pass_current_base"
    assert receipt["result"]["accepted_root_machine_debt"] == "M3"
    assert receipt["result"]["audit_complete"] is receipt["result"]["theorem_complete"] is False
    assert receipt["result"]["verdict"] == "blocked"

    assert set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert set(packet["changed_paths"]) == set(receipt["changed_paths"]) == CHANGED_PATHS
    assert packet["output_summary"] == "\n".join(SUMMARY_LINES)
    assert receipt["commands"] == packet["commands"]
    expected_stdout = "\n".join(SUMMARY_LINES) + "\n"
    assert receipt["output_evidence"]["stdout_semantic_sha256"] == hashlib.sha256(
        expected_stdout.encode()
    ).hexdigest()
    assert receipt["output_evidence"]["stdout_bytes"] == len(expected_stdout.encode())
    assert receipt["output_evidence"]["expected_line_count"] == len(SUMMARY_LINES)
    assert all(
        set(row) == {"command", "exit_code", "result"}
        and isinstance(row["exit_code"], int) and isinstance(row["result"], str)
        for row in packet["commands"]
    )
    actual = {
        line[3:] for line in git("status", "--short", "--untracked-files=all").splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual == CHANGED_PATHS, (actual, CHANGED_PATHS)
    for relative in CHANGED_PATHS:
        assert_text_hygiene(ROOT / relative)
    for path in (
        HERE / "release-decision.json", HERE / "release-receipt.json",
        HERE / "release-validation.md",
    ):
        text = path.read_text(encoding="utf-8")
        assert "/home/" not in text and ".cron/" not in text
        assert "theorem_complete=true" not in text

    print("\n".join(SUMMARY_LINES))


if __name__ == "__main__":
    main()
