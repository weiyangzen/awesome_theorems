#!/usr/bin/env python3
"""Fail-closed narrow validation for S56-M-0533-VALIDATION."""

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
HERE = ROOT / "Stage1_Instances" / "THM-M-0533"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
ITEM = "S56-M-0533-VALIDATION"
THEOREM = "THM-M-0533"
BASE_REVISION = "9293a4d141848287a1f656eefe9929eb30465393"
BASE_TREE = "63616ff5bc0e58e05d2eb66cff302101ea0c2fa0"
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
DENOMINATOR_SHA256 = "238242dfcb6274343a6413ed2628d0944bf0882c280b42608d8e19bad2c88dfc"
EXPECTED_INPUT_HASHES = {
    "Statement.lean": "cbe35890b43f302b71cf1230a87c21b2ac4eedf196210389598453c61ff18bce",
    "ObligationTree.lean": "ded027e2345e1b81568067254d083de705bf062e0f9079fe6d2a427c2c21f3b1",
    "Proof.lean": "4b577167c4778809d6585256f7683df4242488b5132669d0c3365a8912360837",
    "Validation.lean": "13a35cba8e198fb9910c1242b359402538c98c6d423eb6d40ed2de58f0f51131",
    "AnchorAudit.lean": "f961c09b06b643a85a22080a7cbbb624f0b55b5f44458e3b068e3d164b9d7312",
    "anchor-audit.md": "bf50321ccb27ca382d051c7f5f591e49163b7d07709d6ee8b1b3430831a1060a",
    "obligation-registry.json": "cd0411fccc46ee639e87328a41ce396b92f62467fdffd68d9a39761387c9b630",
    "typed-graphs.json": "6ac4e3d41e8e184c6a88f7ffdcde043a79c43e6766a664caf12453aab66a9a24",
    "proof-receipt.json": "7c167975af38f5e3c20d51363852f979ea2c23e966695efae545c71464d8e0cc",
    "proof-blocker.json": "d222d860817cf09ce2bd671a28135a95534092fb921a5c5fb128032825c1b20a",
    "source-statement-crosswalk.md": "f42ffd34e8fa4d36f320efb22069a4fd70bea2bfecd93c0e6110af9070bd5459",
    "check_obligation_tree.py": "72f8ce8e19aec8c3174a7dd2359304811bb1ba228516b7d58d4b27fa4c51d670",
}
SELECTED_PROVENANCE = {
    "Mathlib/AlgebraicTopology/SingularHomology/Basic.lean":
        "655867a11ed5ec706a554ac32f8f273c5227cafd4b47f0de42d84e24b0d33c7c",
    ".lake/build/lib/lean/Mathlib/AlgebraicTopology/SingularHomology/Basic.olean":
        "03202b1396ef4a2ab9ba226ee4aaa93b492667ff0c882c60dc584ca9c4b7f4a7",
    "Mathlib/Algebra/Category/Grp/Biproducts.lean":
        "dcbf839a72d4c47e6126fd008f1093f849021ea06921dc2eb7e64480e7b639e5",
    ".lake/build/lib/lean/Mathlib/Algebra/Category/Grp/Biproducts.olean":
        "f937cf171b4e3f2210e5fc541bdce10d9d89760c0fed3a5fa363ea39d36ca4c7",
    "Mathlib/Topology/Category/TopCat/Opens.lean":
        "1bd4ff8ea268447dbb03e421db4a7087491619ede079db44163838235329d9c3",
    ".lake/build/lib/lean/Mathlib/Topology/Category/TopCat/Opens.olean":
        "77e8d645c1a6af52d4848fdfde4dc475a70e383a171b81bc3c1d2d86843331ec",
}
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
COMPOSITION_DECLARATIONS = (
    "AwesomeTheorems.THM_M_0533.root_of_construction_and_exactness",
)
PROOF_DECLARATIONS = (
    "AwesomeTheorems.THM_M_0533.firstMap_comp_secondMap",
)
VALIDATION_DECLARATIONS = (
    "AwesomeTheorems.THM_M_0533.Validation.independentlyReconstructedFirstSecond",
)
GRAPH_REPORTED_PRE_PROOF_CLOSURES = ["M0533-S-DEFINITIONS", "M0533-T-ASSEMBLE"]
REMAINING_ROOT_CUT = [
    "M0533-C-SUBDIVISION",
    "M0533-L-SMALL-QUASIISO",
    "M0533-L-CHAIN-KERNEL",
    "M0533-L-NATURALITY",
    "M0533-T-DEGREE-ZERO",
]
FIRST_FAILED_MATHEMATICAL_GATE = (
    "M0533-C-SUBDIVISION: the pinned Lean closure has no barycentric-subdivision "
    "chain operator and chain homotopy proving that cover-small singular chains "
    "compute the singular homology of the union"
)
EXPECTED_SUMMARY = (
    "PASS THM-M-0533 network-isolated trust-zero replay of the hash-bound canonical source/declaration\n"
    "PASS conditional composition, the partial proof, and its differential reconstruction use only the observed classical axiom subset\n"
    "PASS frozen hashes, placeholder scan, and selected pinned mathlib source/olean provenance\n"
    "OPEN M0533-C-SUBDIVISION and four other root-cut obligations; exact root, release hermeticity, and distinct-runner verification fail closed\n"
).encode("utf-8")
EXPECTED_SUMMARY_SHA256 = hashlib.sha256(EXPECTED_SUMMARY).hexdigest()
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
    "--setenv", "STAGE1_SKIP_RECEIPT_CHECK", "0",
    "/usr/bin/python3", "-I", "-B",
    f"Stage1_Instances/{THEOREM}/check_validation.py",
]
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/Validation.lean",
    f"Stage1_Instances/{THEOREM}/check_obligation_tree.py",
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
    timeout: int = 720,
) -> str:
    completed = subprocess.run(
        argv, cwd=cwd, env=env, text=True, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, timeout=timeout, check=False,
    )
    if completed.returncode != 0:
        raise RuntimeError(
            f"command failed ({completed.returncode}): {argv!r}\n{completed.stdout}"
        )
    return completed.stdout


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
registry = load(HERE / "obligation-registry.json")
graphs = load(HERE / "typed-graphs.json")
proof_receipt = load(HERE / "proof-receipt.json")
proof_blocker = load(HERE / "proof-blocker.json")
execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")
receipt_path = HERE / "validation-receipt.json"
receipt = load(receipt_path) if receipt_path.exists() else None
verify_receipt = os.environ.get("STAGE1_SKIP_RECEIPT_CHECK") != "1"
if verify_receipt:
    assert receipt is not None, "final validation receipt is required"
    assert (ROOT / ".stage1-worker-selftest.json").is_file(), (
        "final worker self-test manifest is required"
    )

assert git("rev-parse", "HEAD") == BASE_REVISION
assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
item = next(row for row in execution["items"] if row["id"] == ITEM)
assert item == {
    "id": ITEM,
    "theorem_id": THEOREM,
    "execution_rank": 590,
    "phase": "validation",
    "layer": 5,
    "state": "[ ]",
    "depends_on": ["S56-M-0533-PROOF"],
    "owned_paths": [f"Stage1_Instances/{THEOREM}"],
    "deliverable": "Run hermetic kernel, trust, provenance, and independent validation gates.",
    "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
    "attempts": 0,
    "children": [],
}
predecessor = next(
    row for row in execution["items"] if row["id"] == "S56-M-0533-PROOF"
)
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
    "STAGE1_SKIP_RECEIPT_CHECK": "0",
}
assert spec["expected_exit"] == 0 and spec["timeout_seconds"] == 720
assert spec["expected_outputs"] == [{
    "path_or_stream": "stdout",
    "semantic_hash_policy": (
        "four-line deterministic gate summary; exact bytes and SHA-256 are bound "
        "by the provisional receipt"
    ),
}]
registry_ids = [row["obligation_id"] for row in registry["obligations"]]
assert spec["covered_obligation_ids"] == registry_ids
assert len(registry_ids) == len(set(registry_ids)) == 19
assert set(spec["covered_declarations"]) == {
    "AwesomeTheorems.THM_M_0533.MayerVietorisSequence",
    "AwesomeTheorems.THM_M_0533.canonical_iff_alternate",
    *COMPOSITION_DECLARATIONS,
    *PROOF_DECLARATIONS,
    *VALIDATION_DECLARATIONS,
}

for name, expected in EXPECTED_INPUT_HASHES.items():
    assert sha256(HERE / name) == expected, f"bound validation input changed: {name}"
assert registry["frozen_against_statement_sha256"] == EXPECTED_INPUT_HASHES["Statement.lean"]
assert registry["denominator_sha256"] == DENOMINATOR_SHA256
assert graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
closure = graphs["closure_boundary"]
assert closure["closed_obligations"] == GRAPH_REPORTED_PRE_PROOF_CLOSURES
assert closure["root_closed"] is False and closure["root_machine_debt"] == "M3"
assert closure["audit_complete"] is False and closure["theorem_complete"] is False
assert closure["remaining_root_cut_set"] == REMAINING_ROOT_CUT
assert graphs["composition_certificates"] == [{
    "parent": "M0533-ROOT",
    "declaration": COMPOSITION_DECLARATIONS[0],
    "premises": ["M0533-T-CONSTRUCTION", "M0533-T-EXACTNESS"],
    "status": "checked_conditional",
}]
assert proof_receipt["support_state"] == "provisional_worker_selftest"
assert proof_receipt["closed_obligation_ids"] == []
assert proof_receipt["partial_progress_toward_obligation_ids"] == [
    "M0533-T-CONSTRUCTION"
]
assert proof_receipt["result"]["root_closed"] is False
assert proof_receipt["result"]["theorem_complete"] is False
assert proof_blocker["first_failed_gate"] == FIRST_FAILED_MATHEMATICAL_GATE
assert proof_blocker["remaining_root_cut_set"] == REMAINING_ROOT_CUT
assert proof_blocker["root_closed"] is False
assert proof_blocker["audit_complete"] is False
assert proof_blocker["theorem_complete"] is False

for relative in CHANGED_PATHS - {".stage1-worker-selftest.json"}:
    path = ROOT / relative
    if not path.exists():
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
validation_imports = (HERE / "Validation.lean").read_text(encoding="utf-8").split(
    "/-!", 1
)[0]
assert "Proof" not in validation_imports and "ObligationTree" not in validation_imports
proof_and_validation = "\n".join(
    source_without_comments((HERE / name).read_text(encoding="utf-8"))
    for name in ("Proof.lean", "Validation.lean")
)
assert re.search(r"^theorem[ \t]+MayerVietorisSequence\b", proof_and_validation, re.MULTILINE) is None

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
for relative, expected in SELECTED_PROVENANCE.items():
    assert sha256(mathlib / relative) == expected, f"selected provenance drift: {relative}"
assert sha256(LEAN_ROOT / "lean-toolchain") == TOOLCHAIN_SHA256
assert sha256(LEAN_ROOT / "lake-manifest.json") == MANIFEST_SHA256

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
for key, expected in spec["env_allowlist"].items():
    if verify_receipt or key != "STAGE1_SKIP_RECEIPT_CHECK":
        assert os.environ[key] == expected
assert LEAN_COMMIT in run([str(lean), "--version"], cwd=LEAN_ROOT, env=fixed_env)
lean_path = run(
    [str(lake), "env", "printenv", "LEAN_PATH"], cwd=LEAN_ROOT, env=fixed_env
).strip()

tmp = Path(tempfile.mkdtemp(prefix="stage1-m0533-validation-", dir="/tmp"))
try:
    tmp_target = tmp / "Stage1_Instances" / THEOREM
    tmp_target.mkdir(parents=True)
    for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
        shutil.copy2(HERE / name, tmp_target / name)
    (tmp / "home").mkdir()

    def isolated_lean(args: list[str], *, module_path: bool = False) -> str:
        path = f"{tmp_target}:{lean_path}" if module_path else lean_path
        return run(
            [str(lean), "--trust=0", "-R", str(tmp), *args],
            cwd=LEAN_ROOT,
            env={**fixed_env, "HOME": str(tmp / "home"), "LEAN_PATH": path},
        )

    statement_output = isolated_lean([
        "-o", str(tmp_target / "Statement.olean"), str(tmp_target / "Statement.lean")
    ])
    obligation_output = isolated_lean([
        "-o", str(tmp_target / "ObligationTree.olean"),
        str(tmp_target / "ObligationTree.lean"),
    ], module_path=True)
    proof_output = isolated_lean([
        "-o", str(tmp_target / "Proof.olean"), str(tmp_target / "Proof.lean")
    ], module_path=True)
    validation_output = isolated_lean([
        str(tmp_target / "Validation.lean")
    ], module_path=True)
finally:
    shutil.rmtree(tmp)

for declaration in COMPOSITION_DECLARATIONS:
    assert reported_axioms(obligation_output, declaration) <= EXPECTED_AXIOMS
for declaration in PROOF_DECLARATIONS:
    assert reported_axioms(proof_output, declaration) <= EXPECTED_AXIOMS
for declaration in VALIDATION_DECLARATIONS:
    assert reported_axioms(validation_output, declaration) <= EXPECTED_AXIOMS
assert validation_output.count("Declarations are sorry-free!") == len(VALIDATION_DECLARATIONS)
combined_output = "\n".join(
    (statement_output, obligation_output, proof_output, validation_output)
)
assert "AwesomeTheorems.THM_M_0533.MayerVietorisSequence" in statement_output
assert "sorryAx" not in combined_output
assert "declaration uses 'sorry'" not in combined_output
assert "error:" not in combined_output

if receipt is not None and verify_receipt:
    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["release_grade"] is False and receipt["verdict"] == "blocked"
    assert receipt["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert receipt["inputs"]["validation_spec_sha256"] == sha256(
        HERE / "validation-spec.json"
    )
    assert receipt["inputs"]["validator_sha256"] == sha256(Path(__file__).resolve())
    for key, name in (
        ("statement_source_sha256", "Statement.lean"),
        ("obligation_tree_source_sha256", "ObligationTree.lean"),
        ("proof_source_sha256", "Proof.lean"),
        ("validation_probe_sha256", "Validation.lean"),
        ("anchor_probe_sha256", "AnchorAudit.lean"),
        ("anchor_audit_sha256", "anchor-audit.md"),
        ("obligation_registry_sha256", "obligation-registry.json"),
        ("typed_graphs_sha256", "typed-graphs.json"),
        ("proof_receipt_sha256", "proof-receipt.json"),
        ("proof_blocker_sha256", "proof-blocker.json"),
        ("source_crosswalk_sha256", "source-statement-crosswalk.md"),
        ("obligation_validator_sha256", "check_obligation_tree.py"),
    ):
        assert receipt["inputs"][key] == sha256(HERE / name), key
    assert receipt["recipe"] == {
        key: spec[key]
        for key in (
            "recipe_id", "cwd", "argv", "env_allowlist", "timeout_seconds",
            "network_policy", "network_enforcement", "expected_exit",
        )
    }
    assert receipt["evidence_log"]["stream"] == "stdout"
    assert receipt["evidence_log"]["bytes"] == len(EXPECTED_SUMMARY)
    assert receipt["evidence_log"]["sha256"] == EXPECTED_SUMMARY_SHA256
    assert receipt["evidence_log"]["exit_code"] == 0
    result = receipt["result"]
    assert result["graph_reported_pre_proof_closed_obligation_ids"] == GRAPH_REPORTED_PRE_PROOF_CLOSURES
    assert result["graph_illegally_closed_parent_ids"] == ["M0533-T-ASSEMBLE"]
    assert result["newly_closed_obligation_ids"] == []
    assert result["accepted_closed_obligation_ids"] == []
    assert result["validated_conditional_composition_ids"] == ["M0533-T-ASSEMBLE"]
    assert result["root_closed"] is False and result["root_kernel_closed"] is False
    assert result["audit_complete"] is False and result["theorem_complete"] is False
    assert result["root_vector_before"] == result["root_vector_after"] == {
        "H": "H3", "M": "M3", "R": "R4"
    }
    assert result["inherited_recorded_priority_blocker_set"] == REMAINING_ROOT_CUT
    assert result["complete_transitive_provenance_gate"] == "fail_closed"
    assert result["complete_transitive_tcb_gate"] == "fail_closed"
    assert result["hermetic_release_gate"] == "fail_closed"
    assert result["independent_verification_gate"] == "fail_closed"
    assert result["accepted_state_changed"] is False
    assert receipt["first_failed_gate"] == (
        "S56-5.1-EXPRESSION-FINGERPRINT: no independently serialized "
        "elaborated-expression digest exists for the canonical target"
    )
    assert receipt["first_failed_mathematical_proof_gate"] == (
        FIRST_FAILED_MATHEMATICAL_GATE
    )
    assert receipt["inherited_recorded_priority_blocker_set"] == REMAINING_ROOT_CUT
    assert set(receipt["changed_paths"]) == CHANGED_PATHS
    assert receipt["trust"]["accepted_foundation_profile"] is False
    assert receipt["provenance"]["proof_dependency_master_accepted"] is False

packet_path = ROOT / ".stage1-worker-selftest.json"
if packet_path.exists() and verify_receipt:
    packet = load(packet_path)
    assert set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert packet["item_id"] == ITEM and packet["state"] == "[_]"
    assert packet["base_revision"] == BASE_REVISION
    assert set(packet["changed_paths"]) == CHANGED_PATHS
    assert isinstance(packet["commands"], list) and packet["commands"]
    assert isinstance(packet["output_summary"], str) and packet["output_summary"]
    assert isinstance(packet["known_failures"], list) and packet["known_failures"]
    actual_changes = {
        line[3:] if line.startswith("?? ") else line[2:].lstrip()
        for line in git("status", "--short", "--untracked-files=all").splitlines()
    }
    actual_changes.discard("Formalizations/Lean/.lake")
    assert actual_changes == CHANGED_PATHS

print(EXPECTED_SUMMARY.decode("utf-8"), end="", flush=True)
