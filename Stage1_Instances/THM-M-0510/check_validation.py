#!/usr/bin/env python3
"""Fail-closed narrow validator for S56-M-0510-VALIDATION."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0510"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
ITEM = "S56-M-0510-VALIDATION"
THEOREM = "THM-M-0510"
BASE_REVISION = "472dc79eb4d406a6707691193fbe3ab58d0f0cc4"
BASE_TREE = "881d873727dc80435119839b8e60e9e9c2cfb208"
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
EXPRESSION_SHA256 = "9c84bc6acd929a60f87942f0ae5647b0430b9164e35249e561bccecc0cb91b41"
DENOMINATOR_SHA256 = "59e9147cc46427b6fc6a114cf81f7a5710c3441cf3a9ef2a74b1690f08f167dd"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
ROOT_VECTOR = {"H": "H2", "M": "M3", "R": "R4"}
EULER_OBLIGATION = "M0510-N-EULER-PRODUCT"
OPEN_ROOT_CUT = [
    "M0510-N-COEFFICIENT",
    "M0510-C-CONTOUR",
    "M0510-L-MODULAR",
    "M0510-L-MINOR-BOUND",
    "M0510-X-SOURCE",
    "M0510-X-FOUNDATION",
]
EXPECTED_INPUTS = {
    "Statement.lean": "2bdbd9447b9917305ecb72e4268f14effd74ea12a55a2f9aa620fe1d497bd049",
    "ObligationTree.lean": "d75993a57087ceae4d2b80873e991794f87957d30f75950329b9d40a0f08982b",
    "Proof.lean": "4ec8e571d3f2565b81f48161f5e1dfb41ece0d37d7a04a6ccf473fb29d1e47fa",
    "Validation.lean": "9829b209a05559b99682eb1f1a41b19868357bf3a7bd676689abd68578313992",
    "statement.json": "1a5f4b03a9cc2bdcec1cd7691d2007f689dd88b291e68efebb7a45e676284c8a",
    "obligation-registry.json": "678c26527bb23c368a7db74bc1aa6ac71e5ef479f8e0e54926fb288a2bde36b2",
    "typed-graphs.json": "98caff1f27cb7c1562624cde98867d64aa6c9387aa4af427cf3b7164e937987a",
    "proof-receipt.json": "9d1955568997cfb937c59fb273ee586128f216fbecbb2e2fc4ef799fcf3f3edd",
    "proof-blocker.json": "0373983c17ce362ff5de94d13b65259c2f81395cca8f223f5c6b31f29824234c",
    "source-statement-crosswalk.md": "8baf54d69ca4479a493972ab1d5a836aaf526537122d045d6b5d34cf61010a98",
    "scope-map.md": "50730c98dc04b194c4d56b53a86eafac54c93ac8542986850139cda67e3f2ef2",
    "validation-specs.json": "95b2ca04c21af1aa54be93207e012acdbfdbfdd90ce71f8541dc8f553593acf5",
}
SOURCE_BOUNDARIES = {
    "Mathlib/Combinatorics/Enumerative/Partition/Basic.lean": {
        "blob": "6ce7063d65d58b25638e14f5bca60a1480511154",
        "source_sha256": "365f49db37156830a0c14cf5740024dcd8bea923175d4479ee2e370fdf833a09",
        "olean_sha256": "9f6739fac4fbdfb4bf73275a0ef9d73dc62422af12c4d96ef0c639c5fe11df34",
        "olean_bytes": 161800,
    },
    "Mathlib/Combinatorics/Enumerative/Partition/Glaisher.lean": {
        "blob": "3337736c91f36168ff50e8774733af81132de1d9",
        "source_sha256": "1609afc1da7752036198d78304607aa7e1e55bbbbe6901fdb96385268b2602bb",
        "olean_sha256": "88fdbdabbe11a6b8a7a95c9b1a0e8a3ce609e7fdab272f6e07b2166862040efb",
        "olean_bytes": 51920,
    },
    "Mathlib/RingTheory/PowerSeries/PiTopology.lean": {
        "blob": "149d8a8cbef0842facbe51d9838cc706056d6480",
        "source_sha256": "e670935928e1460492aff82968289955ac87c0b51451b526fd2bba0ce366d410",
        "olean_sha256": "514dbe316c4827ebcb624d826e8c1a3a664f62db12408b16b51e288d2cd26a19",
        "olean_bytes": 101896,
    },
}
PROOF_DECLARATIONS = (
    "Stage1Instances.THM_M_0510.coeff_ordinaryPartitionSeries",
    "Stage1Instances.THM_M_0510.geometricFactor_mul_oneSub",
    "Stage1Instances.THM_M_0510.hasProd_ordinaryPartitionSeries_geometric",
    "Stage1Instances.THM_M_0510.ordinaryPartitionSeries_eq_geometricProduct",
    "Stage1Instances.THM_M_0510.ordinaryPartitionSeries_mul_eulerProduct",
)
VALIDATION_DECLARATIONS = (
    "Stage1Instances.THM_M_0510.Validation.differentialCoeffValidationPartitionSeries",
    "Stage1Instances.THM_M_0510.Validation.differentialOrdinaryPartitionSeriesMulEulerProduct",
)
CHANGED_PATHS = [
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/Validation.lean",
    f"Stage1_Instances/{THEOREM}/check_validation.py",
    f"Stage1_Instances/{THEOREM}/validation-phase-spec.json",
    f"Stage1_Instances/{THEOREM}/validation-phase.md",
    f"Stage1_Instances/{THEOREM}/validation-receipt.json",
]
SUMMARY_LINES = [
    "PASS narrow kernel replay: exact statement, partial Euler-product proof, and no-Proof differential reconstruction elaborated at trust zero",
    "PASS trust observation: all seven checked proof bodies use only propext, Classical.choice, and Quot.sound; differential closure has no bodyless nonaxiom or unsafe declaration",
    "PASS selected provenance: frozen hashes, three direct mathlib source/olean boundaries, toolchain pins, license, and clean pinned revision agree",
    "FAIL CLOSED structured authority: proof is provisional, root is open M3, and the claimed M0-L final transport is a tautological assumed-root interface rather than the registered relative-error transport",
    "FAIL CLOSED hermetic release: this network-isolated replay reuses the shared warm cache and is not a clean-checkout cold rebuild or offline archive restoration",
    "FAIL CLOSED independent release: the differential reconstruction shares this worker, checkout, toolchain, and cache; no distinct signed verifier or independent minimal release checker exists",
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
    return ":".join([*(str(path) for path in roots), str(local), str(lean.parent.parent / "lib/lean")])


def isolated_replay(lean: Path, bwrap: Path, lean_path: str) -> dict[str, str]:
    with tempfile.TemporaryDirectory(prefix="stage1-m0510-validation-", dir="/tmp") as tmp_name:
        tmp = Path(tmp_name).resolve()
        for name in ("Statement.lean", "Proof.lean", "Validation.lean"):
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
            argv = base + ["--setenv", "LEAN_PATH", module_path, str(lean), "--trust=0", "-t0"]
            if emit_olean:
                argv += ["-o", name.replace(".lean", ".olean")]
            argv.append(name)
            return run(argv)

        statement_output = lean_run("Statement.lean", lean_path, True)
        module_path = f"{tmp}:{lean_path}"
        return {
            "statement": statement_output,
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
    instance = load(HERE / "instance.json")
    statement = load(HERE / "statement.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    proof_receipt = load(HERE / "proof-receipt.json")
    proof_blocker = load(HERE / "proof-blocker.json")
    legacy_specs = load(HERE / "validation-specs.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 884 and target["baseline"] == "L0"
    assert target["lifecycle_mode"] == "planned"
    assert target["rework_required"] is True and target["theorem_complete"] is False
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 884,
        "phase": "validation",
        "layer": 5,
        "state": "[ ]",
        "depends_on": ["S56-M-0510-PROOF"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Run hermetic kernel, trust, provenance, and independent validation gates.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    predecessor = next(row for row in execution["items"] if row["id"] == "S56-M-0510-PROOF")
    assert predecessor["state"] == "[_]" and predecessor["attempts"] == 1

    for name, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"stale validation input: {name}"
    assert sha256(LEAN_ROOT / "lean-toolchain") == TOOLCHAIN_SHA256
    assert sha256(LEAN_ROOT / "lake-manifest.json") == MANIFEST_SHA256
    formal = statement["canonical_formal_target"]
    assert formal["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert formal["statement_file_sha256"] == EXPECTED_INPUTS["Statement.lean"]
    assert instance["root_vector"] == ROOT_VECTOR
    assert instance["accepted_proof_state"] == []
    assert instance["audit_complete"] is instance["theorem_complete"] is False
    assert registry["root_obligation_id"] == graphs["root_node_id"] == "M0510-ROOT"
    assert registry["denominator_sha256"] == graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    closure = graphs["closure_boundary"]
    assert closure["root_closed"] is False and closure["theorem_complete"] is False
    assert closure["root_machine_classification"] == "M3"

    assert proof_receipt["item_id"] == "S56-M-0510-PROOF"
    assert proof_receipt["proof_body"]["source_sha256"] == EXPECTED_INPUTS["Proof.lean"]
    assert proof_receipt["supported_obligation_ids"] == [EULER_OBLIGATION]
    assert proof_receipt["provisionally_closed_obligation_ids"] == [EULER_OBLIGATION]
    assert proof_receipt["accepted_closed_obligation_ids"] == []
    assert proof_receipt["accepted"] is False
    assert proof_receipt["result"]["root_kernel_closed"] is False
    assert proof_receipt["result"]["theorem_complete"] is False
    assert proof_receipt["remaining_root_cut_set"] == OPEN_ROOT_CUT
    assert proof_blocker["root_closed"] is proof_blocker["audit_complete"] is False
    assert proof_blocker["theorem_complete"] is False

    euler_node = next(node for node in graphs["nodes"] if node["obligation_id"] == EULER_OBLIGATION)
    assert euler_node["machine_debt"] == "M4" and euler_node["formal_target"].startswith("planned ")
    assert euler_node["evidence_ids"] == []
    terminal_node = next(node for node in graphs["nodes"] if node["obligation_id"] == "M0510-T-ASYMPTOTIC")
    assert terminal_node["machine_debt"] == "M0-L"
    assert terminal_node["human_statement"].startswith("Convert relative-error convergence")
    assert terminal_node["formal_target"] == "Stage1Instances.THM_M_0510.root_of_finalAsymptotic"
    terminal_registry = next(
        row for row in registry["obligations"] if row["obligation_id"] == "M0510-T-ASYMPTOTIC"
    )
    assert terminal_registry["terminal_proof_body_id"].endswith("#root_of_finalAsymptotic")
    tree_source = source_without_comments((HERE / "ObligationTree.lean").read_text(encoding="utf-8"))
    assert re.search(
        r"def FinalAsymptoticPackage\s*:\s*Prop\s*:=\s*HardyRamanujanAsymptoticTarget",
        tree_source,
    )
    assert re.search(
        r"theorem root_of_finalAsymptotic\s*\(h\s*:\s*FinalAsymptoticPackage\)\s*:\s*HardyRamanujanAsymptoticTarget\s*:=\s*by\s*exact h",
        tree_source,
    )
    assert "A tautological theorem assuming the asymptotic formula as a hypothesis." in (
        HERE / "scope-map.md"
    ).read_text(encoding="utf-8")

    assert legacy_specs["item_id"] == "S56-M-0510-OBLIGATION_TREE"
    assert all(
        set(recipe) == {"recipe_id", "obligation_id", "state", "required_checks"}
        for recipe in legacy_specs["recipes"]
    )

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|run_tac|implemented_by)\b|"
        r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
        r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
        r"(?:axiom|constant|opaque|unsafe|extern)\b",
        flags=re.MULTILINE,
    )
    all_source = "\n".join(
        source_without_comments((HERE / name).read_text(encoding="utf-8"))
        for name in ("Statement.lean", "Proof.lean", "Validation.lean")
    )
    assert prohibited.search(all_source) is None
    validation_source = (HERE / "Validation.lean").read_text(encoding="utf-8")
    validation_imports = validation_source.split("/-!", 1)[0]
    assert "import Proof" not in validation_imports and "import ObligationTree" not in validation_imports
    for fragment in (
        "theorem differentialCoeffValidationPartitionSeries",
        "theorem differentialOrdinaryPartitionSeriesMulEulerProduct",
        "Nat.Partition.hasProd_powerSeriesMk_card_restricted",
        "tsum_pow_mul_one_sub_of_constantCoeff_eq_zero",
        "assert_no_sorry differentialOrdinaryPartitionSeriesMulEulerProduct",
        "#print_validation_closure",
    ):
        assert fragment in validation_source, fragment

    manifest = load(LEAN_ROOT / "lake-manifest.json")
    mathlib_entry = next(row for row in manifest["packages"] if row["name"] == "mathlib")
    assert mathlib_entry["rev"] == mathlib_entry["inputRev"] == MATHLIB_REVISION
    assert mathlib_entry["url"] == MATHLIB_REMOTE
    assert (LEAN_ROOT / ".lake").is_symlink()
    mathlib = (LEAN_ROOT / ".lake/packages/mathlib").resolve()
    assert mathlib.is_dir()
    assert git("rev-parse", "HEAD", cwd=mathlib) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == MATHLIB_TREE
    assert git("status", "--porcelain=v1", "--untracked-files=all", cwd=mathlib) == ""
    assert git("remote", "get-url", "origin", cwd=mathlib) == MATHLIB_REMOTE
    assert sha256(mathlib / "LICENSE") == MATHLIB_LICENSE_SHA256
    for relative, expected in SOURCE_BOUNDARIES.items():
        source = mathlib / relative
        olean = mathlib / ".lake/build/lib/lean" / Path(relative).with_suffix(".olean")
        tree_entry = git("ls-tree", "HEAD", relative, cwd=mathlib).split()
        assert tree_entry == ["100644", "blob", expected["blob"], relative]
        assert sha256(source) == expected["source_sha256"]
        assert sha256(olean) == expected["olean_sha256"]
        assert olean.stat().st_size == expected["olean_bytes"]

    lean = Path(run(["lake", "env", "which", "lean"], cwd=LEAN_ROOT, env=BASE_ENV).strip())
    lake = Path(run(["lake", "env", "which", "lake"], cwd=LEAN_ROOT, env=BASE_ENV).strip())
    bwrap = Path("/usr/bin/bwrap")
    assert sha256(lean) == LEAN_SHA256 and sha256(lake) == LAKE_SHA256
    assert sha256(bwrap) == BWRAP_SHA256
    assert sha256(Path("/usr/bin/python3")) == PYTHON_SHA256
    assert sha256(Path("/usr/bin/git")) == GIT_SHA256
    assert sha256(Path(HOME) / ".elan/bin/lake") == ELAN_LAUNCHER_SHA256
    assert LEAN_COMMIT in run([str(lean), "--version"], env=BASE_ENV)
    lean_path = pinned_lean_path(lean)
    outputs = isolated_replay(lean, bwrap, lean_path)

    assert "error:" not in outputs["statement"]
    for declaration in PROOF_DECLARATIONS:
        assert reported_axioms(outputs["proof"], declaration) == EXPECTED_AXIOMS
    assert "sorryAx" not in outputs["proof"] and "declaration uses 'sorry'" not in outputs["proof"]
    assert "Declarations are sorry-free!" in outputs["validation"]
    for declaration in VALIDATION_DECLARATIONS:
        assert reported_axioms(outputs["validation"], declaration) == EXPECTED_AXIOMS
    closure_match = re.search(
        r"VALIDATION_CLOSURE declarations=(\d+) modules=(\d+)", outputs["validation"]
    )
    assert closure_match and tuple(map(int, closure_match.groups())) == (16524, 617)
    assert "VALIDATION_CLOSURE axioms=[propext, Classical.choice, Quot.sound]" in outputs["validation"]
    assert "VALIDATION_CLOSURE bodyless_nonaxioms=[]" in outputs["validation"]
    assert "VALIDATION_CLOSURE unsafe=[]" in outputs["validation"]
    assert "sorryAx" not in outputs["validation"]

    if args.probe:
        print(json.dumps({
            "lean_output_sha256": {
                name: hashlib.sha256(output.encode()).hexdigest()
                for name, output in outputs.items()
            },
            "validation_closure": {
                "declarations": 16524,
                "modules": 617,
                "bodyless_nonaxioms": [],
                "unsafe_declarations": [],
            },
            "observed_axioms": sorted(EXPECTED_AXIOMS),
        }, sort_keys=True))
        return

    spec = load(HERE / "validation-phase-spec.json")
    receipt = load(HERE / "validation-receipt.json")
    assert spec["item_id"] == receipt["item_id"] == ITEM
    assert spec["theorem_id"] == receipt["theorem_id"] == THEOREM
    assert spec["depends_on"] == receipt["depends_on"] == ["S56-M-0510-PROOF"]
    assert len(spec["recipes"]) == 1 and receipt["recipe"] == spec["recipes"][0]
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["verdict"] == "blocked" and receipt["release_grade"] is False
    assert receipt["result"]["root_kernel_closed"] is False
    assert receipt["result"]["accepted_closed_obligation_ids"] == []
    assert receipt["result"]["audit_complete"] is False
    assert receipt["result"]["theorem_complete"] is False
    assert receipt["result"]["structured_terminal_transport_gate"] == "fail_closed_semantic_mismatch"
    assert receipt["known_failures"]

    hash_paths = {
        "lean-toolchain": LEAN_ROOT / "lean-toolchain",
        "lake-manifest.json": LEAN_ROOT / "lake-manifest.json",
    }
    hash_paths.update({name: HERE / name for name in receipt["inputs"] if name not in hash_paths})
    for name, expected in receipt["inputs"].items():
        assert sha256(hash_paths[name]) == expected, f"stale receipt input: {name}"

    assert receipt["result"]["lean_output_sha256"] == {
        name: hashlib.sha256(output.encode()).hexdigest() for name, output in outputs.items()
    }
    assert receipt["output_evidence"]["stdout_semantic_sha256"] == hashlib.sha256(
        ("\n".join(SUMMARY_LINES) + "\n").encode()
    ).hexdigest()
    assert receipt["output_evidence"]["expected_line_count"] == len(SUMMARY_LINES)

    if args.worker_packet is None:
        raise AssertionError("--worker-packet is required outside --probe mode")
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
    actual_changed = sorted(
        line[3:] for line in status.splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    )
    assert actual_changed == sorted(CHANGED_PATHS), (actual_changed, CHANGED_PATHS)
    for relative in CHANGED_PATHS:
        assert_text_hygiene(ROOT / relative)

    print("\n".join(SUMMARY_LINES))


if __name__ == "__main__":
    main()
