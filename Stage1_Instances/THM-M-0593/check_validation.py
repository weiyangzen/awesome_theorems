#!/usr/bin/env python3
"""Fail-closed local validator for S56-M-0593-VALIDATION."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0593"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
ITEM = "S56-M-0593-VALIDATION"
THEOREM = "THM-M-0593"
BASE_REVISION = "799262a53af4c03d919b758421e149ffc158d472"
BASE_TREE = "c95932dffb536335b0a3f5c962f13966e755cbde"
LEAN_TOOLCHAIN = "leanprover/lean4:v4.29.0"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
LEAN_SHA256 = "3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf"
LAKE_SHA256 = "a608ff084d7e2af228b92a29d7c2fd083ba0580e46889175ec74a81678c98359"
BWRAP_SHA256 = "0abea81db798ebf6b4742ac0664802d97521547a353c2a0dbdc21d76cbbfd2c0"
TOOLCHAIN_SHA256 = "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2"
MANIFEST_SHA256 = "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_REMOTE = "https://github.com/leanprover-community/mathlib4.git"
MATHLIB_LICENSE_SHA256 = "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1"
REGISTRY_DENOMINATOR_SHA256 = (
    "ff56394a72695c35f72ed72fc1c961a3297943517a2e8b8056047678fb1157e2"
)
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
FROZEN_CUT = {
    "M0593-L-DIMENSION-IMAGE",
    "M0593-L-RANK-REDUCTION",
    "M0593-L-TAYLOR",
}
PROVISIONAL_CUT = {"M0593-L-RANK-REDUCTION", "M0593-L-TAYLOR"}
PROVISIONALLY_VALIDATED = {
    "M0593-B-ZERO",
    "M0593-L-DIMENSION-IMAGE",
    "M0593-B-LOWDIM",
    "M0593-B-MERGE",
}
PROOF_DECLARATIONS = {
    "Stage1Instances.THMM0593.zeroCodomainBranch_proof",
    "Stage1Instances.THMM0593.lowDimensionBranch_proof",
    "Stage1Instances.THMM0593.sardTarget_of_hardDimensionBranch",
}
VALIDATION_DECLARATIONS = {
    "Stage1Instances.THMM0593.Validation.exactRoot_iff_frozen",
    "Stage1Instances.THMM0593.Validation.zeroCodomainBranch_validation",
    "Stage1Instances.THMM0593.Validation.conditionalExactRoot",
}
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/Validation.lean",
    f"Stage1_Instances/{THEOREM}/check_validation.py",
    f"Stage1_Instances/{THEOREM}/validation-phase.md",
    f"Stage1_Instances/{THEOREM}/validation-receipt.json",
    f"Stage1_Instances/{THEOREM}/validation-spec.json",
}
SOURCE_PROVENANCE = {
    "Mathlib/Geometry/Euclidean/Volume/Measure.lean": {
        "source_sha256": "788fc731877fa7c3ef3dbb98a6498487c612fa349ead5392affd84f21020e826",
        "git_blob": "81ffa4f2dfc640f16ff431c6a1ad3179d28f4c53",
        "olean": ".lake/build/lib/lean/Mathlib/Geometry/Euclidean/Volume/Measure.olean",
        "olean_sha256": "87b0825c811af0f9544c213c90cc233dd68e1a0194533d7da08d45cb173dd6d0",
    },
    "Mathlib/Topology/MetricSpace/HausdorffDimension.lean": {
        "source_sha256": "162211066ffe08483b097d6fbc6217883ead50dd0e0ba0593ae9bca8c4abb9ab",
        "git_blob": "952706543399fe31e1351bfb4b51959d7302a096",
        "olean": ".lake/build/lib/lean/Mathlib/Topology/MetricSpace/HausdorffDimension.olean",
        "olean_sha256": "ccbc0f46c01a99fba9ec57011e854e6dd97862d230933eb145486a6e46692f14",
    },
    "Mathlib/Analysis/Calculus/ContDiff/RCLike.lean": {
        "source_sha256": "0e9c4170d6565e8a783df2f48adba8094496d253ad38289e748d9e94f7c0f8f3",
        "git_blob": "7688c3c93600890ee63e520634f0dd43f1d89951",
        "olean": ".lake/build/lib/lean/Mathlib/Analysis/Calculus/ContDiff/RCLike.olean",
        "olean_sha256": "e8a17ea8d70e5b924d81cd5956d13a6ef019ae340a1330bbd0284d8ae7550cc3",
    },
}

if not __debug__:
    raise RuntimeError("validation requires Python assertions")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path) -> dict:
    def reject_duplicates(pairs: list[tuple[str, object]]) -> dict:
        value: dict[str, object] = {}
        for key, item in pairs:
            assert key not in value, f"duplicate JSON key in {path}: {key}"
            value[key] = item
        return value

    result = json.loads(
        path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates
    )
    assert isinstance(result, dict), path
    return result


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
        raise RuntimeError(
            f"command exited {result.returncode}: {argv!r}\n{result.stdout}"
        )
    return result.stdout


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["git", *args], cwd=cwd).rstrip()


def source_without_comments(source: str) -> str:
    """Remove nested block comments and line comments before source scans."""
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


def axiom_report(output: str, declaration: str) -> set[str]:
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


spec = load(HERE / "validation-spec.json")
receipt = load(HERE / "validation-receipt.json")
registry = load(HERE / "obligation-registry.json")
graphs = load(HERE / "typed-graphs.json")
frozen_specs = load(HERE / "validation-specs.json")
proof_receipt = load(HERE / "proof-receipt.json")
proof_blocker = load(HERE / "proof-blocker.json")
execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")
selftest = load(ROOT / ".stage1-worker-selftest.json")

assert git("rev-parse", "HEAD") == BASE_REVISION
assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
item = next(row for row in execution["items"] if row["id"] == ITEM)
assert item == {
    "id": ITEM,
    "theorem_id": THEOREM,
    "execution_rank": 633,
    "phase": "validation",
    "layer": 5,
    "state": "[ ]",
    "depends_on": ["S56-M-0593-PROOF"],
    "owned_paths": [f"Stage1_Instances/{THEOREM}"],
    "deliverable": "Run hermetic kernel, trust, provenance, and independent validation gates.",
    "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
    "attempts": 0,
    "children": [],
}
predecessor = next(
    row for row in execution["items"] if row["id"] == "S56-M-0593-PROOF"
)
assert predecessor["state"] == "[_]" and predecessor["attempts"] == 1

assert spec["schema_version"] == "stage1-validation-spec/1.0"
assert spec["item_id"] == receipt["item_id"] == ITEM
assert spec["theorem_id"] == receipt["theorem_id"] == THEOREM
assert spec["argv"] == [
    "python3", "-I", "-B", f"Stage1_Instances/{THEOREM}/check_validation.py"
]
assert spec["cwd"] == "." and spec["network_policy"] == "denied"
assert spec["expected_exit"] == 0 and spec["timeout_seconds"] == 600
assert len(spec["covered_obligation_ids"]) == len(
    set(spec["covered_obligation_ids"])
)
assert set(spec["covered_declarations"]) == (
    PROOF_DECLARATIONS
    | VALIDATION_DECLARATIONS
    | {"Stage1Instances.THMM0593.root_of_sard_branches"}
)
assert receipt["base_revision"] == BASE_REVISION
assert receipt["base_tree"] == BASE_TREE
assert receipt["support_state"] == "provisional_worker_selftest"
assert receipt["proposed_state"] == "[_]"
assert receipt["accepted"] is False and receipt["release_grade"] is False
assert receipt["verdict"] == "blocked"
assert set(receipt["changed_paths"]) == CHANGED_PATHS
for key in (
    "recipe_id", "cwd", "argv", "env_allowlist", "timeout_seconds",
    "network_policy", "network_enforcement", "expected_exit",
    "expected_outputs", "covered_obligation_ids", "covered_declarations",
):
    assert receipt["recipe"][key] == spec[key]

input_files = {
    "Statement.lean": "dd2a4da4f6cb0b0723a656e627378047834867641d63c6e5a8a0255108aed3bb",
    "ObligationTree.lean": "84825c4e8ad670f722de2e90fd611cc1d91d67dab7de7e25f05df13395b70361",
    "Proof.lean": "3c9faedbdfcaf6afe7b803ba7580be018484650acb303f944c94464be28a0f79",
    "obligation-registry.json": "8be92d406d2a4e156cadf35573336a87987148d2e97027d2943613e56160f023",
    "typed-graphs.json": "5078835c04577c4b186307fe798e5e05a85d4d1f74ade0317d97f4dd2fa4a0b7",
    "proof-receipt.json": "7c1079f1daeaef5a438c382e3e300e850a049c597371867e1fea22d3c0dd8322",
    "proof-blocker.json": "3380871c659352fa2912d5b3c76d4846e3a48ba15f73923d83d9ea42f1a65cd2",
    "validation-specs.json": "be6b3b337d03a3f16439f519a1a93bfada54cc8129db35d40b30212d81526941",
    "anchor-audit.md": "4169509b09d08680e68933766c43b726e21b748e7cd0eaa07192f4a637950577",
    "source-statement-crosswalk.md": "8da88f93bd17cf4037e6b6994d2c21d7530767a90aaf43cdfdc4fa07a7f676a0",
}
for name, expected in input_files.items():
    assert sha256(HERE / name) == expected, f"stale validation input: {name}"
for relative, expected in receipt["inputs"].items():
    assert sha256(ROOT / relative) == expected, f"receipt input drift: {relative}"

assert registry["denominator_sha256"] == REGISTRY_DENOMINATOR_SHA256
assert registry["root_obligation_id"] == "M0593-ROOT"
assert graphs["registry_denominator_sha256"] == REGISTRY_DENOMINATOR_SHA256
closure = graphs["closure_boundary"]
assert closure["root_closed"] is False
assert closure["root_machine_debt"] == "M4"
assert closure["audit_complete"] is closure["theorem_complete"] is False
assert set(closure["remaining_root_cut_set"]) == FROZEN_CUT
assert frozen_specs["item_id"] == "S56-M-0593-OBLIGATION_TREE"
assert len(frozen_specs["recipes"]) == 22
assert {
    tuple(recipe["argv"]) for recipe in frozen_specs["recipes"]
} == {("python3", f"Stage1_Instances/{THEOREM}/check_obligation_tree.py")}

assert proof_receipt["item_id"] == "S56-M-0593-PROOF"
assert proof_receipt["support_state"] == "provisional_worker_selftest"
assert proof_receipt["proof_body"]["source_sha256"] == sha256(HERE / "Proof.lean")
for key, name in (
    ("statement_sha256", "Statement.lean"),
    ("obligation_tree_sha256", "ObligationTree.lean"),
    ("obligation_registry_sha256", "obligation-registry.json"),
    ("typed_graphs_sha256", "typed-graphs.json"),
):
    assert proof_receipt["inputs"][key] == sha256(HERE / name)
assert set(proof_receipt["closed_obligation_ids"]) == PROVISIONALLY_VALIDATED
assert proof_receipt["result"]["root_closed"] is False
assert proof_receipt["result"]["theorem_complete"] is False
assert set(proof_receipt["remaining_root_cut_set_after"]) == PROVISIONAL_CUT
assert proof_blocker["root_closed"] is proof_blocker["theorem_complete"] is False
assert proof_blocker["first_failed_gate"].startswith("M0593-B-HARD")
assert set(proof_blocker["remaining_root_cut_set"]) == PROVISIONAL_CUT

prohibited = re.compile(
    r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by)\b|"
    r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
    r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
    r"(?:axiom|constant|opaque|unsafe|extern)\b",
    re.MULTILINE,
)
for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
    source = source_without_comments((HERE / name).read_text(encoding="utf-8"))
    assert prohibited.search(source) is None, f"prohibited proof device in {name}"
validation_source = source_without_comments(
    (HERE / "Validation.lean").read_text(encoding="utf-8")
)
assert not re.search(r"^import (?:Proof|ObligationTree)$", validation_source, re.MULTILINE)
assert "Proof." not in validation_source and "ObligationTree." not in validation_source

assert sha256(LEAN_ROOT / "lean-toolchain") == TOOLCHAIN_SHA256
assert sha256(LEAN_ROOT / "lake-manifest.json") == MANIFEST_SHA256
manifest = load(LEAN_ROOT / "lake-manifest.json")
mathlib_entry = next(row for row in manifest["packages"] if row["name"] == "mathlib")
assert mathlib_entry["rev"] == mathlib_entry["inputRev"] == MATHLIB_REVISION
mathlib = (LEAN_ROOT / ".lake" / "packages" / "mathlib").resolve()
assert mathlib.is_dir(), "pinned mathlib artifacts unavailable"
assert git("rev-parse", "HEAD", cwd=mathlib) == MATHLIB_REVISION
assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == MATHLIB_TREE
assert git("remote", "get-url", "origin", cwd=mathlib) == MATHLIB_REMOTE
assert git("status", "--porcelain=v1", "--untracked-files=all", cwd=mathlib) == ""
assert sha256(mathlib / "LICENSE") == MATHLIB_LICENSE_SHA256
for source_name, record in SOURCE_PROVENANCE.items():
    source_path = mathlib / source_name
    assert sha256(source_path) == record["source_sha256"]
    assert git("rev-parse", f"HEAD:{source_name}", cwd=mathlib) == record["git_blob"]
    assert sha256(mathlib / record["olean"]) == record["olean_sha256"]

toolchain_root = Path.home() / ".elan" / "toolchains" / "leanprover--lean4---v4.29.0"
lean = toolchain_root / "bin" / "lean"
lake = toolchain_root / "bin" / "lake"
bwrap = Path(shutil.which("bwrap") or "")
assert lean.is_file() and lake.is_file() and bwrap.is_file()
assert sha256(lean) == LEAN_SHA256 and sha256(lake) == LAKE_SHA256
assert sha256(bwrap) == BWRAP_SHA256
assert LEAN_COMMIT in run([str(lean), "--version"], cwd=LEAN_ROOT)

package_lean_paths: list[Path] = []
for entry in manifest["packages"]:
    if entry.get("type") == "path":
        package = (LEAN_ROOT / entry["dir"]).resolve()
    else:
        package = (LEAN_ROOT / ".lake" / "packages" / entry["name"]).resolve()
    build_lib = package / ".lake" / "build" / "lib" / "lean"
    if build_lib.is_dir():
        package_lean_paths.append(build_lib)
local_build = LEAN_ROOT / ".lake" / "build" / "lib" / "lean"
if local_build.is_dir():
    package_lean_paths.append(local_build)
lean_path = ":".join(str(path) for path in package_lean_paths)
assert lean_path, "compiled pinned LEAN_PATH is unavailable"

tmp = Path(tempfile.mkdtemp(prefix="stage1-m0593-validation-", dir="/tmp"))
try:
    for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
        shutil.copy2(HERE / name, tmp / name)
    (tmp / "home").mkdir()

    def isolated_lean(source: str, *, output: str | None = None) -> str:
        env = {
            "HOME": str(tmp / "home"),
            "LANG": "C.UTF-8",
            "LC_ALL": "C.UTF-8",
            "TZ": "UTC",
            "LEAN_NUM_THREADS": "1",
            "LEAN_PATH": f"{tmp}:{lean_path}",
        }
        argv = [str(lean), "--trust=0", "-t0"]
        if output is not None:
            argv.extend(["-o", output])
        argv.append(source)
        return run(argv, cwd=tmp, env=env, timeout=600)

    statement_output = isolated_lean("Statement.lean", output="Statement.olean")
    obligation_output = isolated_lean(
        "ObligationTree.lean", output="ObligationTree.olean"
    )
    proof_output = isolated_lean("Proof.lean", output="Proof.olean")
    validation_output = isolated_lean("Validation.lean", output="Validation.olean")
finally:
    shutil.rmtree(tmp)

assert axiom_report(
    obligation_output, "Stage1Instances.THMM0593.root_of_sard_branches"
) == EXPECTED_AXIOMS
for declaration in PROOF_DECLARATIONS:
    assert axiom_report(proof_output, declaration) == EXPECTED_AXIOMS
for declaration in VALIDATION_DECLARATIONS:
    assert axiom_report(validation_output, declaration) <= EXPECTED_AXIOMS
assert proof_output.count("Declarations are sorry-free!") == 3
assert validation_output.count("Declarations are sorry-free!") == 3
all_output = statement_output + obligation_output + proof_output + validation_output
assert "sorryAx" not in all_output and "error:" not in all_output

assert receipt["result"]["accepted_root_closed"] is False
assert receipt["result"]["provisional_root_closed"] is False
assert receipt["result"]["theorem_complete"] is False
assert receipt["result"]["accepted_closed_obligation_ids"] == []
assert set(receipt["result"]["provisionally_validated_obligation_ids"]) == (
    PROVISIONALLY_VALIDATED
)
assert set(receipt["result"]["frozen_remaining_root_cut_set"]) == FROZEN_CUT
assert set(receipt["result"]["provisional_remaining_root_cut_set"]) == PROVISIONAL_CUT
assert receipt["result"]["hermetic_release_gate"] == "fail_closed"
assert receipt["result"]["complete_transitive_tcb_gate"] == "fail_closed"
assert receipt["result"]["independent_distinct_runner_gate"] == "fail_closed"

assert set(selftest) == {
    "item_id", "changed_paths", "commands", "output_summary",
    "base_revision", "known_failures", "state",
}
assert selftest["item_id"] == ITEM and selftest["state"] == "[_]"
assert selftest["base_revision"] == BASE_REVISION
assert set(selftest["changed_paths"]) == CHANGED_PATHS
assert selftest["known_failures"] == receipt["known_failures"]
status = git("status", "--short", "--untracked-files=all")
actual_changed = {
    line[3:] for line in status.splitlines()
    if line[3:] != "Formalizations/Lean/.lake"
}
assert actual_changed == CHANGED_PATHS, (actual_changed, CHANGED_PATHS)

print("PASS S56-M-0593-VALIDATION narrow nonrelease validation")
print("kernel: exact statement, conditional composition, two partial proof bodies, and same-worker differential probes replayed from fresh outputs with trust zero")
print("trust: seven declarations are sorry-free and report only propext, Classical.choice, and Quot.sound")
print("provenance: proof hashes, clean mathlib pin, selected source blobs, oleans, license, and tool digests agree")
print("root open: HardDimensionBranch is an explicit premise; accepted state remains H1/M4/R4 and theorem_complete=false")
print("blocked: root proof, enforced network isolation, complete TCB/provenance, cold empty-cache offline replay, and distinct-runner independent verification")
