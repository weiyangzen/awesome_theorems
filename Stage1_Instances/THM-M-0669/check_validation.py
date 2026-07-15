#!/usr/bin/env python3
"""Fail-closed narrow validator for S56-M-0669-VALIDATION."""

from __future__ import annotations

import argparse
from datetime import datetime
import hashlib
import json
import os
from pathlib import Path
import platform
import re
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0669"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
ITEM = "S56-M-0669-VALIDATION"
THEOREM = "THM-M-0669"
BASE_REVISION = "443b8bbc23bf35a1e7a4bb7b3183073f76bbee2b"
BASE_TREE = "c5771c47c12b80aba613e6d844570f83b39ded6d"
TOOLCHAIN = "leanprover/lean4:v4.29.0"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
LEAN_SHA256 = "3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf"
BWRAP_SHA256 = "0abea81db798ebf6b4742ac0664802d97521547a353c2a0dbdc21d76cbbfd2c0"
PYTHON_SHA256 = "b8d8288faefdd300201f43fcf00f6f539a27218eeed3a3dff5ab10b9c4c99700"
GIT_SHA256 = "5516c9f362c29376ab9a499a33082f9f611941d8c75930c880e30ad109e39c9a"
TOOLCHAIN_SHA256 = "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2"
MANIFEST_SHA256 = "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_REMOTE = "https://github.com/leanprover-community/mathlib4.git"
MATHLIB_LICENSE_SHA256 = "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1"
STATEMENT_EXPRESSION_SHA256 = (
    "91efc0e7986951efbb4f667a73f31de3eae2f0221d397c37c13a303f3769badd"
)
DENOMINATOR_SHA256 = "9ec85645aa13399fb7dd6255e1cb66f90fc3694c536f6a282a6b30f19173afb4"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
ROOT_VECTOR = {"H": "H1", "M": "M3", "R": "R3"}
PROVISIONAL_IDS = ["M0669-C-BOOLEAN"]
PARTIAL_IDS = ["M0669-C-ATOMIC", "M0669-I-FORMULA", "M0669-T-ASSEMBLE"]
OPEN_ROOT_CUT = [
    "M0669-E-ONE-VAR",
    "M0669-E-SIGN",
    "M0669-E-ROOTS",
    "M0669-E-PROJECT",
    "M0669-E-SEMANTICS",
    "M0669-I-FORMULA",
    "M0669-T-ASSEMBLE",
    "M0669-ROOT",
]
EXPECTED_INPUTS = {
    "Statement.lean": "09836be630efcb735336dc3d18c2e74e83ec73b5c6237c13be1b8b8fa85f2a7a",
    "ObligationTree.lean": "ff86db4e034849d69e37b6d42683f7a21f64238455f4f8cc41bf622fb25ada4d",
    "Proof.lean": "23e739dcbc773c25d4536360fad54e27d0625bcd416875e73cc2210eb6bd2f58",
    "Validation.lean": "4b749e634675c3f9151bc8dbc85d59dd68840d2b572bf47da94b68c2cdbe138e",
    "statement.json": "c6db83b8be055f729b3c01079c08515a120b417cf61db286fd59d34afe11c0fe",
    "anchor-audit.json": "ff03d190345cf872b4bd401f1286537120a8057e4bc0fe6b2eb8c67fb1e82af3",
    "obligation-registry.json": "305e5f67aad487e60f74aa076e63a69d65db599a112b81a21ea909d5b24b9bcb",
    "typed-graphs.json": "ca58a855e548c6f6cf377853c231a95664095c21a875b1a887b3dbe525ee23f8",
    "validation-specs.json": "563f1578dbf4f48b7b5b2ff602db957f2ea303bceca95285147b1577e4cd3022",
    "proof-receipt.json": "51139b89515843ce137ed0b9a8219d2e9d7551fa1c7d4957cff2f72a1b0c6e18",
    "proof-blocker.json": "477e6ade1f847397cd6aad67ff779363ebdeb57e20568d79c968457e44f43993",
    "proof-validation.md": "1dbffd5ca29f4f15fbf62ff2839854d9a3df758d3873215442ffa5af93833a15",
    "source-statement-crosswalk.md": "93484f91b05cfdf9728dab42adeeca522f40fdfc329e30bf0e32da0940535416",
    "check_anchor_audit.py": "9eb8b8e2340cc295a9c32ef884f9caa53eba762368d6c34f107ebf10efc36001",
    "check_obligation_tree.py": "8f6c75b1b1ae9495e242336a1f14c45bad723b76332cd4caf49ca31a9c4d9ed1",
    "check_proof.sh": "2cff331a88c74c2f372aaccfd4c511d81d33b803a7b470de1156f95f70598aa6",
}
SOURCE_BOUNDARIES = {
    "Mathlib/ModelTheory/Algebra/Ring/Basic.lean": {
        "blob": "343f4032178407863604818f910c09a48cc1b5f2",
        "source_sha256": "d28d06c2bcdf51932a8220b7601fc6a4be88301935b551f5542c5dea0fcdb8bb",
        "olean_sha256": "e33d219af606d2f7d8b4a794432bda4e44ed1e9499cfe25bd439a1730e3ee71e",
        "olean_bytes": 331984,
    },
    "Mathlib/ModelTheory/Complexity.lean": {
        "blob": "88f2d680cc352fb256e68bbb3b0ca177126fc32f",
        "source_sha256": "964dfdd62c781341a0e3b9b081200751b68c0c8e0db5388641d80af274fd93d3",
        "olean_sha256": "266b86e720169a3aecff812d45452c94b6818132abd7bf50dbdd4358dc9ae88d",
        "olean_bytes": 1477680,
    },
    "Mathlib/Data/Real/Basic.lean": {
        "blob": "9b462066ead4a4298f2faf62f29681073d2fdc8d",
        "source_sha256": "04aedda6369b441837667a1997d62e64a5070e10f2c0d89309edd0f40903d0a9",
        "olean_sha256": "f8805658052bff6e1ad140c9fdfab740e53110be260a04e27eda2dfc45032c90",
        "olean_bytes": 353560,
    },
    "Mathlib/ModelTheory/Algebra/Ring/FreeCommRing.lean": {
        "blob": "804fbd743e1a2dda4a2ec83f3586932252a3024a",
        "source_sha256": "4edc1051a9d020a21307816ddc1a2612d8d07a7d261784fd06c65933217d37cd",
        "olean_sha256": "0cc591ad32bd76544142e9530da93917258a8c01b0fe84a3c24058c770eafa32",
        "olean_bytes": 59584,
    },
}
PROOF_DECLARATIONS = (
    "Stage1.THM_M_0669.qfEquivalent_of_isQF",
    "Stage1.THM_M_0669.atomicEqualityNormalization",
    "Stage1.THM_M_0669.realize_polynomialOfTerm",
    "Stage1.THM_M_0669.atomicPolynomialNormalization",
    "Stage1.THM_M_0669.qfBooleanClosure",
    "Stage1.THM_M_0669.formulaElimination_of_oneVariable",
    "Stage1.THM_M_0669.tarskiQuantifierElimination_of_oneVariable",
)
VALIDATION_DECLARATIONS = (
    "Stage1.THM_M_0669.Validation.validation_realize_polynomialOfTerm",
    "Stage1.THM_M_0669.Validation.validationAtomicPolynomialNormalization",
    "Stage1.THM_M_0669.Validation.validationQfBooleanClosure",
    "Stage1.THM_M_0669.Validation.validationFormulaElimination",
    "Stage1.THM_M_0669.Validation.validationConditionalRoot",
)
MUTATION_DECLARATIONS = (
    "Stage1.THM_M_0669.mutationRemovedTheory",
    "Stage1.THM_M_0669.mutationChangedDomain",
    "Stage1.THM_M_0669.mutationChangedBinderScope",
    "Stage1.THM_M_0669.mutationExcludesEmptyVariables",
)
COVERED_IDS = [
    "M0669-S-THEORY",
    "M0669-C-ATOMIC",
    "M0669-C-BOOLEAN",
    "M0669-I-FORMULA",
    "M0669-T-ASSEMBLE",
    "M0669-X-PROVENANCE",
]
COVERED_DECLARATIONS = [
    "Stage1.THM_M_0669.TarskiQuantifierEliminationTarget",
    *PROOF_DECLARATIONS,
    *VALIDATION_DECLARATIONS,
]
SCOPE_BOUNDARY = (
    "Network-isolated trust-zero warm worker replay of the exact statement, all "
    "proof-phase partial bodies and conditional compositions, selected direct pinned "
    "provenance, and same-worker no-import differential atomic, Boolean, recursion, "
    "and conditional-root checks. The one-variable real-closed-field elimination "
    "package, exact root, accepted foundation and complete trust/provenance closure, "
    "cold hermetic reproduction, and distinct-runner independent verification remain "
    "fail-closed."
)
CHANGED_PATHS = [
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/Validation.lean",
    f"Stage1_Instances/{THEOREM}/check_validation.py",
    f"Stage1_Instances/{THEOREM}/validation-phase.md",
    f"Stage1_Instances/{THEOREM}/validation-receipt.json",
    f"Stage1_Instances/{THEOREM}/validation-spec.json",
]
SUMMARY_LINES = [
    "PASS narrow kernel replay: exact statement, seven proof-phase declarations, and five no-import differential declarations elaborated at trust zero",
    "PASS trust observation: checked declarations use only propext, Classical.choice, and Quot.sound; differential closure has no bodyless nonaxiom or unsafe declaration",
    "PASS selected provenance: frozen local hashes, four mathlib source/olean boundaries, executable pins, license, and tracked-clean pinned revision agree",
    "OPEN exact root: one-variable real-closed-field elimination and its sign, roots, projection, and semantics bodies remain absent at M3",
    "FAIL CLOSED complete trust/provenance: proof acceptance, accepted foundation policy, serialized transitive closure, and full TCB/SBOM inventory are absent",
    "FAIL CLOSED release gates: root Lake resolution is blocked by an incomplete pinned package, the shared warm cache is not cold hermetic evidence, and this worker is not a distinct independent verifier",
]
COMMAND_ARGV = {
    "standard": ["python3", "Docs/tools/check_stage1_standard.py"],
    "target_check": ["python3", "scripts/stage1_target.py", "check"],
    "target_show": ["python3", "scripts/stage1_target.py", "show", THEOREM],
    "anchor": ["python3", f"Stage1_Instances/{THEOREM}/check_anchor_audit.py"],
    "tree": ["python3", f"Stage1_Instances/{THEOREM}/check_obligation_tree.py"],
    "validation": [
        "python3", "-I", "-B", f"Stage1_Instances/{THEOREM}/check_validation.py",
        "--worker-packet", ".stage1-worker-selftest.json",
    ],
    "spec_json": [
        "python3", "-m", "json.tool",
        f"Stage1_Instances/{THEOREM}/validation-spec.json",
    ],
    "receipt_json": [
        "python3", "-m", "json.tool",
        f"Stage1_Instances/{THEOREM}/validation-receipt.json",
    ],
    "packet_json": ["python3", "-m", "json.tool", ".stage1-worker-selftest.json"],
    "diff": [
        "git", "diff", "--check", "--", f"Stage1_Instances/{THEOREM}",
        ".stage1-worker-selftest.json",
    ],
}

if not __debug__:
    raise RuntimeError("validation requires Python assertions; optimized mode is forbidden")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


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


HOME = os.environ["HOME"]
BASE_ENV = {
    "HOME": HOME,
    "PATH": f"{HOME}/.elan/bin:/usr/bin:/bin",
    "LANG": "C.UTF-8",
    "LC_ALL": "C.UTF-8",
    "TZ": "UTC",
    "LEAN_NUM_THREADS": "1",
}


def run(
    argv: list[str], *, cwd: Path = ROOT, env: dict[str, str] | None = None,
    timeout: int = 600,
) -> str:
    result = subprocess.run(
        argv, cwd=cwd, env=env, text=True, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, timeout=timeout, check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(f"command failed ({result.returncode}): {argv!r}\n{result.stdout}")
    return result.stdout


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["/usr/bin/git", *args], cwd=cwd, env=BASE_ENV).strip()


def source_without_comments(source: str) -> str:
    """Remove nested Lean comments and line comments before supplemental scans."""
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
    no_axioms = f"'{declaration}' does not depend on any axioms"
    pattern = re.compile(
        re.escape(f"'{declaration}' depends on axioms: [") + r"(.*?)]",
        re.DOTALL,
    )
    matches = pattern.findall(output)
    assert output.count(no_axioms) + len(matches) == 1, declaration
    if not matches:
        return set()
    return {part.strip() for part in matches[0].split(",") if part.strip()}


def assert_text_hygiene(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())


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
    return ":".join([
        str(local), *(str(path) for path in roots),
        str(lean.parent.parent / "lib/lean"),
    ])


def isolated_replay(lean: Path, bwrap: Path, lean_path: str) -> dict[str, str]:
    with tempfile.TemporaryDirectory(prefix="stage1-m0669-validation-", dir="/tmp") as tmp_name:
        tmp = Path(tmp_name).resolve()
        for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
            (tmp / name).write_bytes((HERE / name).read_bytes())
        (tmp / "home").mkdir()
        base = [
            str(bwrap), "--ro-bind", "/", "/", "--bind", str(tmp), str(tmp),
            "--dev", "/dev", "--proc", "/proc", "--unshare-net",
            "--die-with-parent", "--clearenv", "--setenv", "HOME", str(tmp / "home"),
            "--setenv", "TMPDIR", str(tmp), "--setenv", "LANG", "C.UTF-8",
            "--setenv", "LC_ALL", "C.UTF-8", "--setenv", "TZ", "UTC",
            "--setenv", "LEAN_NUM_THREADS", "1", "--chdir", str(tmp),
        ]

        def lean_run(name: str, module_path: str, emit_olean: bool) -> str:
            argv = base + [
                "--setenv", "LEAN_PATH", module_path, str(lean), "--trust=0", "-t0",
            ]
            if emit_olean:
                argv += ["-o", name.replace(".lean", ".olean")]
            argv.append(name)
            return run(argv)

        module_path = f"{tmp}:{lean_path}"
        return {
            "statement": lean_run("Statement.lean", lean_path, True),
            "obligation_tree": lean_run("ObligationTree.lean", module_path, True),
            "proof": lean_run("Proof.lean", module_path, False),
            "validation": lean_run("Validation.lean", module_path, False),
        }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--probe", action="store_true")
    parser.add_argument("--worker-packet", type=Path)
    args = parser.parse_args()

    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    targets = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    statement = load(HERE / "statement.json")
    anchor = load(HERE / "anchor-audit.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    frozen_specs = load(HERE / "validation-specs.json")
    proof_receipt = load(HERE / "proof-receipt.json")
    proof_blocker = load(HERE / "proof-blocker.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 713 and target["baseline"] == "L0"
    assert target["lifecycle_mode"] == "planned"
    assert target["rework_required"] is True and target["theorem_complete"] is False
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 713,
        "phase": "validation",
        "layer": 5,
        "state": "[ ]",
        "depends_on": ["S56-M-0669-PROOF"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Run hermetic kernel, trust, provenance, and independent validation gates.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    predecessor = next(row for row in execution["items"] if row["id"] == "S56-M-0669-PROOF")
    assert predecessor["state"] == "[_]" and predecessor["attempts"] == 1

    for name, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"stale validation input: {name}"
    assert sha256(LEAN_ROOT / "lean-toolchain") == TOOLCHAIN_SHA256
    assert sha256(LEAN_ROOT / "lake-manifest.json") == MANIFEST_SHA256
    formal = statement["canonical_formal_target"]
    assert formal["declaration_or_expression"] == (
        "Stage1.THM_M_0669.TarskiQuantifierEliminationTarget"
    )
    assert formal["elaborated_expression_sha256"] == STATEMENT_EXPRESSION_SHA256
    assert formal["statement_file_sha256"] == EXPECTED_INPUTS["Statement.lean"]
    assert registry["root_obligation_id"] == graphs["root_node_id"] == "M0669-ROOT"
    assert registry["denominator_sha256"] == (
        graphs["registry_denominator_sha256"]
    ) == DENOMINATOR_SHA256
    ids = [row["obligation_id"] for row in registry["obligations"]]
    assert len(ids) == len(set(ids)) == 14
    assert registry["frozen_denominators"]["inventory"] == ids
    assert {row["obligation_id"] for row in frozen_specs["recipes"]} == set(ids)
    root = next(node for node in graphs["nodes"] if node["obligation_id"] == "M0669-ROOT")
    assert {
        "H": root["human_debt"],
        "M": root["machine_debt"],
        "R": root["readability_debt"],
    } == ROOT_VECTOR
    closure = graphs["closure_boundary"]
    assert closure["root_closed"] is closure["theorem_complete"] is False
    assert closure["root_machine_classification"] == "M3"

    assert anchor["canonical_target"] == formal["declaration_or_expression"]
    assert anchor["root_machine_debt"] == "M3"
    assert anchor["theorem_proved"] is anchor["theorem_complete"] is False
    assert proof_receipt["item_id"] == "S56-M-0669-PROOF"
    assert proof_receipt["support_state"] == "provisional_worker_selftest"
    assert proof_receipt["accepted"] is False
    assert proof_receipt["proof_body"]["source_sha256"] == EXPECTED_INPUTS["Proof.lean"]
    assert proof_receipt["provisionally_closed_obligation_ids"] == PROVISIONAL_IDS
    assert proof_receipt["partial_progress_toward_obligation_ids"] == PARTIAL_IDS
    assert proof_receipt["accepted_closed_obligation_ids"] == []
    assert proof_receipt["result"]["root_closed"] is False
    assert proof_receipt["result"]["theorem_complete"] is False
    assert proof_blocker["remaining_root_cut_set"] == OPEN_ROOT_CUT
    assert proof_blocker["root_closed"] is proof_blocker["theorem_complete"] is False

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by|run_tac)\b|"
        r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
        r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
        r"(?:axiom|constant|opaque|unsafe|extern)\b",
        flags=re.MULTILINE,
    )
    all_source = "\n".join(
        source_without_comments((HERE / name).read_text(encoding="utf-8"))
        for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean")
    )
    assert prohibited.search(all_source) is None
    validation = (HERE / "Validation.lean").read_text(encoding="utf-8")
    imports = validation.split("/-!", 1)[0]
    assert "import Proof" not in imports and "import ObligationTree" not in imports
    for fragment in (
        "theorem validationAtomicPolynomialNormalization",
        "theorem validationQfBooleanClosure",
        "def ValidationOneVariableElimination : Prop",
        "theorem validationFormulaElimination",
        "theorem validationConditionalRoot",
        "(oneVariable : ValidationOneVariableElimination)",
        "assert_no_sorry validationConditionalRoot",
        "#print_validation_closure",
    ):
        assert fragment in validation, fragment
    assert re.search(r"theorem\s+validationConditionalRoot\s*:", validation) is None

    manifest = load(LEAN_ROOT / "lake-manifest.json")
    mathlib_entry = next(row for row in manifest["packages"] if row["name"] == "mathlib")
    assert mathlib_entry["rev"] == mathlib_entry["inputRev"] == MATHLIB_REVISION
    assert mathlib_entry["url"] == MATHLIB_REMOTE
    assert (LEAN_ROOT / ".lake").is_symlink()
    mathlib = (LEAN_ROOT / ".lake/packages/mathlib").resolve()
    flt_regular = (LEAN_ROOT / ".lake/packages/flt-regular").resolve()
    assert flt_regular.is_dir()
    flt_head = subprocess.run(
        ["/usr/bin/git", "rev-parse", "--verify", "HEAD"],
        cwd=flt_regular,
        env=BASE_ENV,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=30,
        check=False,
    )
    assert flt_head.returncode != 0
    assert "Needed a single revision" in flt_head.stdout
    assert git("rev-parse", "HEAD", cwd=mathlib) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == MATHLIB_TREE
    assert git("diff", "--quiet", "--ignore-submodules", "--", cwd=mathlib) == ""
    assert git("diff", "--cached", "--quiet", "--ignore-submodules", "--", cwd=mathlib) == ""
    assert git("remote", "get-url", "origin", cwd=mathlib) == MATHLIB_REMOTE
    assert sha256(mathlib / "LICENSE") == MATHLIB_LICENSE_SHA256
    for relative, expected in SOURCE_BOUNDARIES.items():
        source = mathlib / relative
        olean = mathlib / ".lake/build/lib/lean" / Path(relative).with_suffix(".olean")
        assert git("rev-parse", f"HEAD:{relative}", cwd=mathlib) == expected["blob"]
        assert sha256(source) == expected["source_sha256"]
        assert sha256(olean) == expected["olean_sha256"]
        assert olean.stat().st_size == expected["olean_bytes"]

    toolchain_key = TOOLCHAIN.replace("/", "--").replace(":", "---")
    lean = Path(HOME) / ".elan/toolchains" / toolchain_key / "bin/lean"
    bwrap = Path("/usr/bin/bwrap")
    python = Path("/usr/bin/python3").resolve()
    git_executable = Path("/usr/bin/git").resolve()
    assert sha256(lean) == LEAN_SHA256
    assert sha256(bwrap) == BWRAP_SHA256 and sha256(python) == PYTHON_SHA256
    assert sha256(git_executable) == GIT_SHA256
    assert LEAN_COMMIT in run([str(lean), "--version"], env=BASE_ENV)

    outputs = isolated_replay(lean, bwrap, pinned_lean_path(lean))
    combined = "\n".join(outputs.values())
    assert "sorryAx" not in combined
    assert all("error:" not in output for output in outputs.values())
    canonical_marker = (
        "def Stage1.THM_M_0669.TarskiQuantifierEliminationTarget : Prop :=\n"
    )
    assert canonical_marker in outputs["statement"]
    canonical_expression = outputs["statement"].split(canonical_marker, 1)[1].strip()
    assert hashlib.sha256(canonical_expression.encode()).hexdigest() == (
        STATEMENT_EXPRESSION_SHA256
    )
    mutation_source = (HERE / "Statement.lean").read_text(encoding="utf-8")
    root_print = "#print Stage1.THM_M_0669.TarskiQuantifierEliminationTarget"
    mutation_outputs: dict[str, str] = {}
    with tempfile.TemporaryDirectory(
        prefix="stage1-m0669-mutations-", dir="/tmp"
    ) as mutation_tmp_name:
        mutation_tmp = Path(mutation_tmp_name).resolve()
        (mutation_tmp / "home").mkdir()
        for declaration in MUTATION_DECLARATIONS:
            short = declaration.rsplit(".", 1)[1]
            source_path = mutation_tmp / f"{short}.lean"
            source_path.write_text(
                mutation_source.replace(root_print, f"#print {declaration}"),
                encoding="utf-8",
            )
            mutation_output = run([
                str(bwrap), "--ro-bind", "/", "/", "--bind",
                str(mutation_tmp), str(mutation_tmp), "--dev", "/dev",
                "--proc", "/proc", "--unshare-net", "--die-with-parent",
                "--clearenv", "--setenv", "HOME", str(mutation_tmp / "home"),
                "--setenv", "TMPDIR", str(mutation_tmp), "--setenv", "LANG",
                "C.UTF-8", "--setenv", "LC_ALL", "C.UTF-8", "--setenv", "TZ",
                "UTC", "--setenv", "LEAN_NUM_THREADS", "1", "--setenv",
                "LEAN_PATH", pinned_lean_path(lean), "--chdir", str(mutation_tmp),
                str(lean), "--trust=0", "-t0", source_path.name,
            ])
            marker = f"def {declaration} : Prop :=\n"
            assert marker in mutation_output
            expression = mutation_output.split(marker, 1)[1].strip()
            assert expression != canonical_expression, declaration
            mutation_outputs[declaration] = mutation_output
    for declaration in PROOF_DECLARATIONS:
        assert reported_axioms(outputs["proof"], declaration) <= EXPECTED_AXIOMS
    for declaration in VALIDATION_DECLARATIONS:
        assert reported_axioms(outputs["validation"], declaration) <= EXPECTED_AXIOMS
    assert outputs["validation"].count("Declarations are sorry-free!") == 5
    closure_match = re.search(
        r"VALIDATION_CLOSURE declarations=(\d+) modules=(\d+)",
        outputs["validation"],
    )
    assert closure_match is not None
    assert (
        "VALIDATION_CLOSURE axioms=[propext, Classical.choice, Quot.sound]"
        in outputs["validation"]
    )
    assert "VALIDATION_CLOSURE bodyless_nonaxioms=[]" in outputs["validation"]
    assert "VALIDATION_CLOSURE unsafe=[]" in outputs["validation"]
    observation = {
        "lean_output_sha256": {
            name: hashlib.sha256(output.encode()).hexdigest()
            for name, output in outputs.items()
        },
        "observed_axioms": sorted(EXPECTED_AXIOMS),
        "validation_closure": {
            "declarations": int(closure_match.group(1)),
            "modules": int(closure_match.group(2)),
            "bodyless_nonaxioms": [],
            "unsafe_declarations": [],
        },
        "mutation_output_sha256": {
            name: hashlib.sha256(output.encode()).hexdigest()
            for name, output in mutation_outputs.items()
        },
    }
    if args.probe:
        print(json.dumps(observation, sort_keys=True))
        return

    spec = load(HERE / "validation-spec.json")
    receipt = load(HERE / "validation-receipt.json")
    assert spec["schema_version"] == "stage1-validation-spec/1.0"
    assert spec["item_id"] == receipt["item_id"] == ITEM
    assert spec["theorem_id"] == receipt["theorem_id"] == THEOREM
    assert receipt["depends_on"] == ["S56-M-0669-PROOF"]
    assert spec["recipe_id"] == "S56-M-0669-VALIDATION-narrow-v1"
    assert spec["argv"] == [
        "python3", "-I", "-B", f"Stage1_Instances/{THEOREM}/check_validation.py",
        "--worker-packet", ".stage1-worker-selftest.json",
    ]
    assert receipt["recipe"]["argv"] == spec["argv"]
    assert receipt["recipe"]["cwd"] == spec["cwd"] == "."
    assert receipt["recipe"]["timeout_seconds"] == spec["timeout_seconds"] == 600
    assert receipt["recipe"]["network_policy"] == spec["network_policy"] == (
        "outer_validator_no_network_operations; all_lean_subprocesses_denied"
    )
    assert receipt["recipe"]["env_allowlist"] == spec["env_allowlist"]
    assert spec["expected_exit"] == receipt["recipe"]["expected_exit"] == 0
    assert spec["expected_outputs"] == receipt["recipe"]["expected_outputs"]
    assert spec["covered_obligation_ids"] == (
        receipt["recipe"]["covered_obligation_ids"]
    ) == COVERED_IDS
    assert spec["covered_declarations"] == (
        receipt["recipe"]["covered_declarations"]
    ) == COVERED_DECLARATIONS
    assert spec["scope_boundary"] == receipt["recipe"]["scope_boundary"] == SCOPE_BOUNDARY

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["phase"] == "validation" and receipt["intent"] == "validate"
    assert receipt["verdict"] == "blocked"
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["release_grade"] is False
    assert receipt["lifecycle_before"] == receipt["lifecycle_after"] == "planned"
    assert receipt["root_vector_before"] == receipt["root_vector_after"] == ROOT_VECTOR
    assert receipt["accepted_receipt_ids"] == []
    started = datetime.fromisoformat(receipt["validation_started_at"])
    ended = datetime.fromisoformat(receipt["validation_ended_at"])
    validated = datetime.fromisoformat(receipt["validated_at"])
    assert started < ended == validated
    assert started.utcoffset() is not None and ended.utcoffset() is not None
    command_argv = [row["argv"] for row in receipt["commands"]]
    assert command_argv == [
        COMMAND_ARGV["standard"], COMMAND_ARGV["target_check"],
        COMMAND_ARGV["target_show"], COMMAND_ARGV["anchor"],
        COMMAND_ARGV["tree"], COMMAND_ARGV["validation"],
        COMMAND_ARGV["spec_json"], COMMAND_ARGV["receipt_json"],
        COMMAND_ARGV["packet_json"], COMMAND_ARGV["diff"],
    ]
    assert all(row["cwd"] == "." and row["exit_code"] == 0 for row in receipt["commands"])
    for key in (
        "repository_state", "environment", "direct_provenance", "trust",
        "hermeticity", "independent_validation", "result", "commands",
        "output_evidence", "known_failures", "freshness", "invalidation_inputs",
    ):
        assert key in receipt
    repository_state = receipt["repository_state"]
    assert repository_state["release_clean"] is False
    assert repository_state["tracked_patch_sha256"] == hashlib.sha256(b"").hexdigest()
    assert repository_state["tracked_patch_bytes"] == 0
    input_payload = [
        {"path": relative, "sha256": sha256(ROOT / relative)}
        for relative in (
            f"Stage1_Instances/{THEOREM}/Validation.lean",
            f"Stage1_Instances/{THEOREM}/check_validation.py",
            f"Stage1_Instances/{THEOREM}/validation-phase.md",
            f"Stage1_Instances/{THEOREM}/validation-spec.json",
        )
    ]
    assert repository_state["untracked_input_sha256"] == hashlib.sha256(
        json.dumps(input_payload, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    assert repository_state["untracked_input_scope"] == [row["path"] for row in input_payload]
    assert repository_state["preexisting_untracked_lake_symlink_target_sha256"] == (
        hashlib.sha256(os.readlink(LEAN_ROOT / ".lake").encode()).hexdigest()
    )
    for name, expected in EXPECTED_INPUTS.items():
        assert receipt["inputs"][name] == expected, name
    assert receipt["inputs"]["validation-spec.json"] == sha256(HERE / "validation-spec.json")
    assert receipt["inputs"]["check_validation.py"] == sha256(Path(__file__).resolve())
    assert receipt["target"]["elaborated_expression_sha256"] == STATEMENT_EXPRESSION_SHA256
    assert receipt["target"]["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert receipt["environment"]["platform"] == (
        f"{platform.system()} {platform.release()} {platform.machine()}"
    )
    assert receipt["environment"]["lean_executable_sha256"] == sha256(lean)
    assert receipt["environment"]["bubblewrap_executable_sha256"] == sha256(bwrap)
    assert receipt["environment"]["python_executable_sha256"] == sha256(python)
    assert receipt["environment"]["git_executable_sha256"] == sha256(git_executable)
    result = receipt["result"]
    assert result["lean_output_sha256"] == observation["lean_output_sha256"]
    assert result["observed_axioms"] == observation["observed_axioms"]
    assert result["validation_closure"] == observation["validation_closure"]
    assert result["mutation_output_sha256"] == observation["mutation_output_sha256"]
    assert result["validated_provisional_obligation_ids"] == PROVISIONAL_IDS
    assert result["validated_partial_progress_ids"] == PARTIAL_IDS
    assert result["accepted_closed_obligation_ids"] == []
    assert result["proof_dependency_master_acceptance"] == "fail_closed"
    assert result["root_closed"] is result["root_kernel_closed"] is False
    assert result["root_machine_debt"] == "M3"
    assert result["provisional_remaining_machine_chain"] == OPEN_ROOT_CUT
    assert result["complete_trust_provenance_gate"] == "fail_closed"
    assert result["hermetic_release_gate"] == "fail_closed"
    assert result["independent_distinct_runner_gate"] == "fail_closed"
    assert result["audit_complete"] is result["theorem_complete"] is False
    assert receipt["direct_provenance"]["proof_dependency_master_accepted"] is False
    assert receipt["trust"]["accepted_foundation_profile"] is False
    assert receipt["trust"]["complete_transitive_trust_closure"] is False
    assert receipt["hermeticity"]["fresh_clean_checkout"] is False
    assert receipt["hermeticity"]["empty_user_package_and_build_caches"] is False
    assert receipt["hermeticity"]["cold_dependency_rebuild"] is False
    assert receipt["hermeticity"]["decision"].startswith("fail_closed")
    assert receipt["independent_validation"]["distinct_verifier_identity"] is False
    assert receipt["independent_validation"]["independently_provisioned_clean_runner"] is False
    assert receipt["independent_validation"]["second_signed_attestation"] is False
    assert receipt["independent_validation"]["decision"] == "fail_closed"
    assert receipt["freshness"]["support_state"] == "provisional_nonrelease_worker_evidence"
    assert receipt["freshness"]["revocation_state"] == "unaccepted"
    assert receipt["known_failures"] and receipt["invalidation_inputs"]
    assert receipt["provisional_remaining_machine_chain"] == OPEN_ROOT_CUT
    assert receipt["authoritative_graph_first_open_cut"] == closure["first_open_cut"]
    assert receipt["first_failed_gate"] == "dependency.S56-M-0669-PROOF.master_acceptance"
    assert receipt["first_failed_theorem_gate"] == "M0669-E-ONE-VAR.root_closure"
    expected_stdout = ("\n".join(SUMMARY_LINES) + "\n").encode()
    assert receipt["output_evidence"]["stdout_semantic_sha256"] == hashlib.sha256(
        expected_stdout
    ).hexdigest()
    assert receipt["output_evidence"]["expected_line_count"] == len(SUMMARY_LINES)
    assert receipt["output_evidence"]["exit_code"] == 0
    assert receipt["changed_paths"] == CHANGED_PATHS

    if args.worker_packet is not None:
        packet = load(args.worker_packet.resolve())
        assert set(packet) == {
            "item_id", "changed_paths", "commands", "output_summary",
            "base_revision", "known_failures", "state",
        }
        assert packet["item_id"] == ITEM and packet["state"] == "[_]"
        assert packet["base_revision"] == BASE_REVISION
        assert packet["changed_paths"] == receipt["changed_paths"] == CHANGED_PATHS
        assert packet["commands"] == receipt["commands"]
        assert packet["output_summary"] == receipt["output_summary"]
        assert packet["known_failures"] == receipt["known_failures"]
        status = git("status", "--short", "--untracked-files=all")
        actual = {
            line[3:] for line in status.splitlines()
            if line[3:] != "Formalizations/Lean/.lake"
        }
        assert actual == set(CHANGED_PATHS), (actual, set(CHANGED_PATHS))

    for relative in CHANGED_PATHS:
        assert_text_hygiene(ROOT / relative)
    for line in SUMMARY_LINES:
        print(line)


if __name__ == "__main__":
    main()
