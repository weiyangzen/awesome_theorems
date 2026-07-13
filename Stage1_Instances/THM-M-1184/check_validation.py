#!/usr/bin/env python3
"""Fail-closed local validator for S56-M-1184-VALIDATION."""

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
HERE = ROOT / "Stage1_Instances" / "THM-M-1184"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
ITEM = "S56-M-1184-VALIDATION"
THEOREM = "THM-M-1184"
BASE_REVISION = "3bb4cb3ae15dff8b48c93242019edec3bf858e48"
BASE_TREE = "8e911f5a101bd92eb0951794fa0d9a3c0c3a2ddc"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
LEAN_SHA256 = "3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf"
LAKE_SHA256 = "a608ff084d7e2af228b92a29d7c2fd083ba0580e46889175ec74a81678c98359"
TOOLCHAIN_SHA256 = "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2"
MANIFEST_SHA256 = "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_REMOTE = "https://github.com/leanprover-community/mathlib4.git"
MATHLIB_LICENSE_SHA256 = "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1"
STATEMENT_EXPRESSION_SHA256 = "edb496494c51e51e63988c1b32c3fd639f1c911af60db1557a364968ff01cc29"
DENOMINATOR_SHA256 = "4626bc02bb751442b67f842fd1e77a79210940bdd405134d5b14c41f1ff07e27"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
WEAK_IDS = [
    "M1184-C-PRODUCT",
    "M1184-C-CONSTANT",
    "M1184-W-INTEGRATE",
    "M1184-W-ORDER",
    "M1184-T-WEAK",
]
OPEN_STRONG_IDS = [
    "M1184-S-SEPARATION",
    "M1184-C-POTENTIALS",
    "M1184-L-GAP",
    "M1184-W-REVERSE",
    "M1184-T-STRONG",
]

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
    source = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
    return re.sub(r"--.*$", "", source, flags=re.MULTILINE)


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
    "execution_rank": 169,
    "phase": "validation",
    "layer": 5,
    "state": "[ ]",
    "depends_on": ["S56-M-1184-PROOF"],
    "owned_paths": [f"Stage1_Instances/{THEOREM}"],
    "deliverable": "Run hermetic kernel, trust, provenance, and independent validation gates.",
    "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
    "attempts": 0,
    "children": [],
}
predecessor = next(row for row in execution["items"] if row["id"] == "S56-M-1184-PROOF")
assert predecessor["state"] == "[_]" and predecessor["attempts"] == 1

assert spec["schema_version"] == "stage1-validation-spec/1.0"
assert spec["item_id"] == ITEM and spec["theorem_id"] == THEOREM
assert spec["argv"] == ["python3", "-I", "-B", str(HERE.relative_to(ROOT) / "check_validation.py")]
assert spec["cwd"] == "." and spec["network_policy"] == "denied"
assert spec["expected_exit"] == 0 and spec["timeout_seconds"] == 300
assert len(spec["covered_obligation_ids"]) == len(set(spec["covered_obligation_ids"]))
if receipt is not None:
    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["accepted"] is False and receipt["release_grade"] is False
    assert receipt["inputs"]["validation_spec_sha256"] == sha256(HERE / "validation-spec.json")
    assert receipt["inputs"]["validator_sha256"] == sha256(Path(__file__).resolve())
    assert receipt["inputs"]["validation_probe_sha256"] == sha256(HERE / "Validation.lean")
    assert receipt["result"]["root_closed"] is False
    assert receipt["result"]["theorem_complete"] is False

assert statement["canonical_formal_target"]["statement_file_sha256"] == sha256(HERE / "Statement.lean")
assert statement["canonical_formal_target"]["elaborated_expression_sha256"] == STATEMENT_EXPRESSION_SHA256
assert registry["frozen_against_statement_sha256"] == sha256(HERE / "Statement.lean")
assert registry["denominator_sha256"] == graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
assert registry["root_obligation_id"] == graphs["root_node_id"] == "M1184-ROOT"
assert proof_receipt["proof_body"]["source_sha256"] == sha256(HERE / "Proof.lean")
assert proof_receipt["inputs"]["Statement.lean"] == sha256(HERE / "Statement.lean")
assert proof_receipt["inputs"]["ObligationTree.lean"] == sha256(HERE / "ObligationTree.lean")
assert proof_receipt["inputs"]["obligation-registry.json"] == sha256(HERE / "obligation-registry.json")
assert proof_receipt["inputs"]["typed-graphs.json"] == sha256(HERE / "typed-graphs.json")
assert proof_receipt["inputs"]["anchor-audit.json"] == sha256(HERE / "anchor-audit.json")
assert proof_receipt["provisionally_closed_obligation_ids"] == WEAK_IDS
assert proof_receipt["remaining_root_cut_set"] == OPEN_STRONG_IDS
assert proof_receipt["accepted"] is False
assert proof_receipt["result"]["weak_package_kernel_closed"] is True
assert proof_receipt["result"]["root_kernel_closed"] is False
assert proof_receipt["result"]["theorem_complete"] is False

node_ids = {node["obligation_id"] for node in graphs["nodes"]}
assert node_ids == {node["obligation_id"] for node in registry["obligations"]}
root = next(node for node in graphs["nodes"] if node["obligation_id"] == "M1184-ROOT")
foundation = next(node for node in graphs["nodes"] if node["obligation_id"] == "M1184-S-FOUNDATION")
provenance = next(node for node in graphs["nodes"] if node["obligation_id"] == "M1184-X-PROVENANCE")
assert root["machine_debt"] == "M2" and root["validity"]["revocation_state"] == "open"
assert foundation["machine_debt"] == provenance["machine_debt"] == "M4"
assert graphs["closure_boundary"] == {
    "root_closed": False,
    "audit_complete": False,
    "theorem_complete": False,
    "root_vector": ["H3", "M2", "R4"],
    "reason": "Both exact inequality packages and all release overlays remain unaccepted.",
}

all_source = "\n".join(
    source_without_comments((HERE / name).read_text(encoding="utf-8"))
    for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean")
)
for pattern in (
    r"\bsorry\b",
    r"\badmit\b",
    r"\bsorryAx\b",
    r"^[ \t]*(?:axiom|unsafe|opaque|extern)\b",
    r"\bimplemented_by\b",
    r"\bnative_decide\b",
):
    assert re.search(pattern, all_source, re.MULTILINE) is None, pattern
validation_imports = (HERE / "Validation.lean").read_text(encoding="utf-8").split("/-!", 1)[0]
assert "import Proof" not in validation_imports
assert "import ObligationTree" not in validation_imports

mathlib = LEAN_ROOT / ".lake" / "packages" / "mathlib"
assert mathlib.resolve().is_dir()
assert git("rev-parse", "HEAD", cwd=mathlib) == MATHLIB_REVISION
assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == MATHLIB_TREE
assert git("status", "--porcelain=v1", "--untracked-files=all", cwd=mathlib) == ""
assert git("remote", "get-url", "origin", cwd=mathlib) == MATHLIB_REMOTE
assert sha256(mathlib / "LICENSE") == MATHLIB_LICENSE_SHA256
assert sha256(LEAN_ROOT / "lean-toolchain") == TOOLCHAIN_SHA256
assert sha256(LEAN_ROOT / "lake-manifest.json") == MANIFEST_SHA256

fixed_env = os.environ.copy()
fixed_env.update(
    {
        "ELAN_TOOLCHAIN": "leanprover/lean4:v4.29.0",
        "LANG": "C.UTF-8",
        "LC_ALL": "C.UTF-8",
        "TZ": "UTC",
        "LEAN_NUM_THREADS": "1",
    }
)
lean = Path(run(["lake", "env", "which", "lean"], cwd=LEAN_ROOT, env=fixed_env).strip())
lake = Path(run(["lake", "env", "which", "lake"], cwd=LEAN_ROOT, env=fixed_env).strip())
assert sha256(lean) == LEAN_SHA256 and sha256(lake) == LAKE_SHA256
assert LEAN_COMMIT in run([str(lean), "--version"], cwd=LEAN_ROOT, env=fixed_env)
assert "5.0.0" in run([str(lake), "--version"], cwd=LEAN_ROOT, env=fixed_env)
lean_path = run(["lake", "env", "printenv", "LEAN_PATH"], cwd=LEAN_ROOT, env=fixed_env).strip()

tmp = Path(tempfile.mkdtemp(prefix="stage1-m1184-validation-", dir="/tmp"))
try:
    for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
        shutil.copy2(HERE / name, tmp / name)
    replay_env = fixed_env.copy()
    replay_env["LEAN_PATH"] = lean_path
    bwrap = shutil.which("bwrap")
    assert bwrap is not None, "bubblewrap network isolation is unavailable"

    def isolated_lean(args: list[str], *, module_path: bool = False) -> str:
        path = f"{tmp}:{lean_path}" if module_path else lean_path
        return run(
            [
                bwrap,
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
                "--setenv", "LEAN_NUM_THREADS", "2",
                "--setenv", "LEAN_PATH", path,
                "--chdir", str(tmp),
                str(lean),
                "--trust=0",
                *args,
            ],
            cwd=ROOT,
            env=replay_env,
        )

    (tmp / "home").mkdir()
    statement_output = isolated_lean(["-o", "Statement.olean", "Statement.lean"])
    obligation_output = isolated_lean(["-o", "ObligationTree.olean", "ObligationTree.lean"], module_path=True)
    proof_output = isolated_lean(["Proof.lean"], module_path=True)
    validation_output = isolated_lean(["Validation.lean"], module_path=True)
finally:
    shutil.rmtree(tmp)

assert "sorryAx" not in "\n".join((statement_output, obligation_output, proof_output, validation_output))
assert "Declarations are sorry-free!" in validation_output
for declaration in (
    "Stage1Instances.THM_M_1184.root_of_duality_packages",
    "Stage1Instances.THM_M_1184.productCoupling",
    "Stage1Instances.THM_M_1184.integral_fst_of_coupling",
    "Stage1Instances.THM_M_1184.integral_snd_of_coupling",
    "Stage1Instances.THM_M_1184.dualValue_le_primalValue",
    "Stage1Instances.THM_M_1184.constantDualPair_nonempty",
    "Stage1Instances.THM_M_1184.objectiveRanges_wellFounded",
    "Stage1Instances.THM_M_1184.weakDuality",
    "Stage1Instances.THM_M_1184.kantorovichDuality_of_reverse",
):
    output = obligation_output if declaration.endswith("root_of_duality_packages") else proof_output
    assert reported_axioms(output, declaration) == EXPECTED_AXIOMS
assert reported_axioms(
    validation_output,
    "Stage1Instances.THM_M_1184.Validation.differentialWeakDuality",
) == EXPECTED_AXIOMS

summary = (
    "PASS S56-M-1184-VALIDATION: trust-zero network-isolated fresh-output replay "
    "checked the exact statement, conditional composition, local weak branch, and "
    "same-worker differential weak branch; observed axioms are exactly propext, "
    "Classical.choice, and Quot.sound; root remains M2 with reverse branch open; "
    "complete TCB/provenance, cold empty-cache, and distinct-runner gates fail closed"
)
print(summary)
