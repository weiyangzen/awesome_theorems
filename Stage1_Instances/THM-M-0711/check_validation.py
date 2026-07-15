#!/usr/bin/env python3
"""Fail-closed validation worker for S56-M-0711-VALIDATION."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import re
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0711"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
ITEM = "S56-M-0711-VALIDATION"
THEOREM = "THM-M-0711"
BASE_REVISION = "3a40b1969f841e07036db5c4d7f03e97c7c57949"
BASE_TREE = "404cccc598c2d4c8831d55138df788f0438ddce8"
TOOLCHAIN = "leanprover/lean4:v4.29.0"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
LEAN_SHA256 = "3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf"
LAKE_SHA256 = "a608ff084d7e2af228b92a29d7c2fd083ba0580e46889175ec74a81678c98359"
ELAN_LAUNCHER_SHA256 = "840179e70803ef373c2ec53342d6a45ea7d022533e4145489fc1278b4f716385"
BWRAP_SHA256 = "0abea81db798ebf6b4742ac0664802d97521547a353c2a0dbdc21d76cbbfd2c0"
PYTHON_SHA256 = "b8d8288faefdd300201f43fcf00f6f539a27218eeed3a3dff5ab10b9c4c99700"
GIT_SHA256 = "5516c9f362c29376ab9a499a33082f9f611941d8c75930c880e30ad109e39c9a"
TOOLCHAIN_SHA256 = "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2"
MANIFEST_SHA256 = "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_REMOTE = "https://github.com/leanprover-community/mathlib4.git"
MATHLIB_LICENSE_SHA256 = "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1"
STATEMENT_SHA256 = "624dd9575960ac9d10b05c677f744c333edc7b162ddda57cafa251642b803436"
DENOMINATOR_SHA256 = "9fbdae321a68e51a301e942864c9a785fab407f21f25247ab04cb74277bd8d24"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
ROOT_VECTOR = {"H": "H1", "M": "M4", "R": "R4"}
PROVISIONAL_IDS = ["M0711-N-QUOTIENT", "M0711-L-HALTING", "M0711-L-MANYONE"]
PARTIAL_IDS = ["M0711-L-NONCOMP", "M0711-T-WITNESS", "M0711-ROOT"]
OPEN_ROOT_CUT = ["M0711-B-REDUCTION", "M0711-S-FOUNDATION"]
EXPECTED_INPUTS = {
    "Statement.lean": STATEMENT_SHA256,
    "ObligationTree.lean": "d5b191ec34e258151ca1a56c041636eda0d5c7149936dca536db492e4d5f8e14",
    "Proof.lean": "119c50417d4559f3142fd67e0375b4cb99865141842f1a1dfc27352f2ada2b65",
    "Validation.lean": "f361ca0ec0c54a9aa9abc26592a7cd27996fe0dc88bd143736c89fdddf0cb789",
    "statement-receipt.json": "0e497c79be5be1727ad57d10553a6224142235390cb8f49dc2b0c26e90241194",
    "obligation-registry.json": "0d40d1d7aa73bb51f2c263f27bac6b348c628cf8405af86b2473637981800983",
    "typed-graphs.json": "f24be97eda17d4e9c99da61f43fc7a5886e489aff1fc335611ab14339f5ff94f",
    "proof-receipt.json": "196f2d0cbbb8145cb78ec6e0ab5f33929cb4cc5e2e0668b5742e56915247acb1",
    "proof-blocker.json": "1ab776204688472c11dc63daab57d29cfc06e11f2a0740d623cb34cd1d7094ef",
    "anchor-audit-receipt.json": "7f186646b95d2a905cfcc73de8085727e4e130e1e4a0a7eb8de33b1ddf628e41",
    "source-statement-crosswalk.md": "74e237433a2c2e14ddf347665c7792de36465bda6f72af3adab08445e165eeaa",
    "proof-validation.md": "214173772dc2ca682aff64a915621786f4b7fa2b0ede585936d42e577bea6fbf",
}
SOURCE_BOUNDARIES = {
    "Mathlib/GroupTheory/PresentedGroup.lean": {
        "blob": "8197660a6783c139ff5c5583e34792f148819e0e",
        "source_sha256": "4226ec95821cd97aaf33a5fd22d3c58dd3b8de4cd3c46e4b8b92e232b77297a9",
        "olean_sha256": "f8a8ba929e4756ab166577dc356c36de35a024b3feae622c54a7762cb1e2080b",
        "olean_bytes": 117776,
    },
    "Mathlib/Computability/Reduce.lean": {
        "blob": "aa5487c021cfdb4c7644efdd30ec5eb9dc0775bb",
        "source_sha256": "30513e477c461fdce1518542f4dc16085f1d98ab47ba2bfbc28d5b741b18e556",
        "olean_sha256": "ed05cc633a618b11db47fafc0daa6333c804d18e5114d7013c0cda9259c33dfe",
        "olean_bytes": 197560,
    },
    "Mathlib/Computability/Halting.lean": {
        "blob": "0834371356762db805d37208b9cf8a1fc0efd217",
        "source_sha256": "c2a073a05c631e7fc957577a66025e9ac36dac741f9aa865e0f053b17f0c85de",
        "olean_sha256": "a4d0f485725fd93028f52418d4c5b6251cbd59cececed2b4ff1f4ac5578a61ba",
        "olean_bytes": 107608,
    },
}
PROOF_DECLARATIONS = (
    "Stage1.THM_M_0711.identityPred_iff_normalClosure",
    "Stage1.THM_M_0711.not_computablePred_of_manyOneReducible",
    "Stage1.THM_M_0711.haltingPredicate_not_computable",
    "Stage1.THM_M_0711.fixedPresentationUndecidable_of_haltingReduction",
    "Stage1.THM_M_0711.novikovBooneTarget_of_haltingReduction",
)
VALIDATION_DECLARATIONS = (
    "Stage1.THM_M_0711.Validation.differentialIdentityPredIffNormalClosure",
    "Stage1.THM_M_0711.Validation.differentialNotComputablePredOfManyOne",
    "Stage1.THM_M_0711.Validation.differentialHaltingPredicateNotComputable",
    "Stage1.THM_M_0711.Validation.differentialConditionalTarget",
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
    "PASS kernel: network-isolated trust-zero fresh-output replay checked the exact statement, partial proof declarations, and differential reconstruction",
    "PASS trust observation: proof and differential declarations are sorry-free and report exactly propext, Classical.choice, and Quot.sound",
    "PASS selected provenance: frozen hashes, clean mathlib pin, license, and three direct source/olean boundaries agree",
    "OPEN exact root: the finite-presentation reduction and accepted foundation gate remain open at M4; accepted state is unchanged",
    "FAIL CLOSED complete trust/provenance: the accepted foundation profile, complete transitive TCB/SBOM, and terminal root provenance are absent",
    "FAIL CLOSED release gates: the shared warm cache is not cold hermetic evidence and this worker is not an independent verifier",
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
    argv: list[str], *, cwd: Path = ROOT, env: dict[str, str] | None = None,
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
        re.escape(f"'{declaration}' depends on axioms: [") + r"(.*?)]",
        re.DOTALL,
    )
    matches = pattern.findall(output)
    assert len(matches) == 1, f"missing or duplicate axiom report for {declaration}"
    return {part.strip() for part in matches[0].split(",") if part.strip()}


def assert_text_hygiene(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())


def ensure_network_isolated() -> None:
    """Re-execute the complete recipe in a read-only, networkless sandbox."""
    if os.environ.get("STAGE1_M0711_NETWORK_ISOLATED") == "1":
        return
    bwrap = Path("/usr/bin/bwrap")
    assert sha256(bwrap) == BWRAP_SHA256
    argv = [
        str(bwrap), "--ro-bind", "/", "/", "--dev", "/dev", "--proc", "/proc",
        "--tmpfs", "/tmp", "--unshare-net", "--die-with-parent", "--clearenv",
        "--setenv", "HOME", HOME, "--setenv", "PATH", BASE_ENV["PATH"],
        "--setenv", "ELAN_TOOLCHAIN", TOOLCHAIN, "--setenv", "LANG", "C.UTF-8",
        "--setenv", "LC_ALL", "C.UTF-8", "--setenv", "TZ", "UTC",
        "--setenv", "LEAN_NUM_THREADS", "1", "--setenv", "TMPDIR", "/tmp",
        "--setenv", "STAGE1_M0711_NETWORK_ISOLATED", "1", "--chdir", str(ROOT),
        "/usr/bin/python3", "-I", "-B", str(Path(__file__).resolve()), *sys.argv[1:],
    ]
    os.execv(str(bwrap), argv)


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
    assert os.environ.get("STAGE1_M0711_NETWORK_ISOLATED") == "1"
    with tempfile.TemporaryDirectory(prefix="stage1-m0711-validation-", dir="/tmp") as tmp_name:
        tmp = Path(tmp_name).resolve()
        for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
            (tmp / name).write_bytes((HERE / name).read_bytes())
        (tmp / "home").mkdir()
        def lean_run(name: str, module_path: str, emit_olean: bool) -> str:
            argv = [str(lean), "--trust=0"]
            if emit_olean:
                argv += ["-o", name.replace(".lean", ".olean")]
            argv.append(name)
            env = {
                "HOME": str(tmp / "home"),
                "PATH": BASE_ENV["PATH"],
                "LANG": "C.UTF-8",
                "LC_ALL": "C.UTF-8",
                "TZ": "UTC",
                "LEAN_NUM_THREADS": "1",
                "TMPDIR": str(tmp),
                "LEAN_PATH": module_path,
            }
            return run(argv, cwd=tmp, env=env)

        return {
            "statement": lean_run("Statement.lean", lean_path, True),
            "obligation": lean_run("ObligationTree.lean", f"{tmp}:{lean_path}", True),
            "proof": lean_run("Proof.lean", f"{tmp}:{lean_path}", False),
            "validation": lean_run("Validation.lean", f"{tmp}:{lean_path}", False),
        }


def main() -> None:
    ensure_network_isolated()
    parser = argparse.ArgumentParser()
    parser.add_argument("--probe", action="store_true")
    parser.add_argument("--worker-packet", type=Path)
    args = parser.parse_args()

    targets = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    proof_receipt = load(HERE / "proof-receipt.json")
    proof_blocker = load(HERE / "proof-blocker.json")
    statement_receipt = load(HERE / "statement-receipt.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 751 and target["baseline"] == "L0"
    assert target["lifecycle_mode"] == "planned"
    assert target["rework_required"] is True and target["theorem_complete"] is False
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 751,
        "phase": "validation",
        "layer": 5,
        "state": "[ ]",
        "depends_on": ["S56-M-0711-PROOF"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Run hermetic kernel, trust, provenance, and independent validation gates.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    predecessor = next(row for row in execution["items"] if row["id"] == "S56-M-0711-PROOF")
    assert predecessor["state"] == "[_]" and predecessor["attempts"] == 1
    assert proof_receipt["support_state"] != "master_accepted"

    for name, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"stale validation input: {name}"
    assert sha256(LEAN_ROOT / "lean-toolchain") == TOOLCHAIN_SHA256
    assert sha256(LEAN_ROOT / "lake-manifest.json") == MANIFEST_SHA256
    assert registry["root_obligation_id"] == graphs["root_node_id"] == "M0711-ROOT"
    assert statement_receipt["source"]["declaration"] == "Stage1.THM_M_0711.NovikovBooneTarget"
    assert statement_receipt["source"]["sha256"] == STATEMENT_SHA256
    assert statement_receipt["elaboration"]["unresolved_metavariables"] is False
    assert registry["frozen_against_statement_sha256"] == STATEMENT_SHA256
    assert registry["denominator_sha256"] == graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert graphs["closure_boundary"] == {
        "root_closed": False,
        "theorem_complete": False,
        "remaining_root_cut_set": OPEN_ROOT_CUT,
    }
    root = next(node for node in graphs["nodes"] if node["obligation_id"] == "M0711-ROOT")
    assert {"H": root["human_debt"], "M": root["machine_debt"], "R": root["readability_debt"]} == ROOT_VECTOR
    assert proof_receipt["proof_body"]["source_sha256"] == EXPECTED_INPUTS["Proof.lean"]
    assert proof_receipt["provisionally_closed_obligation_ids"] == PROVISIONAL_IDS
    assert proof_receipt["partial_progress_toward_obligation_ids"] == PARTIAL_IDS
    assert proof_receipt["accepted_closed_obligation_ids"] == []
    assert proof_receipt["accepted"] is False
    assert proof_receipt["result"]["root_kernel_closed"] is False
    assert proof_receipt["result"]["theorem_complete"] is False
    assert proof_receipt["remaining_root_cut_set"] == OPEN_ROOT_CUT
    assert proof_blocker["root_closed"] is proof_blocker["audit_complete"] is False
    assert proof_blocker["theorem_complete"] is False

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by)\b|"
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
    validation_source = (HERE / "Validation.lean").read_text(encoding="utf-8")
    validation_imports = validation_source.split("/-!", 1)[0]
    assert "import Proof" not in validation_imports and "import ObligationTree" not in validation_imports
    for fragment in (
        "theorem differentialIdentityPredIffNormalClosure",
        "theorem differentialNotComputablePredOfManyOne",
        "theorem differentialHaltingPredicateNotComputable",
        "theorem differentialConditionalTarget",
        "assert_no_sorry differentialConditionalTarget",
        "#print_validation_closure",
    ):
        assert fragment in validation_source, fragment

    manifest = load(LEAN_ROOT / "lake-manifest.json")
    mathlib_entry = next(row for row in manifest["packages"] if row["name"] == "mathlib")
    assert mathlib_entry["rev"] == mathlib_entry["inputRev"] == MATHLIB_REVISION
    assert mathlib_entry["url"] == MATHLIB_REMOTE
    assert (LEAN_ROOT / ".lake").is_symlink()
    mathlib = (LEAN_ROOT / ".lake/packages/mathlib").resolve()
    assert git("rev-parse", "HEAD", cwd=mathlib) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == MATHLIB_TREE
    assert git("status", "--porcelain=v1", "--untracked-files=all", cwd=mathlib) == ""
    assert git("remote", "get-url", "origin", cwd=mathlib) == MATHLIB_REMOTE
    assert sha256(mathlib / "LICENSE") == MATHLIB_LICENSE_SHA256
    pinned_by_file = {row["file"]: row for row in proof_receipt["pinned_sources"]}
    for relative, expected in SOURCE_BOUNDARIES.items():
        source = mathlib / relative
        olean = mathlib / ".lake/build/lib/lean" / Path(relative).with_suffix(".olean")
        assert git("rev-parse", f"HEAD:{relative}", cwd=mathlib) == expected["blob"]
        assert sha256(source) == expected["source_sha256"]
        assert sha256(olean) == expected["olean_sha256"]
        assert olean.stat().st_size == expected["olean_bytes"]
        assert pinned_by_file[relative]["git_blob"] == expected["blob"]
        assert pinned_by_file[relative]["source_sha256"] == expected["source_sha256"]
        assert pinned_by_file[relative]["olean_sha256"] == expected["olean_sha256"]
        assert prohibited.search(source_without_comments(source.read_text(encoding="utf-8"))) is None

    lake_launcher = Path(HOME) / ".elan/bin/lake"
    assert sha256(lake_launcher) == ELAN_LAUNCHER_SHA256
    mathlib_lake_root = mathlib
    lean = Path(run(
        [str(lake_launcher), "env", "which", "lean"], cwd=mathlib_lake_root, env=BASE_ENV
    ).strip())
    lake = Path(run(
        [str(lake_launcher), "env", "which", "lake"], cwd=mathlib_lake_root, env=BASE_ENV
    ).strip())
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
    for declaration in PROOF_DECLARATIONS:
        assert reported_axioms(outputs["proof"], declaration) == EXPECTED_AXIOMS
    assert outputs["proof"].count("Declarations are sorry-free!") == 8
    assert reported_axioms(
        outputs["obligation"], "Stage1.THM_M_0711.novikovBooneTarget_of_witness"
    ) == EXPECTED_AXIOMS
    for declaration in VALIDATION_DECLARATIONS:
        assert reported_axioms(outputs["validation"], declaration) == EXPECTED_AXIOMS
    assert outputs["validation"].count("Declarations are sorry-free!") == 4
    closure_match = re.search(r"VALIDATION_CLOSURE declarations=(\d+) modules=(\d+)", outputs["validation"])
    assert closure_match is not None
    assert "VALIDATION_CLOSURE axioms=[propext, Classical.choice, Quot.sound]" in outputs["validation"]
    assert "VALIDATION_CLOSURE bodyless_nonaxioms=[]" in outputs["validation"]
    assert "VALIDATION_CLOSURE unsafe=[]" in outputs["validation"]
    observation = {
        "lean_output_sha256": {
            name: hashlib.sha256(output.encode()).hexdigest() for name, output in outputs.items()
        },
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
    assert spec["depends_on"] == receipt["depends_on"] == ["S56-M-0711-PROOF"]
    assert spec["env_allowlist"] == {
        "HOME": "inherited only to locate the hash-verified Elan launcher; the recipe immediately re-executes with a fixed sandbox environment"
    }
    recipe = {key: spec[key] for key in (
        "recipe_id", "cwd", "argv", "env_allowlist", "timeout_seconds",
        "network_policy", "network_enforcement", "expected_exit",
        "expected_outputs", "covered_obligation_ids", "covered_declarations",
    )}
    assert receipt["recipe"] == recipe
    assert spec["argv"] == [
        "/usr/bin/python3", "-I", "-B", f"Stage1_Instances/{THEOREM}/check_validation.py",
        "--worker-packet", ".stage1-worker-selftest.json",
    ]
    assert spec["cwd"] == "." and spec["timeout_seconds"] == 600
    assert spec["network_policy"] == "denied" and spec["expected_exit"] == 0
    assert "bwrap" in spec["network_enforcement"]

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
    assert receipt["target"]["serialized_expression_stdout_sha256"] == (
        statement_receipt["elaboration"]["serialized_stdout_sha256"]
    )
    assert receipt["target"]["environment_fingerprint"] == (
        "lean-4.29.0-98dc76e3_mathlib-8a178386ffc0_statement-elaboration"
    )
    assert receipt["validation_started_at"] < receipt["validation_ended_at"]
    assert receipt["validation_ended_at"] == receipt["validated_at"]
    assert receipt["attestor"] == "stage1-rev56-worker-slot2"
    for name, expected in EXPECTED_INPUTS.items():
        assert receipt["inputs"][name] == expected, name
    assert receipt["inputs"]["validation-spec.json"] == sha256(HERE / "validation-spec.json")
    assert receipt["inputs"]["check_validation.py"] == sha256(Path(__file__).resolve())
    assert receipt["environment"]["platform"] == f"{platform.system()} {platform.release()} {platform.machine()}"
    assert receipt["environment"]["lean_executable_sha256"] == sha256(lean)
    assert receipt["environment"]["lake_executable_sha256"] == sha256(lake)
    assert receipt["environment"]["bubblewrap_executable_sha256"] == sha256(bwrap)
    assert receipt["environment"]["python_executable_sha256"] == sha256(python)
    assert receipt["environment"]["git_executable_sha256"] == sha256(git_executable)
    result = receipt["result"]
    assert result["lean_output_sha256"] == observation["lean_output_sha256"]
    assert result["observed_axioms"] == observation["observed_axioms"]
    assert result["validation_closure"] == observation["validation_closure"]
    assert result["revalidated_provisional_obligation_ids"] == PROVISIONAL_IDS
    assert result["conditional_progress_obligation_ids"] == PARTIAL_IDS
    assert result["accepted_closed_obligation_ids"] == []
    assert result["proof_dependency_master_acceptance"] == "fail_closed"
    assert result["root_closed"] is result["root_kernel_closed"] is False
    assert result["root_machine_debt"] == "M4"
    assert result["open_root_cut_set"] == OPEN_ROOT_CUT
    assert result["complete_trust_provenance_gate"] == "fail_closed"
    assert result["hermetic_release_gate"] == "fail_closed"
    assert result["independent_distinct_runner_gate"] == "fail_closed"
    assert result["audit_complete"] is result["theorem_complete"] is False
    assert receipt["repository_state"]["release_clean"] is False
    assert receipt["repository_state"]["preexisting_untracked_lake_symlink_target_line_sha256"] == hashlib.sha256(
        (os.readlink(LEAN_ROOT / ".lake") + "\n").encode()
    ).hexdigest()
    assert receipt["trust"]["accepted_foundation_profile"] is False
    assert receipt["trust"]["complete_transitive_trust_closure"] is False
    assert receipt["direct_provenance"]["proof_dependency_master_accepted"] is False
    assert receipt["direct_provenance"]["root_terminal_body_present"] is False
    assert receipt["hermeticity"]["cold_dependency_rebuild"] is False
    assert receipt["hermeticity"]["decision"].startswith("fail_closed")
    assert receipt["independent_validation"]["distinct_verifier_identity"] is False
    assert receipt["independent_validation"]["independently_provisioned_clean_runner"] is False
    assert receipt["independent_validation"]["second_signed_attestation"] is False
    assert receipt["independent_validation"]["independently_implemented_minimal_release_verifier"] is False
    assert receipt["independent_validation"]["decision"] == "fail_closed"
    assert receipt["remaining_root_cut_set"] == OPEN_ROOT_CUT
    assert receipt["first_failed_gate"] == (
        "dependency.S56-M-0711-PROOF.master_acceptance_and_M0711-B-REDUCTION.root_closure"
    )
    expected_stdout = ("\n".join(SUMMARY_LINES) + "\n").encode()
    assert receipt["output_evidence"]["stdout_semantic_sha256"] == hashlib.sha256(expected_stdout).hexdigest()
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
        actual = {line[3:] for line in status.splitlines() if line[3:] != "Formalizations/Lean/.lake"}
        assert actual == set(CHANGED_PATHS), (actual, set(CHANGED_PATHS))

    for relative in CHANGED_PATHS:
        assert_text_hygiene(ROOT / relative)
    for line in SUMMARY_LINES:
        print(line)


if __name__ == "__main__":
    main()
