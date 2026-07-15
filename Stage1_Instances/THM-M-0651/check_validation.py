#!/usr/bin/env python3
"""Fail-closed narrow validator for S56-M-0651-VALIDATION."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import re
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0651"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
ITEM = "S56-M-0651-VALIDATION"
THEOREM = "THM-M-0651"
BASE_REVISION = "9254a0ec0d0c71b346ae15a911721409e3ab3139"
BASE_TREE = "a3de0086d55c8f209894b07409deeeed04c393a3"
TOOLCHAIN = "leanprover/lean4:v4.29.0"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
LEAN_SHA256 = "3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf"
LAKE_SHA256 = "a608ff084d7e2af228b92a29d7c2fd083ba0580e46889175ec74a81678c98359"
BWRAP_SHA256 = "0abea81db798ebf6b4742ac0664802d97521547a353c2a0dbdc21d76cbbfd2c0"
PYTHON_SHA256 = "b8d8288faefdd300201f43fcf00f6f539a27218eeed3a3dff5ab10b9c4c99700"
GIT_SHA256 = "5516c9f362c29376ab9a499a33082f9f611941d8c75930c880e30ad109e39c9a"
ELAN_LAUNCHER_SHA256 = "840179e70803ef373c2ec53342d6a45ea7d022533e4145489fc1278b4f716385"
TOOLCHAIN_SHA256 = "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2"
MANIFEST_SHA256 = "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_REMOTE = "https://github.com/leanprover-community/mathlib4.git"
MATHLIB_LICENSE_SHA256 = "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1"
STATEMENT_EXPRESSION_SHA256 = (
    "789c281a89ba5947476cb2189ae3e216de0eeaa0b5d016549489d8c1553d8c43"
)
DENOMINATOR_SHA256 = "e739a3f3ee963205d34582d0879d767e928e26670f557de0871addcc176f3805"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
ROOT_VECTOR = {"H": "H1", "M": "M4", "R": "R3"}
PARTIAL_IDS = ["M0651-L-ENUM", "M0651-L-DENSE", "M0651-B-ARITY0"]
OPEN_ROOT_CUT = [
    "M0651-L-ENUM", "M0651-L-DENSE", "M0651-L-HENKIN", "M0651-L-OMIT",
]
EXPECTED_INPUTS = {
    "instance.json": "a4829af9d1331524e186d3e54ad90dfdfead7fda371e85ad345c956406c6a945",
    "Statement.lean": "39b09536792acdd585eb62dc09917eca50eff8717211a764bca58d96645d38ea",
    "ObligationTree.lean": "2317873fba80bc681a10267eaba79f13828a35f156950168a388b565f9c8c2df",
    "ProofLemmas.lean": "47b5cb564dba6793cc10b3b9cf3cd50cd565441a8b2cd97cc346462928e089dc",
    "Validation.lean": "ab820ad99f8c5fb6cc479db9b51215635155b5eb8bf1b85931da97105d7ee121",
    "statement.json": "cf4e441e06d3309f010c975b2da9efea08ed805a66627797b7400bae6e503c5b",
    "anchor-audit.json": "17fc3419e05444401a36b0146562a552179c663c6a92606f1a05add44b21111c",
    "obligation-registry.json": "9a87b090025b80fde991e80c2eec07a9f67ae84a269802288d30c7ec572d142f",
    "typed-graphs.json": "7ae5e1d811de7c88799746b29a6d89d277f0954ab1b131c499f807cb47548900",
    "validation-specs.json": "4dae74f1a59cd29cab2c6df0dcae15211c870ac077d1b17b7990d5b1b9eb911c",
    "proof-receipt.json": "92501ac511409d61a3303884b0d25ba4024fdaf936eb38855a85866644113ee2",
    "proof-blocker.json": "3e937b90d7746c5b13afb72ab953c729a7041a725a2266649ebba86f49b48f80",
    "source-statement-crosswalk.md": "00718987cb793062b48e4581bc224f8eab57ef08817d03ae1ac1935a50815f8e",
    "check_obligation_tree.py": "9a71a865cd55045f999dd29b8964c0a6af60981130d1457ea5d1946492df08fa",
    "check_proof.sh": "bdf2e00cdfa7a632c6fb36e3b0597330366034130d1bb4d32b08a146743f0d95",
}
SOURCE_BOUNDARIES = {
    "Mathlib/ModelTheory/Basic.lean": {
        "blob": "2fbcc91b10a0c30a8db3f172a31051a985d186fc",
        "source_sha256": "605f58bb88665164b80112c3e03ef0ed1730d3521a356b52a917aed8d9dc269b",
        "olean_sha256": "076c18295efbb5703b79ea534f911a0115feccbdd0fbd92d1858b619ac3075a9",
        "olean_bytes": 770736,
    },
    "Mathlib/ModelTheory/Encoding.lean": {
        "blob": "4f89b44a4bde26011d23e1bc34ee4d96bef1a440",
        "source_sha256": "2d7709cb45570abbfab31647fb747baa6820c0d26e08c8071bdb04706469ee7d",
        "olean_sha256": "e16b65dbdaca6da901c58ce2e34f2d3c72a2978aa3b8292998eaa61aa0c0c633",
        "olean_bytes": 937072,
    },
    "Mathlib/ModelTheory/Satisfiability.lean": {
        "blob": "b0688b14fc0cec8283a3666c886faf010858f401",
        "source_sha256": "0abb92d531851a57909945b740981d79a4cbb29238f2a3d21cb5fa57aa143edb",
        "olean_sha256": "56f4ca802c48e3f8c97fb8bb939f027d2ee2712cacf1de1495bae29796ae9a9b",
        "olean_bytes": 108872,
    },
    "Mathlib/Data/Countable/Defs.lean": {
        "blob": "38a9d80b0ea672f7ac03a7ee3dc6d6baf7bfff58",
        "source_sha256": "cdc835b0a6826e59905cbc5841db0de60b70e87e746cadda939b63529c67bdfe",
        "olean_sha256": "5b25fa7d27f2cd0fb9d6e64b0e415db8458f6e51eb36da57b66c25949ce97ac0",
        "olean_bytes": 47536,
    },
}
PROOF_DECLARATIONS = (
    "Stage1Instances.THM_M_0651.ProofLemmas.countable_symbols",
    "Stage1Instances.THM_M_0651.ProofLemmas.countable_finite_arity_syntax",
    "Stage1Instances.THM_M_0651.ProofLemmas.exists_surjective_formula_schedule",
    "Stage1Instances.THM_M_0651.ProofLemmas.countable_avoidance_requirements",
    "Stage1Instances.THM_M_0651.ProofLemmas.exists_surjective_avoidance_schedule",
    "Stage1Instances.THM_M_0651.ProofLemmas.exists_consistent_avoidance_extension",
)
AXIOM_FREE_PROOF_DECLARATIONS = (
    "Stage1Instances.THM_M_0651.ProofLemmas.zero_arity_formula_requirement_inhabited",
    "Stage1Instances.THM_M_0651.ProofLemmas.zero_arity_tuple_requirement_inhabited",
)
VALIDATION_DECLARATIONS = (
    "Stage1Instances.THM_M_0651.Validation.differentialOmitsIffNoRealizingTuple",
    "Stage1Instances.THM_M_0651.Validation.differentialExistsSurjectiveAvoidanceSchedule",
    "Stage1Instances.THM_M_0651.Validation.differentialExistsConsistentAvoidanceExtension",
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
    "PASS narrow kernel replay: exact statement, conditional tree, eight partial proof bodies, and three no-import differential declarations elaborated at trust zero",
    "PASS trust observation: all checked bodies use only propext, Classical.choice, and Quot.sound; differential closure has no bodyless nonaxiom or unsafe declaration",
    "PASS selected provenance: frozen hashes, four selected mathlib source/olean boundaries, executable pins, license, and clean pinned revision agree",
    "OPEN exact root: the frozen cut ENUM/DENSE/HENKIN/OMIT remains M4 with zero closed obligations and no canonical cross-module root proof",
    "FAIL CLOSED complete trust/provenance: proof acceptance, accepted foundation policy, serialized transitive closure, and full TCB/SBOM inventory are absent",
    "FAIL CLOSED release gates: shared warm cache is not cold hermetic evidence and this worker is not a distinct independent verifier",
]

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
    return run(["/usr/bin/git", *args], cwd=cwd, env=BASE_ENV).strip()


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
    no_axioms = f"'{declaration}' does not depend on any axioms"
    pattern = re.compile(
        re.escape(f"'{declaration}' depends on axioms: [") + r"(.*?)]", re.DOTALL,
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
        (LEAN_ROOT / ".lake" / "packages" / name / ".lake/build/lib/lean").resolve()
        for name in package_names
    ]
    assert all(path.is_dir() for path in roots)
    local = (LEAN_ROOT / ".lake/build/lib/lean").resolve()
    assert local.is_dir()
    return ":".join([*(str(path) for path in roots), str(local), str(lean.parent.parent / "lib/lean")])


def isolated_replay(lean: Path, bwrap: Path, lean_path: str) -> dict[str, str]:
    with tempfile.TemporaryDirectory(prefix="stage1-m0651-validation-", dir="/tmp") as tmp_name:
        tmp = Path(tmp_name).resolve()
        names = ("Statement.lean", "ObligationTree.lean", "ProofLemmas.lean", "Validation.lean")
        for name in names:
            (tmp / name).write_bytes((HERE / name).read_bytes())
        (tmp / "home").mkdir()
        base = [
            str(bwrap), "--ro-bind", "/", "/", "--bind", str(tmp), str(tmp),
            "--dev", "/dev", "--proc", "/proc", "--unshare-net", "--die-with-parent",
            "--clearenv", "--setenv", "HOME", str(tmp / "home"),
            "--setenv", "TMPDIR", str(tmp), "--setenv", "LANG", "C.UTF-8",
            "--setenv", "LC_ALL", "C.UTF-8", "--setenv", "TZ", "UTC",
            "--setenv", "LEAN_NUM_THREADS", "1", "--chdir", str(tmp),
        ]

        def lean_run(name: str, module_path: str) -> str:
            output = name.replace(".lean", ".olean")
            return run(base + [
                "--setenv", "LEAN_PATH", module_path, str(lean), "--trust=0", "-t0",
                "--root", str(tmp), "-o", output, name,
            ])

        statement = lean_run("Statement.lean", lean_path)
        return {
            "statement": statement,
            "obligation_tree": lean_run("ObligationTree.lean", lean_path),
            "proof": lean_run("ProofLemmas.lean", lean_path),
            "validation": lean_run("Validation.lean", f"{tmp}:{lean_path}"),
        }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--probe", action="store_true")
    parser.add_argument("--worker-packet", type=Path)
    args = parser.parse_args()

    execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")
    targets = load(ROOT / "Docs" / "Stage1_Targets_rev-5.6.json")
    instance = load(HERE / "instance.json")
    statement = load(HERE / "statement.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    proof_receipt = load(HERE / "proof-receipt.json")
    proof_blocker = load(HERE / "proof-blocker.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 697 and target["baseline"] == "L0"
    assert target["lifecycle_mode"] == "planned"
    assert target["rework_required"] is True and target["theorem_complete"] is False
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item == {
        "id": ITEM, "theorem_id": THEOREM, "execution_rank": 697,
        "phase": "validation", "layer": 5, "state": "[ ]",
        "depends_on": ["S56-M-0651-PROOF"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Run hermetic kernel, trust, provenance, and independent validation gates.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0, "children": [],
    }
    predecessor = next(row for row in execution["items"] if row["id"] == "S56-M-0651-PROOF")
    assert predecessor["state"] == "[_]" and predecessor["attempts"] >= 1

    for name, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"stale validation input: {name}"
    assert sha256(LEAN_ROOT / "lean-toolchain") == TOOLCHAIN_SHA256
    assert sha256(LEAN_ROOT / "lake-manifest.json") == MANIFEST_SHA256
    formal = statement["canonical_formal_target"]
    assert formal["elaborated_expression_sha256"] == STATEMENT_EXPRESSION_SHA256
    assert formal["statement_file_sha256"] == EXPECTED_INPUTS["Statement.lean"]
    assert registry["frozen_against_statement_sha256"] == EXPECTED_INPUTS["statement.json"]
    assert registry["frozen_against_anchor_audit_sha256"] == EXPECTED_INPUTS["anchor-audit.json"]
    assert registry["root_obligation_id"] == "M0651-ROOT"
    assert registry["denominator_sha256"] == graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    closure = graphs["closure_boundary"]
    assert closure["closed_obligations"] == [] and closure["root_closed"] is False
    assert closure["root_machine_debt"] == "M4" and closure["remaining_root_cut_set"] == OPEN_ROOT_CUT
    assert closure["audit_complete"] is closure["theorem_complete"] is False
    root = next(node for node in graphs["nodes"] if node["obligation_id"] == "M0651-ROOT")
    assert {"H": root["human_debt"], "M": root["machine_debt"], "R": root["readability_debt"]} == ROOT_VECTOR
    assert instance["root_vector"] == ROOT_VECTOR
    assert instance["audit_complete"] is instance["theorem_complete"] is False

    assert proof_receipt["item_id"] == "S56-M-0651-PROOF"
    assert proof_receipt["proof_body"]["source_sha256"] == EXPECTED_INPUTS["ProofLemmas.lean"]
    assert proof_receipt["partial_progress_toward_obligation_ids"] == PARTIAL_IDS
    assert proof_receipt["supported_obligation_ids"] == []
    assert proof_receipt["provisionally_closed_obligation_ids"] == []
    assert proof_receipt["accepted_closed_obligation_ids"] == []
    assert proof_receipt["accepted"] is False
    assert proof_receipt["result"]["root_kernel_closed"] is False
    assert proof_receipt["result"]["theorem_complete"] is False
    assert proof_receipt["remaining_root_cut_set"] == OPEN_ROOT_CUT
    assert proof_blocker["root_closed"] is False and proof_blocker["theorem_complete"] is False

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by|run_tac|oracle)\b|"
        r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
        r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
        r"(?:axiom|constant|opaque|unsafe|extern)\b", re.MULTILINE,
    )
    source_names = ("Statement.lean", "ObligationTree.lean", "ProofLemmas.lean", "Validation.lean")
    all_source = "\n".join(
        source_without_comments_and_strings((HERE / name).read_text(encoding="utf-8"))
        for name in source_names
    )
    assert prohibited.search(all_source) is None
    validation_imports = (HERE / "Validation.lean").read_text(encoding="utf-8").split("/-!", 1)[0]
    assert "import ProofLemmas" not in validation_imports
    assert "import ObligationTree" not in validation_imports

    manifest = load(LEAN_ROOT / "lake-manifest.json")
    mathlib_entry = next(row for row in manifest["packages"] if row["name"] == "mathlib")
    assert mathlib_entry["rev"] == mathlib_entry["inputRev"] == MATHLIB_REVISION
    assert mathlib_entry["url"] == MATHLIB_REMOTE
    assert (LEAN_ROOT / ".lake").is_symlink()
    mathlib = (LEAN_ROOT / ".lake/packages/mathlib").resolve()
    assert git("rev-parse", "HEAD", cwd=mathlib) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == MATHLIB_TREE
    assert git("remote", "get-url", "origin", cwd=mathlib) == MATHLIB_REMOTE
    assert git("status", "--porcelain=v1", "--untracked-files=all", cwd=mathlib) == ""
    assert sha256(mathlib / "LICENSE") == MATHLIB_LICENSE_SHA256
    for relative, expected in SOURCE_BOUNDARIES.items():
        source = mathlib / relative
        olean = mathlib / ".lake/build/lib/lean" / Path(relative).with_suffix(".olean")
        assert git("rev-parse", f"HEAD:{relative}", cwd=mathlib) == expected["blob"]
        assert sha256(source) == expected["source_sha256"]
        assert sha256(olean) == expected["olean_sha256"]
        assert olean.stat().st_size == expected["olean_bytes"]
        assert prohibited.search(source_without_comments_and_strings(source.read_text(encoding="utf-8"))) is None

    lake_launcher = Path(HOME) / ".elan/bin/lake"
    assert sha256(lake_launcher) == ELAN_LAUNCHER_SHA256
    lean = Path(run([str(lake_launcher), "env", "which", "lean"], cwd=LEAN_ROOT, env=BASE_ENV).strip())
    lake = Path(run([str(lake_launcher), "env", "which", "lake"], cwd=LEAN_ROOT, env=BASE_ENV).strip())
    bwrap = Path("/usr/bin/bwrap")
    python = Path("/usr/bin/python3").resolve()
    git_executable = Path("/usr/bin/git")
    assert sha256(lean) == LEAN_SHA256 and sha256(lake) == LAKE_SHA256
    assert sha256(bwrap) == BWRAP_SHA256 and sha256(python) == PYTHON_SHA256
    assert sha256(git_executable) == GIT_SHA256
    assert LEAN_COMMIT in run([str(lean), "--version"], env=BASE_ENV)
    assert "5.0.0-src+98dc76e" in run([str(lake), "--version"], env=BASE_ENV)

    outputs = isolated_replay(lean, bwrap, pinned_lean_path(lean))
    combined = "\n".join(outputs.values())
    assert "sorryAx" not in combined and all("error:" not in output for output in outputs.values())
    assert reported_axioms(
        outputs["obligation_tree"],
        "Stage1Instances.THM_M_0651.ObligationTree.root_compose",
    ) == {"propext", "Quot.sound"}
    for declaration in PROOF_DECLARATIONS:
        assert reported_axioms(outputs["proof"], declaration) == EXPECTED_AXIOMS
    for declaration in AXIOM_FREE_PROOF_DECLARATIONS:
        assert reported_axioms(outputs["proof"], declaration) == set()
    for declaration in VALIDATION_DECLARATIONS:
        assert reported_axioms(outputs["validation"], declaration) == EXPECTED_AXIOMS
    assert outputs["validation"].count("Declarations are sorry-free!") == 3
    closure_match = re.search(r"VALIDATION_CLOSURE declarations=(\d+) modules=(\d+)", outputs["validation"])
    assert closure_match is not None
    assert "VALIDATION_CLOSURE axioms=[propext, Classical.choice, Quot.sound]" in outputs["validation"]
    assert "VALIDATION_CLOSURE bodyless_nonaxioms=[]" in outputs["validation"]
    assert "VALIDATION_CLOSURE unsafe=[]" in outputs["validation"]
    observation = {
        "lean_output_sha256": {name: hashlib.sha256(output.encode()).hexdigest() for name, output in outputs.items()},
        "observed_axioms": sorted(EXPECTED_AXIOMS),
        "validation_closure": {
            "declarations": int(closure_match.group(1)),
            "modules": int(closure_match.group(2)),
            "bodyless_nonaxioms": [],
            "unsafe_declarations": [],
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
    assert spec["depends_on"] == receipt["depends_on"] == ["S56-M-0651-PROOF"]
    assert len(spec["recipes"]) == 1 and spec["recipes"][0] == receipt["recipe"]
    recipe = spec["recipes"][0]
    assert recipe["argv"] == [
        "/usr/bin/python3", "-I", "-B", f"Stage1_Instances/{THEOREM}/check_validation.py",
        "--worker-packet", ".stage1-worker-selftest.json",
    ]
    assert recipe["covered_obligation_ids"] == []
    assert recipe["validated_partial_progress_toward_obligation_ids"] == PARTIAL_IDS
    assert recipe["cwd"] == "." and recipe["timeout_seconds"] == 600
    assert recipe["network_policy"] == "denied" and recipe["expected_exit"] == 0
    assert recipe["env_allowlist"] == {
        "ELAN_TOOLCHAIN": TOOLCHAIN, "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8",
        "TZ": "UTC", "LEAN_NUM_THREADS": "1",
        "HOME": "runner home used only to address the hash-verified .elan/bin/lake launcher",
        "PATH": "/usr/bin:/bin",
    }
    assert len(recipe["expected_outputs"]) == 1
    assert recipe["expected_outputs"][0]["path_or_stream"] == "stdout"
    assert "bubblewrap" in recipe["network_enforcement"]
    assert len(recipe["covered_declarations"]) == len(set(recipe["covered_declarations"]))
    assert "zero frozen obligations" in recipe["scope_boundary"]

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
    assert receipt["validation_started_at"] < receipt["validation_ended_at"] == receipt["validated_at"]
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
    assert repository_state["preexisting_untracked_lake_symlink_target_sha256"] == hashlib.sha256(
        os.readlink(LEAN_ROOT / ".lake").encode()
    ).hexdigest()
    for name, expected in EXPECTED_INPUTS.items():
        assert receipt["inputs"][name] == expected, name
    assert receipt["inputs"]["validation-spec.json"] == sha256(HERE / "validation-spec.json")
    assert receipt["inputs"]["check_validation.py"] == sha256(Path(__file__).resolve())
    assert receipt["target"]["elaborated_expression_sha256"] == STATEMENT_EXPRESSION_SHA256
    assert receipt["target"]["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert receipt["environment"]["platform"] == f"{platform.system()} {platform.release()} {platform.machine()}"
    environment = receipt["environment"]
    assert environment["toolchain"] == TOOLCHAIN and environment["lean_commit"] == LEAN_COMMIT
    assert environment["lean_executable_sha256"] == sha256(lean)
    assert environment["lake_executable_sha256"] == sha256(lake)
    assert environment["bubblewrap_executable_sha256"] == sha256(bwrap)
    assert environment["python_executable_sha256"] == sha256(python)
    assert environment["git_executable_sha256"] == sha256(git_executable)
    assert environment["mathlib_revision"] == MATHLIB_REVISION
    assert environment["mathlib_tree"] == MATHLIB_TREE
    assert environment["mathlib_origin"] == MATHLIB_REMOTE
    assert environment["mathlib_license_sha256"] == MATHLIB_LICENSE_SHA256
    direct = receipt["direct_provenance"]
    assert direct["proof_dependency_master_accepted"] is False
    assert direct["canonical_root_terminal_body_id"] is None
    assert direct["complete_terminal_body_import_artifact_source_boundary_and_tcb_closure"] is False
    recorded_boundaries = {row["source"]: row for row in direct["source_and_compiled_boundaries"]}
    assert set(recorded_boundaries) == set(SOURCE_BOUNDARIES)
    for relative, expected in SOURCE_BOUNDARIES.items():
        row = recorded_boundaries[relative]
        assert row["source_blob"] == expected["blob"]
        assert row["source_sha256"] == expected["source_sha256"]
        assert row["compiled_sha256"] == expected["olean_sha256"]
        assert row["compiled_bytes"] == expected["olean_bytes"]
    result = receipt["result"]
    assert result["lean_output_sha256"] == observation["lean_output_sha256"]
    assert result["observed_axioms"] == observation["observed_axioms"]
    assert result["validation_closure"] == observation["validation_closure"]
    assert result["validated_partial_progress_toward_obligation_ids"] == PARTIAL_IDS
    assert result["supported_obligation_ids"] == []
    assert result["provisionally_closed_obligation_ids"] == []
    assert result["accepted_closed_obligation_ids"] == []
    assert result["proof_dependency_master_acceptance"] == "fail_closed"
    assert result["root_closed"] is result["root_kernel_closed"] is False
    assert result["root_machine_debt"] == "M4" and result["open_root_cut_set"] == OPEN_ROOT_CUT
    assert result["complete_trust_provenance_gate"] == "fail_closed"
    assert result["hermetic_release_gate"] == "fail_closed"
    assert result["independent_distinct_runner_gate"] == "fail_closed"
    assert result["audit_complete"] is result["theorem_complete"] is False
    assert receipt["trust"]["accepted_foundation_profile"] is False
    assert receipt["trust"]["complete_transitive_trust_closure"] is False
    assert receipt["hermeticity"]["fresh_clean_checkout"] is False
    assert receipt["hermeticity"]["empty_user_package_and_build_caches"] is False
    assert receipt["hermeticity"]["decision"].startswith("fail_closed")
    independent = receipt["independent_validation"]
    assert independent["distinct_verifier_identity"] is False
    assert independent["independently_provisioned_clean_runner"] is False
    assert independent["second_signed_attestation"] is False
    assert independent["independently_implemented_minimal_release_verifier"] is False
    assert independent["decision"] == "fail_closed"
    assert receipt["remaining_root_cut_set"] == OPEN_ROOT_CUT
    assert receipt["first_failed_gate"] == (
        "dependency.S56-M-0651-PROOF.master_acceptance_and_M0651-L-HENKIN.root_closure"
    )
    expected_stdout = ("\n".join(SUMMARY_LINES) + "\n").encode()
    assert receipt["output_evidence"]["stdout_semantic_sha256"] == hashlib.sha256(expected_stdout).hexdigest()
    output_evidence = receipt["output_evidence"]
    assert output_evidence["expected_line_count"] == len(SUMMARY_LINES)
    assert output_evidence["exit_code"] == 0
    assert output_evidence["raw_logs_retained"] is False
    assert output_evidence["raw_log_sha256"] is None
    assert receipt["known_failures"] and receipt["invalidation_inputs"]
    assert receipt["freshness"]["support_state"] == "provisional_nonrelease_worker_evidence"
    assert receipt["freshness"]["revocation_state"] == "unaccepted"
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
        actual = {line[3:] for line in status.splitlines() if line[3:] != "Formalizations/Lean/.lake"}
        assert actual == set(CHANGED_PATHS), (actual, set(CHANGED_PATHS))

    for relative in CHANGED_PATHS:
        assert_text_hygiene(ROOT / relative)
    for line in SUMMARY_LINES:
        print(line)


if __name__ == "__main__":
    main()
