#!/usr/bin/env python3
"""Fail-closed narrow validation for S56-M-0442-VALIDATION."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import pwd
import re
import shutil
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0442"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
ITEM = "S56-M-0442-VALIDATION"
THEOREM = "THM-M-0442"
BASE_REVISION = "a1a7e939e58f103f5ff5d23af51437fa8658aa04"
BASE_TREE = "d881fd9641fa3e5f3ebe5082b35672981e90adcf"
LEAN_TOOLCHAIN = "leanprover/lean4:v4.29.0"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
LEAN_SHA256 = "3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf"
LAKE_SHA256 = "a608ff084d7e2af228b92a29d7c2fd083ba0580e46889175ec74a81678c98359"
BWRAP_SHA256 = "0abea81db798ebf6b4742ac0664802d97521547a353c2a0dbdc21d76cbbfd2c0"
PYTHON_SHA256 = "b8d8288faefdd300201f43fcf00f6f539a27218eeed3a3dff5ab10b9c4c99700"
TOOLCHAIN_SHA256 = "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2"
MANIFEST_SHA256 = "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_REMOTE = "https://github.com/leanprover-community/mathlib4.git"
MATHLIB_LICENSE_SHA256 = "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1"
STATEMENT_EXPRESSION_SHA256 = (
    "b65a3a73cac19c57286b3cba584fc84ebda329b70006b409f12ec6e761721658"
)
EXPECTED_INPUT_HASHES = {
    "Statement.lean": "8779e87e3bc1c18654f30bb6380798da00baeaf18e8df6a588c6519ae8655ce4",
    "ObligationTree.lean": "6bf3713e057593c9690ea877901e3418d1c1b3f4e41c8f8acd43d01198e7b38e",
    "Proof.lean": "6c0c7737f36b2e0d692828ed596c4d6286d258efcd122835a84eaf8cf9b9630b",
    "statement.json": "3cae15fe8c83c2034eb8149487e4322730d7febfb618fec68cebd7d8f36d807c",
    "anchor-audit.json": "cf6d14efe101761821962b52d54e69c01a5c32557c3502ed1f1112217370ecf0",
    "obligation-registry.json": "1df31d91ca04657c2c90d2effbd80daad2988a1d0b3d64f4a6e1ed8ebd2a15c9",
    "typed-graphs.json": "6248c8a590c5bc358ea0cf0de179d3e3c9db725fa30fb37d05c4be3b9c6f594d",
    "proof-blocker.json": "82ab210fc5c79cb0d29b2d297023daa34f5fac4b5b43818d4002917025b94dfd",
    "proof-validation.md": "82290a891582fc5882021b7d09a83c831c5a8d615062fb13b3e8066c6b41047f",
    "source-statement-crosswalk.md": "3ab6e07b49c8f10bf2f4b4aaeea215eb677b241f9a4d94699f03fcbc4fee4b00",
}
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
PROOF_DECLARATIONS = (
    "cyclic_order_le_sixteen",
    "bicyclic_index_four_mul_le_sixteen",
    "torsion_ncard_eq_of_hasCyclicTorsionOrder",
    "torsion_ncard_eq_of_hasBicyclicTorsionIndex",
    "mazurRationalTorsionTarget_implies_torsionBoundAtMostSixteen",
)
VALIDATION_DECLARATIONS = (
    "cyclic_order_le_sixteen",
    "bicyclic_index_four_mul_le_sixteen",
    "allowed_shape_cardinality_bound",
)
REMAINING_ROOT_CUT = [
    "M0442-G-FIN",
    "M0442-G-RANK",
    "M0442-C-PRIME",
    "M0442-C-POWER",
    "M0442-B-TWO",
    "M0442-B-INDEX",
    "M0442-M-MODULI",
    "M0442-M-CUSPS",
    "M0442-M-RATIONAL",
    "M0442-A-REDUCTION",
    "M0442-A-DESCENT",
    "M0442-SOURCE",
    "M0442-TRUST",
]
FIRST_FAILED_GATE = (
    "M0442-M-MODULI: no kernel-checked compactified modular-curve/moduli-map "
    "proof body is present in the pinned dependency closure"
)
RECIPE_PATH = "/usr/bin:/bin"
RECIPE_ARGV = [
    "/usr/bin/bwrap",
    "--ro-bind", "/", "/",
    "--dev", "/dev",
    "--proc", "/proc",
    "--tmpfs", "/tmp",
    "--unshare-net",
    "--die-with-parent",
    "--clearenv",
    "--setenv", "HOME", "/tmp",
    "--setenv", "PATH", RECIPE_PATH,
    "--setenv", "LANG", "C.UTF-8",
    "--setenv", "LC_ALL", "C.UTF-8",
    "--setenv", "TZ", "UTC",
    "--setenv", "LEAN_NUM_THREADS", "1",
    "/usr/bin/python3", "-I", "-B",
    f"Stage1_Instances/{THEOREM}/check_validation.py",
]
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
anchor = load(HERE / "anchor-audit.json")
registry = load(HERE / "obligation-registry.json")
graphs = load(HERE / "typed-graphs.json")
proof_blocker = load(HERE / "proof-blocker.json")
execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")
receipt_path = HERE / "validation-receipt.json"
receipt = load(receipt_path) if receipt_path.exists() else None
verify_receipt = os.environ.get("STAGE1_SKIP_RECEIPT_CHECK") != "1"

assert git("rev-parse", "HEAD") == BASE_REVISION
assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
item = next(row for row in execution["items"] if row["id"] == ITEM)
assert item == {
    "id": ITEM,
    "theorem_id": THEOREM,
    "execution_rank": 88,
    "phase": "validation",
    "layer": 5,
    "state": "[ ]",
    "depends_on": ["S56-M-0442-PROOF"],
    "owned_paths": [f"Stage1_Instances/{THEOREM}"],
    "deliverable": "Run hermetic kernel, trust, provenance, and independent validation gates.",
    "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
    "attempts": 0,
    "children": [],
}
predecessor = next(row for row in execution["items"] if row["id"] == "S56-M-0442-PROOF")
assert predecessor["state"] == "[_]" and predecessor["attempts"] == 1

assert spec["schema_version"] == "stage1-validation-spec/1.0"
assert spec["item_id"] == ITEM and spec["theorem_id"] == THEOREM
assert spec["argv"] == RECIPE_ARGV
assert spec["cwd"] == "." and spec["network_policy"] == "denied"
assert spec["env_allowlist"] == {
    "HOME": "/tmp",
    "PATH": RECIPE_PATH,
    "LANG": "C.UTF-8",
    "LC_ALL": "C.UTF-8",
    "TZ": "UTC",
    "LEAN_NUM_THREADS": "1",
}
assert spec["expected_exit"] == 0 and spec["timeout_seconds"] == 300
assert len(spec["covered_obligation_ids"]) == len(set(spec["covered_obligation_ids"]))
assert set(REMAINING_ROOT_CUT) <= set(spec["covered_obligation_ids"])
expected_declarations = {
    "Stage1Instances.THMM0442.MazurRationalTorsionTarget",
    "Stage1Instances.THMM0442.mazurRationalTorsionTarget_iff_historicalCandidateShape",
    "Stage1Instances.THMM0442.ObligationTree.engine_compose",
    *("Stage1Instances.THMM0442.Proof." + name for name in PROOF_DECLARATIONS),
    *("Stage1Instances.THMM0442.Validation." + name for name in VALIDATION_DECLARATIONS),
}
assert set(spec["covered_declarations"]) == expected_declarations
assert len(spec["covered_declarations"]) == len(expected_declarations)

for name, expected in EXPECTED_INPUT_HASHES.items():
    assert sha256(HERE / name) == expected, f"bound validation input changed: {name}"
formal = statement["canonical_formal_target"]
assert formal["statement_file_sha256"] == sha256(HERE / "Statement.lean")
assert formal["elaborated_expression_sha256"] == STATEMENT_EXPRESSION_SHA256
assert registry["root_obligation_id"] == graphs["root_obligation_id"] == "M0442-ROOT"
assert registry["frozen_against_statement_sha256"] == sha256(HERE / "Statement.lean")
assert registry["frozen_against_anchor_audit_sha256"] == sha256(HERE / "anchor-audit.json")
assert len(registry["obligations"]) == 21
closure = graphs["closure_boundary"]
assert closure["closed_obligations"] == []
assert closure["conditionally_composed_obligations"] == ["M0442-T"]
assert closure["remaining_root_cut_set"] == REMAINING_ROOT_CUT
assert closure["root_closed"] is False
assert closure["audit_complete"] is False
assert closure["theorem_complete"] is False
assert proof_blocker["item_id"] == "S56-M-0442-PROOF"
assert proof_blocker["verdict"] == "blocked" and proof_blocker["state"] == "[_]"
assert proof_blocker["closed_obligations"] == []
assert proof_blocker["remaining_root_cut_set"] == REMAINING_ROOT_CUT
assert proof_blocker["root_closed"] is False
assert proof_blocker["audit_complete"] is False
assert proof_blocker["theorem_complete"] is False
assert proof_blocker["first_failed_gate"] == FIRST_FAILED_GATE
for name in (
    "Statement.lean", "ObligationTree.lean", "Proof.lean",
    "obligation-registry.json", "typed-graphs.json", "anchor-audit.json",
):
    assert proof_blocker["source_hashes"][name] == sha256(HERE / name)

for relative in CHANGED_PATHS - {".stage1-worker-selftest.json"}:
    path = ROOT / relative
    if not path.exists() and not verify_receipt:
        continue
    data = path.read_bytes()
    assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())

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
assert "MazurEngine" not in source_without_comments(
    (HERE / "Validation.lean").read_text(encoding="utf-8")
)
proof_and_validation = "\n".join(
    source_without_comments((HERE / name).read_text(encoding="utf-8"))
    for name in ("Proof.lean", "Validation.lean")
)
assert re.search(
    r"^theorem[ \t]+mazurRationalTorsionTarget(?:[ \t:(]|$)",
    proof_and_validation,
    re.MULTILINE,
) is None

manifest = load(LEAN_ROOT / "lake-manifest.json")
mathlib_entry = next(row for row in manifest["packages"] if row["name"] == "mathlib")
assert mathlib_entry["rev"] == mathlib_entry["inputRev"] == MATHLIB_REVISION
mathlib = LEAN_ROOT / ".lake" / "packages" / "mathlib"
assert mathlib.resolve().is_dir(), "pinned mathlib artifact is unavailable"
assert git("rev-parse", "HEAD", cwd=mathlib) == MATHLIB_REVISION
assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == MATHLIB_TREE
assert git("remote", "get-url", "origin", cwd=mathlib) == MATHLIB_REMOTE
assert git("status", "--porcelain=v1", "--untracked-files=all", cwd=mathlib) == ""
assert sha256(mathlib / "LICENSE") == MATHLIB_LICENSE_SHA256
assert sha256(LEAN_ROOT / "lean-toolchain") == TOOLCHAIN_SHA256
assert sha256(LEAN_ROOT / "lake-manifest.json") == MANIFEST_SHA256
mathlib_candidate = next(
    row for row in anchor["candidates"] if row["candidate_id"] == "MATHLIB-SUBSTRATE"
)
assert mathlib_candidate["revision"] == MATHLIB_REVISION
assert mathlib_candidate["classification"] == "M4"
assert mathlib_candidate["proof_credit"] is False
assert anchor["root_machine_classification"] == "M4"
assert anchor["theorem_proved"] is False and anchor["theorem_complete"] is False

account_home = Path(pwd.getpwuid(os.getuid()).pw_dir)
toolchain_bin = account_home / ".elan" / "toolchains" / "leanprover--lean4---v4.29.0" / "bin"
lean = toolchain_bin / "lean"
lake = toolchain_bin / "lake"
bwrap = Path(shutil.which("bwrap") or "")
assert lean.is_file() and lake.is_file() and bwrap.is_file()
assert sha256(lean) == LEAN_SHA256 and sha256(lake) == LAKE_SHA256
assert bwrap == Path("/usr/bin/bwrap") and sha256(bwrap) == BWRAP_SHA256
assert sha256(Path("/usr/bin/python3")) == PYTHON_SHA256
fixed_env = {
    "HOME": os.environ["HOME"],
    "PATH": f"{toolchain_bin}:/usr/bin:/bin",
    "ELAN_TOOLCHAIN": LEAN_TOOLCHAIN,
    "LANG": "C.UTF-8",
    "LC_ALL": "C.UTF-8",
    "TZ": "UTC",
    "LEAN_NUM_THREADS": "1",
}
assert {key: os.environ[key] for key in spec["env_allowlist"]} == spec["env_allowlist"]
assert LEAN_COMMIT in run([str(lean), "--version"], cwd=LEAN_ROOT, env=fixed_env)
lean_path = run([str(lake), "env", "printenv", "LEAN_PATH"], cwd=LEAN_ROOT, env=fixed_env).strip()

tmp = Path(tempfile.mkdtemp(prefix="stage1-m0442-validation-", dir="/tmp"))
try:
    for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
        shutil.copy2(HERE / name, tmp / name)
    (tmp / "home").mkdir()

    def isolated_lean(args: list[str], *, module_path: bool = False) -> str:
        path = f"{tmp}:{lean_path}" if module_path else lean_path
        return run(
            [str(lake), "env", "lean", "--trust=0", *args],
            cwd=tmp,
            env={**fixed_env, "HOME": str(tmp / "home"), "LEAN_PATH": path},
        )

    statement_output = isolated_lean(["-o", "Statement.olean", "Statement.lean"])
    obligation_output = isolated_lean(
        ["-o", "ObligationTree.olean", "ObligationTree.lean"], module_path=True
    )
    proof_output = isolated_lean(["-o", "Proof.olean", "Proof.lean"], module_path=True)
    validation_output = isolated_lean(["Validation.lean"], module_path=True)
finally:
    shutil.rmtree(tmp)

composition = "Stage1Instances.THMM0442.ObligationTree.engine_compose"
assert reported_axioms(obligation_output, composition) <= EXPECTED_AXIOMS
for short_name in PROOF_DECLARATIONS:
    declaration = "Stage1Instances.THMM0442.Proof." + short_name
    assert reported_axioms(proof_output, declaration) <= EXPECTED_AXIOMS
for short_name in VALIDATION_DECLARATIONS:
    declaration = "Stage1Instances.THMM0442.Validation." + short_name
    assert reported_axioms(validation_output, declaration) <= EXPECTED_AXIOMS
assert validation_output.count("Declarations are sorry-free!") == len(VALIDATION_DECLARATIONS)
combined_output = "\n".join((statement_output, obligation_output, proof_output, validation_output))
assert "sorryAx" not in combined_output
assert "declaration uses 'sorry'" not in combined_output
assert "error:" not in combined_output

if receipt is not None and verify_receipt:
    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["release_grade"] is False and receipt["verdict"] == "blocked"
    assert receipt["canonical_target_expression_sha256"] == STATEMENT_EXPRESSION_SHA256
    assert receipt["inputs"]["validation_spec_sha256"] == sha256(HERE / "validation-spec.json")
    assert receipt["inputs"]["validator_sha256"] == sha256(Path(__file__).resolve())
    assert receipt["inputs"]["validation_probe_sha256"] == sha256(HERE / "Validation.lean")
    for key, name in (
        ("statement_source_sha256", "Statement.lean"),
        ("obligation_tree_source_sha256", "ObligationTree.lean"),
        ("proof_source_sha256", "Proof.lean"),
        ("statement_record_sha256", "statement.json"),
        ("anchor_audit_sha256", "anchor-audit.json"),
        ("obligation_registry_sha256", "obligation-registry.json"),
        ("typed_graphs_sha256", "typed-graphs.json"),
        ("proof_blocker_sha256", "proof-blocker.json"),
        ("proof_validation_sha256", "proof-validation.md"),
        ("source_crosswalk_sha256", "source-statement-crosswalk.md"),
    ):
        assert receipt["inputs"][key] == sha256(HERE / name), key
    assert receipt["recipe"] == {
        key: spec[key]
        for key in (
            "recipe_id", "cwd", "argv", "env_allowlist", "timeout_seconds",
            "network_policy", "network_enforcement", "expected_exit",
        )
    }
    result = receipt["result"]
    assert result["supported_obligation_ids"] == []
    assert result["provisionally_closed_obligation_ids"] == []
    assert result["accepted_closed_obligation_ids"] == []
    assert result["root_closed"] is False and result["root_kernel_closed"] is False
    assert result["audit_complete"] is False and result["theorem_complete"] is False
    assert result["root_vector_before"] == result["root_vector_after"] == {
        "H": "H1", "M": "M4", "R": "R4"
    }
    assert result["remaining_root_cut_set"] == REMAINING_ROOT_CUT
    assert result["complete_transitive_provenance_gate"] == "fail_closed"
    assert result["complete_transitive_tcb_gate"] == "fail_closed"
    assert result["hermetic_release_gate"] == "fail_closed"
    assert result["independent_verification_gate"] == "fail_closed"
    assert result["accepted_state_changed"] is False
    assert receipt["first_failed_gate"] == FIRST_FAILED_GATE
    assert receipt["first_failed_release_gate"] == "S56-10.6-HERMETIC-COLD-EMPTY-CACHE"
    assert receipt["remaining_root_cut_set"] == REMAINING_ROOT_CUT
    assert set(receipt["changed_paths"]) == CHANGED_PATHS
    assert receipt["trust"]["accepted_foundation_profile"] is False
    assert receipt["trust"]["complete_transitive_trust_closure"] is False
    assert receipt["provenance"]["root_provenance_closure"] == "open"
    assert receipt["hermeticity"]["decision"] == "fail_closed_nonrelease_warm_cache_replay"
    assert receipt["independent_validation"]["decision"] == "fail_closed"
    assert receipt["evidence_log"]["exit_code"] == 0
    assert receipt["validation_started_at"] < receipt["validation_ended_at"]
    assert receipt["validated_at"] == receipt["validation_ended_at"]

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
    if receipt is not None and verify_receipt:
        assert packet["known_failures"] == receipt["known_failures"]
    actual_changes = {
        line[3:] for line in run(
            ["git", "status", "--short", "--untracked-files=all"]
        ).splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual_changes == CHANGED_PATHS, (actual_changes, CHANGED_PATHS)

print("PASS THM-M-0442 network-isolated trust-zero replay of the frozen Lean target")
print("PASS conditional composition, five partial declarations, and three differential declarations use only the selected classical axiom subset")
print("PASS frozen hashes, proof blocker, placeholder scan, and pinned mathlib provenance; zero frozen obligations closed")
print("OPEN M0442-M-MODULI and twelve other root-cut obligations; hermetic release and distinct-runner verification fail closed")
