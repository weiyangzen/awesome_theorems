#!/usr/bin/env python3
"""Fail-closed validation runner for S56-M-0325-VALIDATION."""

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
HERE = ROOT / "Stage1_Instances" / "THM-M-0325"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
ITEM = "S56-M-0325-VALIDATION"
THEOREM = "THM-M-0325"
BASE_REVISION = "dafb8b51c4561eee5fcf162a8d5ee49555584bdb"
BASE_TREE = "cca569d6bbc491441652aae678232353fb385a74"
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
EXPRESSION_SHA256 = "b4daa662b6b3f7cc1578975aeaf9fd097ef586b209bd0d26d4262c59ac59cf82"
DENOMINATOR_SHA256 = "4c41e44f32c7c300ac25319a49fd14dcf197599756525b2dec8dcdce4207703c"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
SOURCE_HASHES = {
    "Statement.lean": "a24ef5cd7e7ee64b388eeb36d2881c66f85630deca58f63440de5dd72098eb1e",
    "ObligationTree.lean": "224e289bd647e8154c50d2756d62bf72c8201ad48cde442d85ad7655da60abf8",
    "AnchorAudit.lean": "56f2a86f4be164368d65ccd893d7be0776876ef7653970ab41f95401c9d9719e",
    "Proof.lean": "3d1c12641a8d7f3cb5331c44079312ba4b80612d62e5ffedba645e9aa83d0a9a",
    "statement.json": "a6bee1f7353bf8963da181fd5ddc0ed73b7a193b9dce6d794795566dabf834e2",
    "anchor-audit.json": "fb87d78fbdb668ec985e9a104c48d38ee43ec4ab984a19fa8f79ec3785220d6e",
    "obligation-registry.json": "9afd64086d56f8fb871e3f5e48bf9d38a01cba7b3ac8e6dd544a0fcb99a9587b",
    "typed-graphs.json": "420e72dedc91e7545b64b158394c271e564de8b07437bcd67d57c22866fa0f8b",
    "validation-specs.json": "2662b619c16b1ba57b98ddc33d1acae395614ea94722d57dedf652e9c50afe02",
    "proof-receipt-slot35.json": "0953d0285eac48bdcd525eb381c3a1e7ea5f9be987ff413d5a3e2c72026d52d8",
    "proof-blocker-slot35.json": "803596496eb995ea523cb9428886bb1ff13bbd61d4ddddfaca5ca4ae539002de",
}
PARTIAL_DECLARATIONS = (
    "scalarUnitBoundedBy_apply",
    "scalarUnitBoundedBy_of_abs_eq_one",
    "nonneg_of_scalarUnitBoundedBy",
    "scalarMatrixForm_zero",
    "hilbertMatrixForm_zero",
    "zero_scalarUnitBoundedBy",
    "zero_hilbertUnitBoundedBy",
    "abs_real_inner_le_one_of_norm_le_one",
    "abs_matrix_inner_term_le",
    "abs_hilbertMatrixForm_le_sum_abs",
    "hilbertUnitBoundedBy_sum_abs",
)
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/check_validation.py",
    f"Stage1_Instances/{THEOREM}/validation-blocker.json",
    f"Stage1_Instances/{THEOREM}/validation-phase.md",
    f"Stage1_Instances/{THEOREM}/validation-receipt.json",
    f"Stage1_Instances/{THEOREM}/validation-spec.json",
}
KNOWN_FAILURES = [
    "The proof prerequisite is provisional and incomplete; its receipt closes no frozen obligation and no exact root body exists.",
    "M0325-K-TRANSFORM and seven other frozen analytic obligations remain open; the root stays M3 with cut M0325-T-PACKAGE.",
    "The foundation profile, complete transitive declaration provenance, imported compiled-object inventory, compiler/bootstrap, supply-chain, SBOM, and TCB closure are not accepted.",
    "The run reused the shared warm canonical .lake artifacts and is not a clean-checkout cold empty-cache offline replay.",
    "No second signed distinct-runner attestation or independently implemented minimal verifier exists.",
    "Primary-source H0, readable R0, AUDIT-Z, THEOREM-Z, release reconciliation, and master acceptance remain open.",
    "The target-local task-dag.json is a stale planned/open projection and has not been rewritten by this validation worker.",
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
    argv: list[str], *, cwd: Path = ROOT, env: dict[str, str] | None = None,
    timeout: int = 600, expected_exit: int = 0,
) -> str:
    result = subprocess.run(
        argv, cwd=cwd, env=env, text=True, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, timeout=timeout, check=False,
    )
    if result.returncode != expected_exit:
        raise RuntimeError(
            f"command exited {result.returncode}, expected {expected_exit}: {argv!r}\n{result.stdout}"
        )
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
        rf"'{re.escape(declaration)}' depends on axioms:\s*\[(?P<axioms>.*?)\]", re.DOTALL
    )
    matches = pattern.findall(output)
    assert output.count(no_axioms) + len(matches) == 1, f"bad axiom report for {declaration}"
    if not matches:
        return set()
    return {part.strip() for part in matches[0].split(",") if part.strip()}


def canonical_json_id(document: dict, omitted_field: str) -> str:
    body = dict(document)
    body.pop(omitted_field, None)
    payload = json.dumps(body, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return "sha256:" + hashlib.sha256(payload).hexdigest()


spec = load(HERE / "validation-spec.json")
statement = load(HERE / "statement.json")
registry = load(HERE / "obligation-registry.json")
graphs = load(HERE / "typed-graphs.json")
frozen_specs = load(HERE / "validation-specs.json")
proof_receipt = load(HERE / "proof-receipt-slot35.json")
proof_blocker = load(HERE / "proof-blocker-slot35.json")
execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")
receipt = load(HERE / "validation-receipt.json") if (HERE / "validation-receipt.json").exists() else None
blocker = load(HERE / "validation-blocker.json") if (HERE / "validation-blocker.json").exists() else None

assert git("rev-parse", "HEAD") == BASE_REVISION
assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
item = next(row for row in execution["items"] if row["id"] == ITEM)
assert item == {
    "id": ITEM,
    "theorem_id": THEOREM,
    "execution_rank": 214,
    "phase": "validation",
    "layer": 5,
    "state": "[ ]",
    "depends_on": ["S56-M-0325-PROOF"],
    "owned_paths": [f"Stage1_Instances/{THEOREM}"],
    "deliverable": "Run hermetic kernel, trust, provenance, and independent validation gates.",
    "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
    "attempts": 0,
    "children": [],
}
predecessor = next(row for row in execution["items"] if row["id"] == "S56-M-0325-PROOF")
assert predecessor["state"] == "[_]" and predecessor["attempts"] == 1

assert spec["schema_version"] == "stage1-validation-recipe/1.0"
assert spec["item_id"] == ITEM and spec["theorem_id"] == THEOREM
assert spec["argv"] == ["python3", "-I", "-B", f"Stage1_Instances/{THEOREM}/check_validation.py"]
assert spec["cwd"] == "." and spec["network_policy"] == "denied"
assert spec["expected_exit"] == 0 and spec["timeout_seconds"] == 600
assert spec["covered_obligation_ids"] == [
    "M0325-S-DEFINITIONS", "M0325-S-BOUNDARY", "M0325-T-ASSEMBLE"
]
expected_spec_declarations = [
    "Stage1Instances.THM_M_0325.target_iff_intakeSourceShape",
    "Stage1Instances.THM_M_0325.empty_scalar_boundary",
    "Stage1Instances.THM_M_0325.target_of_proofPackage",
    "Stage1Instances.THM_M_0325.auditedInjectiveLeProjective",
    *(f"Stage1Instances.THM_M_0325.{name}" for name in PARTIAL_DECLARATIONS),
]
assert spec["covered_declarations"] == expected_spec_declarations

for name, digest in SOURCE_HASHES.items():
    assert sha256(HERE / name) == digest, name
assert statement["canonical_formal_target"]["elaborated_expression_sha256"] == EXPRESSION_SHA256
assert statement["canonical_formal_target"]["statement_file_sha256"] == SOURCE_HASHES["Statement.lean"]
assert registry["denominator_sha256"] == graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
assert registry["root_obligation_id"] == graphs["root_node_id"] == "M0325-ROOT"
assert registry["status_observed_after_freeze"]["root_machine_debt"] == "M3"
assert graphs["closure_boundary"]["root_closed"] is False
assert graphs["closure_boundary"]["theorem_complete"] is False
assert graphs["closure_boundary"]["remaining_root_cut_set"] == ["M0325-T-PACKAGE"]
assert frozen_specs["item_id"] == "S56-M-0325-OBLIGATION_TREE"
assert {tuple(recipe["argv"]) for recipe in frozen_specs["recipes"]} == {
    ("python3", f"Stage1_Instances/{THEOREM}/check_obligation_tree.py")
}
assert proof_receipt["accepted"] is False
assert proof_receipt["supported_obligation_ids"] == []
assert proof_receipt["result"]["root_kernel_closed"] is False
assert proof_receipt["result"]["proof_phase_complete"] is False
assert proof_receipt["theorem_complete"] is False
assert proof_blocker["root_closed"] is False and proof_blocker["proof_phase_complete"] is False
assert proof_blocker["remaining_root_cut_set"] == ["M0325-T-PACKAGE"]
assert proof_blocker["first_failed_gate"].startswith("M0325-K-TRANSFORM:")

sources = ("Statement.lean", "ObligationTree.lean", "AnchorAudit.lean", "Proof.lean")
all_source = "\n".join(
    source_without_comments((HERE / name).read_text(encoding="utf-8")) for name in sources
)
for pattern in (
    r"\bsorry\b", r"\badmit\b", r"\bsorryAx\b",
    r"^[ \t]*(?:axiom|constant|unsafe|opaque|extern)\b",
    r"\bimplemented_by\b", r"\bnative_decide\b",
):
    assert re.search(pattern, all_source, re.MULTILINE) is None, pattern
assert "theorem proof : GrothendieckInequalityTarget" not in all_source
assert "theorem proof : GrothendieckProofPackage" not in all_source

mathlib = (LEAN_ROOT / ".lake" / "packages" / "mathlib").resolve()
assert mathlib.is_dir()
assert git("rev-parse", "HEAD", cwd=mathlib) == MATHLIB_REVISION
assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == MATHLIB_TREE
assert git("status", "--porcelain=v1", "--untracked-files=all", cwd=mathlib) == ""
assert git("remote", "get-url", "origin", cwd=mathlib) == MATHLIB_REMOTE
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
assert compiled_dirs and any("/mathlib/" in str(path) for path in compiled_dirs)
lean_path = ":".join(str(path) for path in compiled_dirs)

tmp = Path(tempfile.mkdtemp(prefix="stage1-m0325-validation-", dir="/tmp"))
try:
    for name in sources:
        shutil.copy2(HERE / name, tmp / name)
    (tmp / "home").mkdir()

    def isolated_lake_lean(name: str, *, module_path: bool) -> str:
        path = f"{tmp}:{lean_path}" if module_path else lean_path
        return run(
            [
                str(bwrap), "--ro-bind", "/", "/", "--bind", str(tmp), str(tmp),
                "--dev", "/dev", "--proc", "/proc", "--unshare-net", "--die-with-parent",
                "--setenv", "HOME", str(tmp / "home"),
                "--setenv", "ELAN_TOOLCHAIN", LEAN_TOOLCHAIN,
                "--setenv", "LANG", "C.UTF-8", "--setenv", "LC_ALL", "C.UTF-8",
                "--setenv", "TZ", "UTC", "--setenv", "LEAN_NUM_THREADS", "1",
                "--setenv", "LEAN_PATH", path, "--chdir", str(tmp),
                str(lake), "env", "lean", "--trust=0", "-t0", "--root", str(tmp),
                "-o", f"{Path(name).stem}.olean", name,
            ],
            env=fixed_env,
        )

    statement_output = isolated_lake_lean("Statement.lean", module_path=False)
    obligation_output = isolated_lake_lean("ObligationTree.lean", module_path=True)
    anchor_output = isolated_lake_lean("AnchorAudit.lean", module_path=False)
    proof_output = isolated_lake_lean("Proof.lean", module_path=True)
    olean_hashes = {
        name: sha256(tmp / name)
        for name in ("Statement.olean", "ObligationTree.olean", "AnchorAudit.olean", "Proof.olean")
    }
finally:
    shutil.rmtree(tmp)

combined_output = "\n".join((statement_output, obligation_output, anchor_output, proof_output))
assert "error:" not in combined_output and "declaration uses 'sorry'" not in combined_output
assert reported_axioms(
    obligation_output, "Stage1Instances.THM_M_0325.target_of_proofPackage"
) <= EXPECTED_AXIOMS
assert reported_axioms(
    anchor_output, "Stage1Instances.THM_M_0325.auditedInjectiveLeProjective"
) <= EXPECTED_AXIOMS
for short_name in PARTIAL_DECLARATIONS:
    assert reported_axioms(
        proof_output, f"Stage1Instances.THM_M_0325.{short_name}"
    ) <= EXPECTED_AXIOMS

expected_oleans = {
    "Statement.olean": "5da713d6cd67197fa4d54b69ee1ac0c6aebaec8d545748297800cf5f09ccdd7d",
    "ObligationTree.olean": "6588e3bc5a2d045319df89401047b1a133b7d5b0adc47bc8c44e9832931a7d2a",
    "AnchorAudit.olean": "7e864ef4728c00f185c095d830f32be1cfceedec398dfcdb367e9bbd48ced1d0",
    "Proof.olean": "3fb550337b224daed7bc786339a3da72f9dc440df0147b028ac2d144bfd6afc1",
}
assert olean_hashes == expected_oleans, olean_hashes

if receipt is not None:
    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["receipt_id"] == canonical_json_id(receipt, "receipt_id")
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["verdict"] == "blocked" and receipt["proposed_state"] == "[_]"
    assert receipt["accepted"] is False and receipt["release_grade"] is False
    assert receipt["result"]["root_kernel_closed"] is False
    assert receipt["result"]["theorem_complete"] is False
    assert receipt["result"]["olean_sha256"] == expected_oleans
    assert receipt["known_failures"] == KNOWN_FAILURES
    assert receipt["first_failed_gate"] == "dependency.S56-M-0325-PROOF.not_complete"
    assert receipt["remaining_root_cut_set"] == ["M0325-T-PACKAGE"]
    assert receipt["accepted_receipt_ids"] == []
    assert receipt["root_vector_before"] == receipt["root_vector_after"] == {
        "H": "H2", "M": "M3", "R": "R4"
    }
    for key in (
        "cwd", "argv", "env_allowlist", "timeout_seconds", "network_policy",
        "expected_exit", "expected_outputs", "covered_obligation_ids", "covered_declarations",
    ):
        assert receipt["recipe"][key] == spec[key]
    expected_stdout = (
        "PASS S56-M-0325-VALIDATION: network-isolated lake env lean --trust=0 fresh-output "
        "replay checked the statement, conditional composition, pinned anchor, and 11 partial local "
        "bodies; the proof dependency, exact root, complete trust/provenance, cold hermetic, and "
        "independent-verification gates fail closed\n"
    )
    assert receipt["recipe"]["stdout_semantic_sha256"] == hashlib.sha256(
        expected_stdout.encode("utf-8")
    ).hexdigest()
    assert set(receipt["changed_paths"]) == CHANGED_PATHS
    assert receipt["inputs"]["validation-spec.json"] == sha256(HERE / "validation-spec.json")
    assert receipt["inputs"]["check_validation.py"] == sha256(Path(__file__).resolve())
    recorded_untracked = receipt["nonrelease_input_set"]["owned_untracked_input_sha256"]
    for relative, digest in recorded_untracked.items():
        assert sha256(ROOT / relative) == digest, relative
if blocker is not None:
    assert blocker["item_id"] == ITEM and blocker["verdict"] == "blocked"
    assert blocker["blocker_id"] == canonical_json_id(blocker, "blocker_id")
    assert blocker["first_failed_gate"] == "dependency.S56-M-0325-PROOF.not_complete"
    assert blocker["remaining_root_cut_set"] == ["M0325-T-PACKAGE"]

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
    assert receipt is not None and selftest["known_failures"] == receipt["known_failures"] == KNOWN_FAILURES
    actual_changes = {
        line[3:] for line in git("status", "--short", "--untracked-files=all").splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual_changes == CHANGED_PATHS, (actual_changes, CHANGED_PATHS)

for relative in CHANGED_PATHS:
    path = ROOT / relative
    if path.exists():
        data = path.read_bytes()
        assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines()), path

print(
    "PASS S56-M-0325-VALIDATION: network-isolated lake env lean --trust=0 fresh-output "
    "replay checked the statement, conditional composition, pinned anchor, and 11 partial local "
    "bodies; the proof dependency, exact root, complete trust/provenance, cold hermetic, and "
    "independent-verification gates fail closed"
)
