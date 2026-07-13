#!/usr/bin/env python3
"""Fail-closed narrow validation for S56-M-0405-VALIDATION."""

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
HERE = ROOT / "Stage1_Instances" / "THM-M-0405"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
ITEM = "S56-M-0405-VALIDATION"
THEOREM = "THM-M-0405"
BASE_REVISION = "09a2e94f8f331e8fa7938c55db7dddafb47a6c74"
BASE_TREE = "31b53f41ab005b6c095c80080147c15a11077149"
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
STATEMENT_SHA256 = "db2edf61040b73d00d4d3ab2b7dc227b6ec418793400bf79ac86edc79aa18da1"
DENOMINATOR_SHA256 = "cd9daee4b82734d1e98e216a6371bd83f3fcff1a181e79381773133a6b9da793"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
PROOF_DECLARATIONS = (
    "ne_of_ratioNotRootOfUnity",
    "LucasPair.alpha_ne_zero",
    "LucasPair.beta_ne_zero",
    "LucasPair.alpha_ne_beta",
    "LucasPair.denominator_ne_zero",
    "LucasPair.coe_discriminant",
    "LucasPair.term_zero",
    "LucasPair.term_one",
    "LehmerPair.alpha_ne_zero",
    "LehmerPair.beta_ne_zero",
    "LehmerPair.alpha_ne_beta",
    "LehmerPair.oddDenominator_ne_zero",
    "LehmerPair.add_ne_zero",
    "LehmerPair.sq_sub_sq_ne_zero",
    "LehmerPair.coe_discriminant",
    "LehmerPair.coe_squaredEvenDenominator",
    "LehmerPair.term_one",
    "LehmerPair.term_two",
)
VALIDATION_DECLARATIONS = (
    "lucas_beta_ne_zero",
    "lucas_alpha_ne_beta",
    "lucas_term_zero",
    "lucas_term_one",
)
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


spec = load(HERE / "validation-spec.json")
statement = load(HERE / "statement.json")
registry = load(HERE / "obligation-registry.json")
graphs = load(HERE / "typed-graphs.json")
proof_receipt = load(HERE / "proof-receipt.json")
proof_blocker = load(HERE / "proof-blocker.json")
execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")
receipt_path = HERE / "validation-receipt.json"
receipt = load(receipt_path) if receipt_path.exists() else None

assert git("rev-parse", "HEAD") == BASE_REVISION
assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
item = next(row for row in execution["items"] if row["id"] == ITEM)
assert item == {
    "id": ITEM,
    "theorem_id": THEOREM,
    "execution_rank": 18,
    "phase": "validation",
    "layer": 5,
    "state": "[ ]",
    "depends_on": ["S56-M-0405-PROOF"],
    "owned_paths": [f"Stage1_Instances/{THEOREM}"],
    "deliverable": "Run hermetic kernel, trust, provenance, and independent validation gates.",
    "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
    "attempts": 0,
    "children": [],
}
predecessor = next(row for row in execution["items"] if row["id"] == "S56-M-0405-PROOF")
assert predecessor["state"] == "[_]" and predecessor["attempts"] == 1

assert spec["schema_version"] == "stage1-validation-spec/1.0"
assert spec["item_id"] == ITEM and spec["theorem_id"] == THEOREM
assert spec["argv"] == [
    "python3", "-I", "-B", "Stage1_Instances/THM-M-0405/check_validation.py"
]
assert spec["cwd"] == "." and spec["network_policy"] == "denied"
assert spec["expected_exit"] == 0 and spec["timeout_seconds"] == 300
assert len(spec["covered_obligation_ids"]) == len(set(spec["covered_obligation_ids"]))
if receipt is not None:
    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["release_grade"] is False
    assert receipt["inputs"]["validation_spec_sha256"] == sha256(HERE / "validation-spec.json")
    assert receipt["inputs"]["validator_sha256"] == sha256(Path(__file__).resolve())
    assert receipt["inputs"]["validation_probe_sha256"] == sha256(HERE / "Validation.lean")
    assert receipt["recipe"] == {
        key: spec[key]
        for key in (
            "recipe_id", "cwd", "argv", "env_allowlist",
            "timeout_seconds", "network_policy", "expected_exit",
        )
    }
    assert receipt["result"]["root_closed"] is False
    assert receipt["result"]["theorem_complete"] is False
    assert receipt["result"]["supported_obligation_ids"] == []
    assert receipt["result"]["provisionally_closed_obligation_ids"] == []
    assert receipt["result"]["accepted_closed_obligation_ids"] == []
    assert receipt["result"]["minimal_open_root_cut_set"] == ["M0405-X-BHV-BRIDGE"]
    assert receipt["first_failed_gate"].startswith("dependency.S56-M-0405-PROOF")
    assert set(receipt["changed_paths"]) == CHANGED_PATHS

assert sha256(HERE / "Statement.lean") == STATEMENT_SHA256
assert statement["statement_sha256"] == STATEMENT_SHA256
assert registry["denominator_sha256"] == DENOMINATOR_SHA256
assert registry["status_observed_after_freeze"] == {
    "closed_obligations": [],
    "root_machine_debt": "M4",
}
assert graphs["registry_id"] == registry["registry_id"]
closure = graphs["closure_boundary"]
assert closure["root_machine_debt"] == "M4"
assert closure["closed_obligations"] == []
assert closure["minimal_open_root_cut_set"] == ["M0405-X-BHV-BRIDGE"]
assert closure["theorem_complete"] is False and closure["audit_complete"] is False
root_node = next(node for node in graphs["nodes"] if node["node_id"] == "M0405-ROOT")
assert root_node["human_debt"] == "H1"
assert root_node["machine_debt"] == "M4"
assert root_node["readability_debt"] == "R3"

assert proof_receipt["support_state"] == "provisional_worker_selftest"
assert proof_receipt["accepted"] is False
assert proof_receipt["supported_obligation_ids"] == []
assert proof_receipt["provisionally_closed_obligation_ids"] == []
assert proof_receipt["accepted_closed_obligation_ids"] == []
assert proof_receipt["proof_body"]["source_sha256"] == sha256(HERE / "Proof.lean")
for key, name in (
    ("statement_sha256", "Statement.lean"),
    ("obligation_tree_sha256", "ObligationTree.lean"),
    ("obligation_registry_sha256", "obligation-registry.json"),
    ("typed_graphs_sha256", "typed-graphs.json"),
    ("anchor_audit_sha256", "anchor-audit.json"),
    ("proof_blocker_sha256", "proof-blocker.json"),
):
    assert proof_receipt["inputs"][key] == sha256(HERE / name), key
assert proof_receipt["result"]["root_kernel_closed"] is False
assert proof_receipt["result"]["theorem_complete"] is False
assert proof_receipt["remaining_root_cut_set"] == ["M0405-X-BHV-BRIDGE"]
assert proof_blocker["supported_obligation_ids"] == []
assert proof_blocker["root_closed"] is False
assert proof_blocker["theorem_complete"] is False

all_source = "\n".join(
    source_without_comments((HERE / name).read_text(encoding="utf-8"))
    for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean")
)
prohibited = re.compile(
    r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by)\b|"
    r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
    r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
    r"(?:axiom|constant|opaque|unsafe|extern)\b",
    re.MULTILINE,
)
assert prohibited.search(all_source) is None
validation_imports = (HERE / "Validation.lean").read_text(encoding="utf-8").split("/-!", 1)[0]
assert "import Proof" not in validation_imports
assert "import ObligationTree" not in validation_imports
assert "theorem proof : Statement" not in all_source

manifest = load(LEAN_ROOT / "lake-manifest.json")
mathlib_entry = next(row for row in manifest["packages"] if row["name"] == "mathlib")
assert mathlib_entry["rev"] == mathlib_entry["inputRev"] == MATHLIB_REVISION
mathlib = LEAN_ROOT / ".lake" / "packages" / "mathlib"
assert mathlib.resolve().is_dir()
assert git("rev-parse", "HEAD", cwd=mathlib) == MATHLIB_REVISION
assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == MATHLIB_TREE
assert git("remote", "get-url", "origin", cwd=mathlib) == MATHLIB_REMOTE
assert git("status", "--porcelain=v1", "--untracked-files=all", cwd=mathlib) == ""
assert sha256(mathlib / "LICENSE") == MATHLIB_LICENSE_SHA256
assert sha256(LEAN_ROOT / "lean-toolchain") == TOOLCHAIN_SHA256
assert sha256(LEAN_ROOT / "lake-manifest.json") == MANIFEST_SHA256

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
lean_path = run(["lake", "env", "printenv", "LEAN_PATH"], cwd=LEAN_ROOT, env=fixed_env).strip()
bwrap = Path(shutil.which("bwrap") or "")
assert lean.is_file() and lake.is_file() and bwrap.is_file()
assert sha256(lean) == LEAN_SHA256 and sha256(lake) == LAKE_SHA256
assert sha256(bwrap) == BWRAP_SHA256
assert LEAN_COMMIT in run([str(lean), "--version"], cwd=LEAN_ROOT, env=fixed_env)

tmp = Path(tempfile.mkdtemp(prefix="stage1-m0405-validation-", dir="/tmp"))
try:
    for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
        shutil.copy2(HERE / name, tmp / name)
    (tmp / "home").mkdir()

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
                "--setenv", "HOME", str(tmp / "home"),
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
                *args,
            ],
            env=fixed_env,
        )

    statement_output = isolated_lean(["-o", "Statement.olean", "Statement.lean"])
    obligation_output = isolated_lean(
        ["-o", "ObligationTree.olean", "ObligationTree.lean"], module_path=True
    )
    proof_output = isolated_lean(["-o", "Proof.olean", "Proof.lean"], module_path=True)
    validation_output = isolated_lean(["Validation.lean"], module_path=True)
finally:
    shutil.rmtree(tmp)

for short_name in ("statement_of_branches", "lucasBranch_of_statement", "lehmerBranch_of_statement"):
    declaration = "Stage1.THM_M_0405." + short_name
    assert reported_axioms(obligation_output, declaration) <= EXPECTED_AXIOMS
for short_name in PROOF_DECLARATIONS:
    declaration = "Stage1.THM_M_0405." + short_name
    assert reported_axioms(proof_output, declaration) <= EXPECTED_AXIOMS
for short_name in VALIDATION_DECLARATIONS:
    declaration = "Stage1.THM_M_0405.Validation." + short_name
    assert reported_axioms(validation_output, declaration) <= EXPECTED_AXIOMS
assert validation_output.count("Declarations are sorry-free!") == len(VALIDATION_DECLARATIONS)
combined_output = "\n".join((statement_output, obligation_output, proof_output, validation_output))
assert "sorryAx" not in combined_output
assert "declaration uses 'sorry'" not in combined_output
assert "error:" not in combined_output

selftest_path = ROOT / ".stage1-worker-selftest.json"
if selftest_path.exists():
    packet = load(selftest_path)
    assert set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert packet["item_id"] == ITEM and packet["state"] == "[_]"
    assert packet["base_revision"] == BASE_REVISION
    assert set(packet["changed_paths"]) == CHANGED_PATHS
    assert receipt is not None and packet["known_failures"] == receipt["known_failures"]
    actual_changes = {
        line[3:] for line in run(
            ["git", "status", "--short", "--untracked-files=all"]
        ).splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual_changes == CHANGED_PATHS, (actual_changes, CHANGED_PATHS)

print("PASS THM-M-0405 network-isolated trust-zero narrow kernel replay")
print("PASS 18 proof declarations and 4 differential declarations use only the selected classical axiom subset")
print("PASS frozen hashes, placeholder scan, pinned mathlib provenance, and honest open-M4 boundary")
print("OPEN M0405-X-BHV-BRIDGE; hermetic release and distinct-runner independent verification fail closed")
