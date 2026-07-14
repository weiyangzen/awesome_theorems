#!/usr/bin/env python3
"""Fail-closed narrow validation for S56-M-0526-VALIDATION."""

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
HERE = ROOT / "Stage1_Instances" / "THM-M-0526"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
ITEM = "S56-M-0526-VALIDATION"
THEOREM = "THM-M-0526"
BASE_REVISION = "c470319c4a07f669317557ea705f6546605ac4da"
BASE_TREE = "680bb215853ecfbfa26fe069d1282188ed3944aa"
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
    "a7550267adfd8bc8d37de8174319c6389cb1bbab62b740595a9c91d831567d45"
)
DENOMINATOR_SHA256 = "6ee9cb595c6fee2025b76834826de8a48bb4a0bcb6fa86a8d3d91a17632452f5"
EXPECTED_INPUT_HASHES = {
    "Statement.lean": "862db06c1419e1eed5c5c9f118865bd0c1e35c3121b869697dceda5a99cd7d28",
    "ObligationTree.lean": "9b04e0d818885b9c100da79f28dfdebe8fb8bd95bd3db4594a09da531f5952c6",
    "Proof.lean": "74ac822c8e16fe91eefcb0a2664dd7c1404505dbeb2323f8259730ba2f6489c6",
    "statement.json": "eb4dcabe1c0422e695eb2755ec8618107bb5306520258429a78acace4d28fb0d",
    "anchor-audit.json": "2dc4e9ced9ec65e801a8789a574d0d12a1ca0ffc8ca254bdd2d51ce2a999c118",
    "obligation-registry.json": "facb4300b98cae1961de2f114ecd08c5d9d09078aac9f024e9680361b541d12a",
    "typed-graphs.json": "abc7af1ff0a7537b8fa577045c57e11983a797384caaa82dcc7f7973891c3713",
    "proof-receipt.json": "bc258b91369c42ab2f549f0278b3985c735c23ee9566f339f55cfe77e246c45b",
    "proof-blocker.json": "ec6dc6ff806f431819197988326fdb10d9174ab9a7af3ccd06c2850697f7c265",
    "source-statement-crosswalk.md": "9fc2269a30a5719c9dd19476f32a13e2656fc333048c6d4a09f5e8cd59538373",
    "proof-outline.md": "1f943725a90e8a0c22cf5ac4a7ee1d90dab95e2e08c1835e1dd3578df6a9e48d",
}
SELECTED_PROVENANCE = {
    "Mathlib/AlgebraicTopology/FundamentalGroupoid/FundamentalGroup.lean":
        "4d38953d013f239ed987fb0e1d46bdb440a9366420d456d550fd4719c2c94a2d",
    ".lake/build/lib/lean/Mathlib/AlgebraicTopology/FundamentalGroupoid/FundamentalGroup.olean":
        "40c4554eedc92e7d09cb85aa261aff67dac57eb43a6e5aa0fe3d7cb33f0c6c60",
    "Mathlib/AlgebraicTopology/FundamentalGroupoid/Basic.lean":
        "3574eb339dcfa87a57bde1a54d441eda7a2abea7b3c42093f19e6c0bb17f9fd6",
    ".lake/build/lib/lean/Mathlib/AlgebraicTopology/FundamentalGroupoid/Basic.olean":
        "e0af7a4b385f2cc821a93cb7ef192ea98ccbb8a0073662a1e5945c341c7f9b5c",
    "Mathlib/Topology/UnitInterval.lean":
        "ded00444664001f0b07abfd619bf40d11edd564967b3e7c5243fcbdd66049e90",
    ".lake/build/lib/lean/Mathlib/Topology/UnitInterval.olean":
        "00cef28fa2c2db805180c51a805a4cfd283d89011a10df72810e0681234cc0fe",
    "Mathlib/Topology/Subpath.lean":
        "8023375c817a266a059cdb98d7e57da3afca84ef177fe2045f2dfe22bce1e272",
    ".lake/build/lib/lean/Mathlib/Topology/Subpath.olean":
        "84244a06fa7f8bfaec1131a12ed23bf1bf610cbd2b175886fb3fe0feeef0fd5c",
}
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
PROOF_DECLARATIONS = (
    "Stage1Instances.THM_M_0526.square_commutativity_proof",
    "Stage1Instances.THM_M_0526.square_package",
    "Stage1Instances.THM_M_0526.path_subdivision_of_two_open_cover",
)
COMPOSITION_DECLARATIONS = (
    "Stage1Instances.THM_M_0526.compose_pushout",
    "Stage1Instances.THM_M_0526.compose_root",
)
VALIDATION_DECLARATIONS = (
    "Stage1Instances.THM_M_0526.Validation.independentlyReconstructedSquare",
    "Stage1Instances.THM_M_0526.Validation.independentlyReconstructedSubdivision",
)
PROVISIONAL_OBLIGATIONS = [
    "SVK-MAP-FUNCTORIALITY",
    "SVK-SQUARE",
    "SVK-LEBESGUE-NUMBER",
]
REMAINING_ROOT_CUT = [
    "SVK-CHANGE-BASEPATH",
    "SVK-WORD-DEFINITION",
    "SVK-REFINEMENT-INVARIANCE",
    "SVK-HOMOTOPY-INVARIANCE",
    "SVK-LIFT-HOM",
    "SVK-GENERATION",
    "SVK-AGREEMENT-ON-WORDS",
]
FIRST_FAILED_GATE = (
    "SVK-CHANGE-BASEPATH: no implemented transport package yet turns each "
    "subordinate segment into a based loop in U or V compatibly through U intersection V"
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
    timeout: int = 720,
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
proof_receipt = load(HERE / "proof-receipt.json")
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
    "execution_rank": 583,
    "phase": "validation",
    "layer": 5,
    "state": "[ ]",
    "depends_on": ["S56-M-0526-PROOF"],
    "owned_paths": [f"Stage1_Instances/{THEOREM}"],
    "deliverable": "Run hermetic kernel, trust, provenance, and independent validation gates.",
    "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
    "attempts": 0,
    "children": [],
}
predecessor = next(row for row in execution["items"] if row["id"] == "S56-M-0526-PROOF")
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
assert spec["expected_exit"] == 0 and spec["timeout_seconds"] == 720
assert set(spec["covered_obligation_ids"]) == {
    row["id"] for row in registry["obligations"]
}
assert len(spec["covered_obligation_ids"]) == len(set(spec["covered_obligation_ids"]))
assert set(spec["covered_declarations"]) == {
    "Stage1Instances.THM_M_0526.SeifertVanKampenTarget",
    *COMPOSITION_DECLARATIONS,
    *PROOF_DECLARATIONS,
    *VALIDATION_DECLARATIONS,
}

for name, expected in EXPECTED_INPUT_HASHES.items():
    assert sha256(HERE / name) == expected, f"bound validation input changed: {name}"
formal = statement["canonical_formal_target"]
assert formal["statement_file_sha256"] == sha256(HERE / "Statement.lean")
assert formal["elaborated_expression_sha256"] == STATEMENT_EXPRESSION_SHA256
assert registry["frozen_denominator_sha256"] == DENOMINATOR_SHA256
assert registry["closure_summary"] == {
    "required": 17,
    "closed": 0,
    "open": 17,
    "root_closed": False,
}
assert proof_receipt["support_state"] == "provisional_worker_selftest"
assert proof_receipt["proposed_state"] == "[_]" and proof_receipt["accepted"] is False
assert proof_receipt["provisionally_closed_obligation_ids"] == PROVISIONAL_OBLIGATIONS
assert proof_receipt["accepted_closed_obligation_ids"] == []
assert proof_receipt["remaining_root_cut_set"] == REMAINING_ROOT_CUT
assert proof_receipt["result"]["root_kernel_closed"] is False
assert proof_blocker["first_failed_gate"] == FIRST_FAILED_GATE
assert proof_blocker["remaining_root_cut_set"] == REMAINING_ROOT_CUT
assert proof_blocker["root_closed"] is False
assert proof_blocker["theorem_complete"] is False
assert graphs["item_id"] == "S56-M-0526-OBLIGATION_TREE"
assert graphs["deduplication"]["distinct_terminal_proof_bodies"] == 0
assert "no proof-body credit" in graphs["status_boundary"]

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
assert "Proof" not in validation_imports and "ObligationTree" not in validation_imports
proof_and_validation = "\n".join(
    source_without_comments((HERE / name).read_text(encoding="utf-8"))
    for name in ("Proof.lean", "Validation.lean")
)
assert re.search(r"^theorem[ \t]+SeifertVanKampenTarget\b", proof_and_validation, re.MULTILINE) is None

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
assert anchor["classification"]["machine_state"] == "not_repo_local_closed"
assert anchor["mathlib"]["exact_candidate"] is None
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

tmp = Path(tempfile.mkdtemp(prefix="stage1-m0526-validation-", dir="/tmp"))
try:
    tmp_target = tmp / "Stage1_Instances" / THEOREM
    tmp_target.mkdir(parents=True)
    for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
        shutil.copy2(HERE / name, tmp_target / name)
    (tmp / "home").mkdir()

    def isolated_lean(args: list[str], *, module_path: bool = False) -> str:
        path = f"{tmp}:{lean_path}" if module_path else lean_path
        return run(
            [str(lake), "env", "lean", "--trust=0", "-t0", "-R", str(tmp), *args],
            cwd=LEAN_ROOT,
            env={**fixed_env, "HOME": str(tmp / "home"), "LEAN_PATH": path},
        )

    statement_output = isolated_lean([
        "-o", str(tmp_target / "Statement.olean"), str(tmp_target / "Statement.lean")
    ])
    obligation_output = isolated_lean([
        "-o", str(tmp_target / "ObligationTree.olean"), str(tmp_target / "ObligationTree.lean")
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
combined_output = "\n".join((statement_output, obligation_output, proof_output, validation_output))
assert "Stage1Instances.THM_M_0526.SeifertVanKampenTarget" in statement_output
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
    assert receipt["registry_denominator_sha256"] == DENOMINATOR_SHA256
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
        ("proof_receipt_sha256", "proof-receipt.json"),
        ("proof_blocker_sha256", "proof-blocker.json"),
        ("source_crosswalk_sha256", "source-statement-crosswalk.md"),
        ("proof_outline_sha256", "proof-outline.md"),
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
    assert result["provisionally_revalidated_obligation_ids"] == PROVISIONAL_OBLIGATIONS
    assert result["accepted_closed_obligation_ids"] == []
    assert result["root_closed"] is False and result["root_kernel_closed"] is False
    assert result["audit_complete"] is False and result["theorem_complete"] is False
    assert result["root_vector_before"] == result["root_vector_after"] == {
        "H": "H2", "M": "M4", "R": "R4"
    }
    assert result["remaining_root_cut_set"] == REMAINING_ROOT_CUT
    assert result["complete_transitive_provenance_gate"] == "fail_closed"
    assert result["complete_transitive_tcb_gate"] == "fail_closed"
    assert result["hermetic_release_gate"] == "fail_closed"
    assert result["independent_verification_gate"] == "fail_closed"
    assert result["accepted_state_changed"] is False
    assert receipt["first_failed_gate"] == FIRST_FAILED_GATE
    assert receipt["remaining_root_cut_set"] == REMAINING_ROOT_CUT
    assert set(receipt["changed_paths"]) == CHANGED_PATHS
    assert receipt["trust"]["accepted_foundation_profile"] is False
    assert receipt["provenance"]["proof_dependency_master_accepted"] is False

packet_path = ROOT / ".stage1-worker-selftest.json"
if packet_path.exists() and verify_receipt:
    packet = load(packet_path)
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

print("PASS THM-M-0526 network-isolated trust-zero replay of the exact frozen target")
print("PASS conditional composition, three partial declarations, and two differential reconstructions use only the observed classical axiom subset")
print("PASS frozen hashes, placeholder scan, and selected pinned mathlib source/olean provenance")
print("OPEN SVK-CHANGE-BASEPATH and six other root-cut obligations; exact root, release hermeticity, and distinct-runner verification fail closed")
