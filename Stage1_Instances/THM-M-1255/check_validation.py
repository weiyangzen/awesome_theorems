#!/usr/bin/env python3
"""Fail-closed local validator for S56-M-1255-VALIDATION."""

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
HERE = ROOT / "Stage1_Instances" / "THM-M-1255"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
ITEM = "S56-M-1255-VALIDATION"
THEOREM = "THM-M-1255"
BASE_REVISION = "bad90e2e2479d376609447202eb4f437789d0d11"
BASE_TREE = "df3ade7b4d06057f8aac33369c3d69bd391aa05a"
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
STATEMENT_EXPRESSION_SHA256 = "0ea54a511c4baf6d8bfacb7e784833be9ca4faef66bf1c736765465ed65ad3cf"
DENOMINATOR_SHA256 = "7cbea3ad9b0c61388cb73afed61f64984ca5670e061dc3a966a7d6599411c2c9"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
FROZEN_CLOSED_IDS = ["M1255-S-DEFINITIONS", "M1255-T-ASSEMBLE"]
PROVISIONAL_PROOF_IDS = ["M1255-L-COMMUTE", "M1255-C-ACTION"]
FROZEN_OPEN_CUT = ["M1255-C-ACTION", "M1255-C-FUNDSOL"]
PROPOSED_OPEN_CUT = ["M1255-C-FUNDSOL"]
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/Validation.lean",
    f"Stage1_Instances/{THEOREM}/check_validation.py",
    f"Stage1_Instances/{THEOREM}/validation-phase.md",
    f"Stage1_Instances/{THEOREM}/validation-receipt.json",
    f"Stage1_Instances/{THEOREM}/validation-spec.json",
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
    timeout: int = 300,
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
    return run(["git", *args], cwd=cwd).rstrip()


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
    pattern = re.compile(
        rf"'{re.escape(declaration)}' depends on axioms:\s*\[(?P<axioms>.*?)\]",
        re.DOTALL,
    )
    match = pattern.search(output)
    assert match is not None, f"missing axiom report for {declaration}"
    return {part.strip() for part in match.group("axioms").split(",") if part.strip()}


spec = load(HERE / "validation-spec.json")
statement = load(HERE / "statement.json")
registry = load(HERE / "obligation-registry.json")
graphs = load(HERE / "typed-graphs.json")
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
    "execution_rank": 160,
    "phase": "validation",
    "layer": 5,
    "state": "[ ]",
    "depends_on": ["S56-M-1255-PROOF"],
    "owned_paths": [f"Stage1_Instances/{THEOREM}"],
    "deliverable": "Run hermetic kernel, trust, provenance, and independent validation gates.",
    "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
    "attempts": 0,
    "children": [],
}
predecessor = next(row for row in execution["items"] if row["id"] == "S56-M-1255-PROOF")
assert predecessor["state"] == "[_]" and predecessor["attempts"] == 1

assert spec["schema_version"] == "stage1-validation-spec/1.0"
assert spec["item_id"] == ITEM and spec["theorem_id"] == THEOREM
assert spec["argv"] == [
    "python3", "-I", "-B", str(HERE.relative_to(ROOT) / "check_validation.py")
]
assert spec["cwd"] == "." and spec["network_policy"] == "denied"
assert spec["expected_exit"] == 0 and spec["timeout_seconds"] == 1200
assert "bubblewrap --unshare-net" in spec["network_enforcement"]
assert spec["env_allowlist"] == {
    "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8", "TZ": "UTC", "LEAN_NUM_THREADS": "1"
}
assert spec["covered_obligation_ids"] == [
    "M1255-S-DEFINITIONS", "M1255-L-COMMUTE", "M1255-C-ACTION", "M1255-T-ASSEMBLE"
]
assert set(spec["audited_open_obligation_ids"]) == (
    {row["obligation_id"] for row in registry["obligations"]}
    - set(spec["covered_obligation_ids"])
)

if receipt is not None:
    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["accepted"] is False and receipt["release_grade"] is False
    assert receipt["inputs"]["validation_spec_sha256"] == sha256(HERE / "validation-spec.json")
    assert receipt["inputs"]["validator_sha256"] == sha256(Path(__file__).resolve())
    assert receipt["inputs"]["validation_probe_sha256"] == sha256(HERE / "Validation.lean")
    assert receipt["result"]["root_closed"] is False
    assert receipt["result"]["theorem_complete"] is False
    assert set(receipt["changed_paths"]) == CHANGED_PATHS

canonical = statement["canonical_formal_target"]
assert canonical["statement_file_sha256"] == sha256(HERE / "Statement.lean")
assert canonical["elaborated_expression_sha256"] == STATEMENT_EXPRESSION_SHA256
assert registry["frozen_against_statement_sha256"] == sha256(HERE / "Statement.lean")
assert registry["frozen_against_anchor_audit_sha256"] == sha256(HERE / "anchor-audit.json")
assert registry["denominator_sha256"] == graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
assert registry["root_obligation_id"] == graphs["root_node_id"] == "M1255-ROOT"
assert proof_receipt["proof_body"]["source_sha256"] == sha256(HERE / "Proof.lean")
assert proof_receipt["inputs"]["statement_sha256"] == sha256(HERE / "Statement.lean")
assert proof_receipt["inputs"]["obligation_tree_sha256"] == sha256(HERE / "ObligationTree.lean")
assert proof_receipt["inputs"]["obligation_registry_sha256"] == sha256(HERE / "obligation-registry.json")
assert proof_receipt["inputs"]["typed_graphs_sha256"] == sha256(HERE / "typed-graphs.json")
assert proof_receipt["closed_obligation_ids"] == PROVISIONAL_PROOF_IDS
assert proof_receipt["accepted_closed_obligation_ids"] == []
assert proof_receipt["remaining_root_cut_set"] == PROPOSED_OPEN_CUT
assert proof_receipt["result"]["root_closed"] is False
assert proof_receipt["result"]["theorem_complete"] is False

node_ids = {node["obligation_id"] for node in graphs["nodes"]}
assert node_ids == {node["obligation_id"] for node in registry["obligations"]}
nodes = {node["obligation_id"]: node for node in graphs["nodes"]}
assert nodes["M1255-ROOT"]["machine_debt"] == "M3"
assert nodes["M1255-S-FOUNDATION"]["machine_debt"] == "M4"
assert nodes["M1255-X-PROVENANCE"]["machine_debt"] == "M4"
assert nodes["M1255-X-SOURCE"]["human_debt"] == "H1"
assert graphs["closure_boundary"]["closed_obligations"] == FROZEN_CLOSED_IDS
assert graphs["closure_boundary"]["remaining_root_cut_set"] == FROZEN_OPEN_CUT
assert graphs["closure_boundary"]["root_closed"] is False
assert graphs["closure_boundary"]["audit_complete"] is False
assert graphs["closure_boundary"]["theorem_complete"] is False

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
validation_imports = (HERE / "Validation.lean").read_text(encoding="utf-8").split("/-!", 1)[0]
assert "import Proof" not in validation_imports
assert "import ObligationTree" not in validation_imports
assert "import Statement" in validation_imports
obligation_source = source_without_comments((HERE / "ObligationTree.lean").read_text(encoding="utf-8"))
assert "import Statement" not in obligation_source.split("namespace", 1)[0]
assert "def MalgrangeEhrenpreisTarget" in obligation_source

mathlib = LEAN_ROOT / ".lake" / "packages" / "mathlib"
assert mathlib.resolve().is_dir()
assert git("rev-parse", "HEAD", cwd=mathlib) == MATHLIB_REVISION
assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == MATHLIB_TREE
assert git("status", "--porcelain=v1", "--untracked-files=all", cwd=mathlib) == ""
assert git("remote", "get-url", "origin", cwd=mathlib) == MATHLIB_REMOTE
assert sha256(mathlib / "LICENSE") == MATHLIB_LICENSE_SHA256
assert sha256(LEAN_ROOT / "lean-toolchain") == TOOLCHAIN_SHA256
assert sha256(LEAN_ROOT / "lake-manifest.json") == MANIFEST_SHA256

manifest = load(LEAN_ROOT / "lake-manifest.json")
for package in manifest["packages"]:
    name = package["name"].strip("«»")
    package_dir = (LEAN_ROOT / ".lake" / "packages" / name).resolve()
    assert package_dir.is_dir(), f"pinned package is missing: {name}"
    assert git("rev-parse", "HEAD", cwd=package_dir) == package["rev"]
    assert git("status", "--porcelain=v1", "--untracked-files=all", cwd=package_dir) == ""

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
bwrap = Path(shutil.which("bwrap") or "")
assert lean.is_file() and lake.is_file() and bwrap.is_file()
assert sha256(lean) == LEAN_SHA256
assert sha256(lake) == LAKE_SHA256
assert sha256(bwrap) == BWRAP_SHA256
assert LEAN_COMMIT in run([str(lean), "--version"], cwd=LEAN_ROOT, env=fixed_env)
assert "5.0.0" in run([str(lake), "--version"], cwd=LEAN_ROOT, env=fixed_env)
lean_path = run(["lake", "env", "printenv", "LEAN_PATH"], cwd=LEAN_ROOT, env=fixed_env).strip()

tmp = Path(tempfile.mkdtemp(prefix="stage1-m1255-validation-", dir="/tmp"))
try:
    for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
        shutil.copy2(HERE / name, tmp / name)
    (tmp / "home").mkdir()
    replay_env = fixed_env.copy()
    replay_env["LEAN_PATH"] = lean_path

    def isolated_lean(args: list[str], *, module_path: bool = False) -> str:
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
                "--clearenv",
                "--setenv", "HOME", str(tmp / "home"),
                "--setenv", "LANG", "C.UTF-8",
                "--setenv", "LC_ALL", "C.UTF-8",
                "--setenv", "TZ", "UTC",
                "--setenv", "LEAN_NUM_THREADS", "1",
                "--setenv", "LEAN_PATH", path,
                "--chdir", str(tmp),
                str(lean),
                "--trust=0",
                "-t0",
                *args,
            ],
            cwd=ROOT,
            env=replay_env,
        )

    statement_output = isolated_lean(["-o", "Statement.olean", "Statement.lean"])
    validation_output = isolated_lean(["Validation.lean"], module_path=True)
    # ObligationTree deliberately duplicates the statement namespace and must be replayed separately.
    (tmp / "Statement.olean").unlink()
    obligation_output = isolated_lean(["-o", "ObligationTree.olean", "ObligationTree.lean"])
    proof_output = isolated_lean(["Proof.lean"], module_path=True)
finally:
    shutil.rmtree(tmp)

combined_output = "\n".join((statement_output, validation_output, obligation_output, proof_output))
assert "sorryAx" not in combined_output
assert "Declarations are sorry-free!" in validation_output
assert reported_axioms(
    obligation_output,
    "Stage1Instances.THM_M_1255.root_of_action_and_fundamental_packages",
) == EXPECTED_AXIOMS
for declaration in (
    "Stage1Instances.THM_M_1255.Proof.coordinateDerivatives_commute",
    "Stage1Instances.THM_M_1255.Proof.exponentAction_single",
    "Stage1Instances.THM_M_1255.Proof.polynomialAction_map_X",
    "Stage1Instances.THM_M_1255.Proof.polynomialActionPackage",
):
    assert reported_axioms(proof_output, declaration) == EXPECTED_AXIOMS
for declaration in (
    "Stage1Instances.THM_M_1255.Validation.differentialCoordinateDerivativesCommute",
    "Stage1Instances.THM_M_1255.Validation.differentialPolynomialActionExists",
):
    assert reported_axioms(validation_output, declaration) == EXPECTED_AXIOMS

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

summary = (
    "PASS S56-M-1255-VALIDATION: trust-zero network-isolated fresh-output replay "
    "checked the canonical statement, conditional composition, local commutation/action bodies, "
    "and a same-worker canonical differential reconstruction; observed axioms are exactly "
    "propext, Classical.choice, and Quot.sound; the fundamental-solution root branch remains open, "
    "and exact module linkage, complete TCB/provenance, cold empty-cache, and distinct-runner gates "
    "fail closed"
)
print(summary)
