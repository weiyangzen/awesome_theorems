#!/usr/bin/env python3
"""Fail-closed local validator for S56-M-1138-VALIDATION."""

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
HERE = ROOT / "Stage1_Instances" / "THM-M-1138"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
ITEM = "S56-M-1138-VALIDATION"
THEOREM = "THM-M-1138"
BASE_REVISION = "499a718cc7926abaf61e9721fe0d7485059403e6"
BASE_TREE = "ed2a23c0266f4d921ad97562392226015eee80be"
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
FLT_REGULAR_REVISION = "56161b6eb5281fbfe9c38f2bcec0f429ebc11a27"
STATEMENT_EXPRESSION_SHA256 = "7ae115564e67b7065344d9b323240a2694c3f1f1f01640d1b542dcc2152f4f5c"
DENOMINATOR_SHA256 = "a2093825a633069dc09fc9bf1597396052d7f9272bb33f44ace551aa7ba1ca49"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
WITHHELD_ROUTE_IDS = {
    "M1138-C-CLOSURE-MAXIMIZER",
    "M1138-B-MAXIMIZER-LOCATION",
    "M1138-L-INTERIOR-LOCAL",
    "M1138-L-CONNECTED-PROPAGATION",
    "M1138-L-CONTINUITY-EXTENSION",
}
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/check_validation.py",
    f"Stage1_Instances/{THEOREM}/validation-phase.md",
    f"Stage1_Instances/{THEOREM}/validation-receipt.json",
    f"Stage1_Instances/{THEOREM}/validation-spec.json",
}
SOURCE_PROVENANCE = {
    "Mathlib/Analysis/Calculus/DerivativeTest.lean": {
        "source_sha256": "4d89b7883a04a373e0dc4d73b0163a7542a690249d9316509701e96074fb7dbb",
        "git_blob": "de697940d455520137948b48e506e2377b14f5a3",
        "olean_sha256": "e16cab82cfcf4ca5b58c533ee745886cfd088b745aca3efb4231cb58ad731a8a",
    },
    "Mathlib/Analysis/InnerProductSpace/Calculus.lean": {
        "source_sha256": "695878ec0ba211d9027445a28f4474ed5716237a1bf960d34375f7233b4906e5",
        "git_blob": "efec86444df931af495584ae8a6f4a39e9abe9b1",
        "olean_sha256": "3582d6dae6ed23f5a39cb31d8c61530a6e3d6a6300deaa474ba6d8b70237ff24",
    },
    "Mathlib/Topology/Connected/Clopen.lean": {
        "source_sha256": "41977a3ba127bb92d2fe8099836fb72330c1f91986ce0a9e905af9b454abad7b",
        "git_blob": "1f9dafd93b92a9deb9f4b898c532e46787e17f38",
        "olean_sha256": "eca19fae13a3183a1336f169e1c8fa6a1941e5760888a6107c9df1606ebcad03",
    },
    "Mathlib/Analysis/InnerProductSpace/Harmonic/HarmonicContOnCl.lean": {
        "source_sha256": "33aefdda3bea8d84225fa77525ab4b4a84751f7492d261a2920c517022f32278",
        "git_blob": "d885a8372fc7e1116d0bce17d29371ec1c9fdc56",
        "olean_sha256": "0c40b3ba1110b09488512b7ec89dcab5db90898f53838563fbff9155c90415d4",
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

    result = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates)
    assert isinstance(result, dict), path
    return result


def run(
    argv: list[str],
    *,
    cwd: Path = ROOT,
    env: dict[str, str] | None = None,
    timeout: int = 600,
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
            f"command exited {result.returncode}, expected {expected_exit}: {argv!r}\n{result.stdout}"
        )
    return result.stdout


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["git", *args], cwd=cwd).rstrip()


def source_without_comments(source: str) -> str:
    """Remove nested Lean comments and line comments before defense-in-depth scans."""
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


spec = load(HERE / "validation-spec.json")
statement = load(HERE / "statement.json")
anchor = load(HERE / "anchor-audit.json")
registry = load(HERE / "obligation-registry.json")
graphs = load(HERE / "typed-graphs.json")
frozen_specs = load(HERE / "validation-specs.json")
proof_receipt = load(HERE / "proof-receipt.json")
execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")
receipt_path = HERE / "validation-receipt.json"
receipt = load(receipt_path) if receipt_path.exists() else None

assert git("rev-parse", "HEAD") == BASE_REVISION
assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
item = next(row for row in execution["items"] if row["id"] == ITEM)
assert item == {
    "id": ITEM,
    "theorem_id": THEOREM,
    "execution_rank": 343,
    "phase": "validation",
    "layer": 5,
    "state": "[ ]",
    "depends_on": ["S56-M-1138-PROOF"],
    "owned_paths": [f"Stage1_Instances/{THEOREM}"],
    "deliverable": "Run hermetic kernel, trust, provenance, and independent validation gates.",
    "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
    "attempts": 0,
    "children": [],
}
predecessor = next(row for row in execution["items"] if row["id"] == "S56-M-1138-PROOF")
assert predecessor["state"] == "[_]" and predecessor["attempts"] == 1

assert spec["schema_version"] == "stage1-validation-recipe/1.0"
assert spec["item_id"] == ITEM and spec["theorem_id"] == THEOREM
assert spec["argv"] == [
    "python3", "-I", "-B", f"Stage1_Instances/{THEOREM}/check_validation.py"
]
assert spec["cwd"] == "." and spec["network_policy"] == "denied"
assert spec["expected_exit"] == 0 and spec["timeout_seconds"] == 600
assert len(spec["covered_obligation_ids"]) == len(set(spec["covered_obligation_ids"]))
if receipt is not None:
    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["accepted"] is False and receipt["release_grade"] is False
    assert receipt["verdict"] == "blocked" and receipt["proposed_state"] == "[_]"
    assert receipt["inputs"]["validation-spec.json"] == sha256(HERE / "validation-spec.json")
    assert receipt["inputs"]["check_validation.py"] == sha256(Path(__file__).resolve())
    assert receipt["result"]["accepted_root_closed"] is False
    assert receipt["result"]["theorem_complete"] is False
    assert set(receipt["changed_paths"]) == CHANGED_PATHS
    assert receipt["recipe"]["recipe_id"] == spec["recipe_id"]
    for key in (
        "cwd", "argv", "env_allowlist", "timeout_seconds", "network_policy",
        "expected_exit", "covered_obligation_ids", "covered_declarations",
    ):
        assert receipt["recipe"][key] == spec[key]
    expected_stdout = (
        "PASS S56-M-1138-VALIDATION: network-isolated lake env lean --trust=0 fresh-output "
        "replay checked the exact statement, conditional composition, and local perturbation "
        "root; both proof declarations are sorry-free with exactly propext, Classical.choice, "
        "and Quot.sound; frozen route reconciliation, complete TCB/provenance, cold empty-cache, "
        "and independent-verification gates fail closed\n"
    )
    assert receipt["recipe"]["stdout_semantic_sha256"] == hashlib.sha256(
        expected_stdout.encode("utf-8")
    ).hexdigest()
    recorded_untracked = receipt["nonrelease_input_set"]["untracked_input_sha256"]
    for relative, digest in recorded_untracked.items():
        assert sha256(ROOT / relative) == digest

assert statement["statement_file_sha256"] == sha256(HERE / "Statement.lean")
assert statement["elaborated_expression_sha256"] == STATEMENT_EXPRESSION_SHA256
assert registry["frozen_against_statement_sha256"] == sha256(HERE / "Statement.lean")
assert registry["frozen_against_anchor_audit_sha256"] == sha256(HERE / "anchor-audit.json")
assert registry["denominator_sha256"] == graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
assert registry["root_obligation_id"] == graphs["root_node_id"] == "M1138-ROOT"
assert proof_receipt["proof_body"]["source_sha256"] == sha256(HERE / "Proof.lean")
proof_inputs = {
    "statement_sha256": "Statement.lean",
    "obligation_tree_sha256": "ObligationTree.lean",
    "obligation_registry_sha256": "obligation-registry.json",
    "typed_graphs_sha256": "typed-graphs.json",
    "anchor_audit_sha256": "anchor-audit.json",
    "validation_specs_sha256": "validation-specs.json",
}
for key, name in proof_inputs.items():
    assert proof_receipt["inputs"][key] == sha256(HERE / name)
assert proof_receipt["accepted"] is False and proof_receipt["content_addressed"] is False
assert proof_receipt["result"]["root_kernel_closed"] is True
assert proof_receipt["result"]["accepted_root_closed"] is False
assert proof_receipt["theorem_complete"] is False
assert set(proof_receipt["root_evidence"]["withheld_frozen_route_ids"]) == WITHHELD_ROUTE_IDS
assert proof_receipt["root_evidence"]["foundation_credit_withheld"] is True

assert frozen_specs["item_id"] == "S56-M-1138-OBLIGATION_TREE"
assert len(frozen_specs["recipes"]) == 15
assert {
    tuple(recipe["argv"]) for recipe in frozen_specs["recipes"]
} == {("python3", f"Stage1_Instances/{THEOREM}/check_obligation_tree.py")}
assert "not open analytic proofs" in frozen_specs["status_boundary"]
assert graphs["closure_boundary"] == {
    "closed_obligations": ["M1138-S-DEFINITIONS", "M1138-T-ROOT-TRANSPORT"],
    "root_closed": False,
    "theorem_complete": False,
    "remaining_root_cut_set": ["M1138-T-BOUNDARY-MAX"],
    "root_machine_debt": "M3",
}
root_node = next(node for node in graphs["nodes"] if node["obligation_id"] == "M1138-ROOT")
foundation_node = next(
    node for node in graphs["nodes"] if node["obligation_id"] == "M1138-S-FOUNDATION"
)
provenance_node = next(
    node for node in graphs["nodes"] if node["obligation_id"] == "M1138-X-PROVENANCE"
)
assert root_node["machine_debt"] == "M3"
assert foundation_node["machine_debt"] == provenance_node["machine_debt"] == "M4"
assert all(row["exact_root_closure"] is False for row in anchor["candidates"])

sources = ("Statement.lean", "ObligationTree.lean", "Proof.lean")
all_source = "\n".join(
    source_without_comments((HERE / name).read_text(encoding="utf-8")) for name in sources
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
mathlib = LEAN_ROOT / ".lake" / "packages" / "mathlib"
assert mathlib.resolve().is_dir()
assert git("rev-parse", "HEAD", cwd=mathlib) == MATHLIB_REVISION
assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == MATHLIB_TREE
assert git("status", "--porcelain=v1", "--untracked-files=all", cwd=mathlib) == ""
assert git("remote", "get-url", "origin", cwd=mathlib) == MATHLIB_REMOTE
assert sha256(mathlib / "LICENSE") == MATHLIB_LICENSE_SHA256
assert sha256(LEAN_ROOT / "lean-toolchain") == TOOLCHAIN_SHA256
assert sha256(LEAN_ROOT / "lake-manifest.json") == MANIFEST_SHA256
for source, expected in SOURCE_PROVENANCE.items():
    source_path = mathlib / source
    olean_path = mathlib / ".lake" / "build" / "lib" / "lean" / source.replace(".lean", ".olean")
    assert sha256(source_path) == expected["source_sha256"]
    assert git("rev-parse", f"HEAD:{source}", cwd=mathlib) == expected["git_blob"]
    assert sha256(olean_path) == expected["olean_sha256"]

flt_regular = LEAN_ROOT / ".lake" / "packages" / "flt-regular"
assert flt_regular.resolve().is_dir()
assert run(
    ["git", "-C", str(flt_regular), "cat-file", "-e", f"{FLT_REGULAR_REVISION}^{{commit}}"]
) == ""
assert git("rev-parse", "HEAD", cwd=flt_regular) == FLT_REGULAR_REVISION
assert git("status", "--porcelain=v1", "--untracked-files=all", cwd=flt_regular) == ""
assert not (flt_regular / ".lake" / "build" / "lib" / "lean").exists()

fixed_env = os.environ.copy()
fixed_env.update({
    "ELAN_TOOLCHAIN": LEAN_TOOLCHAIN,
    "LANG": "C.UTF-8",
    "LC_ALL": "C.UTF-8",
    "TZ": "UTC",
    "LEAN_NUM_THREADS": "1",
})
toolchain_root = Path.home() / ".elan" / "toolchains" / "leanprover--lean4---v4.29.0"
lean = toolchain_root / "bin" / "lean"
lake = toolchain_root / "bin" / "lake"
bwrap = Path(shutil.which("bwrap") or "")
assert lean.is_file() and lake.is_file() and bwrap.is_file()
assert sha256(lean) == LEAN_SHA256 and sha256(lake) == LAKE_SHA256
assert sha256(bwrap) == BWRAP_SHA256
assert LEAN_COMMIT in run([str(lean), "--version"], env=fixed_env)
assert "5.0.0" in run([str(lake), "--version"], env=fixed_env)

compiled_dirs = sorted(
    path.resolve()
    for path in (LEAN_ROOT / ".lake" / "packages").glob("*/.lake/build/lib/lean")
    if path.is_dir()
)
project_compiled = (LEAN_ROOT / ".lake" / "build" / "lib" / "lean").resolve()
assert project_compiled.is_dir()
compiled_dirs.append(project_compiled)
assert all("flt-regular" not in str(path) for path in compiled_dirs)
lean_path = ":".join(str(path) for path in compiled_dirs)

tmp = Path(tempfile.mkdtemp(prefix="stage1-m1138-validation-", dir="/tmp"))
try:
    for name in sources:
        shutil.copy2(HERE / name, tmp / name)
    (tmp / "home").mkdir()

    def isolated_lake_lean(args: list[str], *, module_path: bool = False) -> str:
        path = f"{tmp}:{lean_path}" if module_path else lean_path
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
                str(lake),
                "env",
                "lean",
                "--trust=0",
                "--root", str(tmp),
                *args,
            ],
            cwd=ROOT,
            env=fixed_env,
        )

    statement_output = isolated_lake_lean(["-o", "Statement.olean", "Statement.lean"])
    obligation_output = isolated_lake_lean(
        ["-o", "ObligationTree.olean", "ObligationTree.lean"], module_path=True
    )
    proof_output = isolated_lake_lean(["Proof.lean"], module_path=True)
finally:
    shutil.rmtree(tmp)

combined_output = "\n".join((statement_output, obligation_output, proof_output))
assert "sorryAx" not in combined_output
assert proof_output.count("Declarations are sorry-free!") == 2
assert reported_axioms(
    obligation_output, "Stage1Instances.THM_M_1138.root_of_boundaryMaximumPackage"
) == EXPECTED_AXIOMS
for declaration in (
    "Stage1Instances.THM_M_1138.Proof.boundaryMaximumPackage",
    "Stage1Instances.THM_M_1138.Proof.harmonicWeakMaximumPrinciple",
):
    assert reported_axioms(proof_output, declaration) == EXPECTED_AXIOMS
selftest_path = ROOT / ".stage1-worker-selftest.json"
if selftest_path.exists():
    selftest = load(selftest_path)
    assert set(selftest) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert selftest["item_id"] == ITEM and selftest["state"] == "[_]"
    assert selftest["base_revision"] == BASE_REVISION
    assert set(selftest["changed_paths"]) == CHANGED_PATHS
    assert receipt is not None
    assert selftest["known_failures"] == receipt["known_failures"]
    status = git("status", "--short", "--untracked-files=all")
    actual_changes = {
        line[3:] for line in status.splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual_changes == CHANGED_PATHS, (actual_changes, CHANGED_PATHS)

for relative in CHANGED_PATHS:
    path = ROOT / relative
    data = path.read_bytes()
    assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines()), path

summary = (
    "PASS S56-M-1138-VALIDATION: network-isolated lake env lean --trust=0 fresh-output "
    "replay checked the exact statement, conditional composition, and local perturbation root; "
    "both proof declarations are sorry-free with exactly propext, Classical.choice, and "
    "Quot.sound; frozen route reconciliation, complete TCB/provenance, cold empty-cache, and "
    "independent-verification gates fail closed"
)
print(summary)
