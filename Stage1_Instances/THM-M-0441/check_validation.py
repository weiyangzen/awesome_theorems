#!/usr/bin/env python3
"""Fail-closed narrow validation for S56-M-0441-VALIDATION."""

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
HERE = ROOT / "Stage1_Instances" / "THM-M-0441"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
ITEM = "S56-M-0441-VALIDATION"
THEOREM = "THM-M-0441"
BASE_REVISION = "18ff7447208231633bf2e01e8aad3111af56531a"
BASE_TREE = "9ea9aab30253e72b62ef25c80e17b575356fb7b6"
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
    "103f282fc63e0dfa6ac9de4f13736044bf5131a41883196fdca531df00a5a475"
)
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
PROOF_DECLARATIONS = (
    "subset_algebraicPart_of_semialgebraic_preconnected_nontrivial",
    "algebraicPart_subset",
    "algebraicPart_mono",
    "normalizedRatPair_injective",
    "finite_int_natAbs_le",
    "finite_rat_height_le",
    "finite_point_height_le",
    "finite_transcendentalRationalPoints",
    "ncard_transcendentalRationalPoints_le_height_slice",
    "countingConclusion_zero_dimensional",
    "pilaWilkie_zero_dimensional",
    "countingConclusion_of_diff_eq_empty",
    "countingConclusion_of_semialgebraic_preconnected_nontrivial",
    "countingConclusion_empty",
)
VALIDATION_DECLARATIONS = (
    "algebraicPart_subset",
    "normalized_components_bounded",
    "zero_dimensional_height",
)
PARTIAL_IDS = [
    "M0441-S-HEIGHT",
    "M0441-S-ALG",
    "M0441-B-ZERO",
    "M0441-B-POS",
    "M0441-L-COUNT",
]
REMAINING_CUT = [
    "M0441-C-PARAM",
    "M0441-L-DET",
    "M0441-C-BLOCKS",
    "M0441-B-INDUCT",
    "M0441-SOURCE",
    "M0441-TRUST",
]
SOURCE_IDENTITY_GATE = (
    "statement.source_identity."
    "unchecked_arity_T_constant_and_algebraic_part_transports"
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
    "execution_rank": 87,
    "phase": "validation",
    "layer": 5,
    "state": "[ ]",
    "depends_on": ["S56-M-0441-PROOF"],
    "owned_paths": [f"Stage1_Instances/{THEOREM}"],
    "deliverable": "Run hermetic kernel, trust, provenance, and independent validation gates.",
    "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
    "attempts": 0,
    "children": [],
}
predecessor = next(row for row in execution["items"] if row["id"] == "S56-M-0441-PROOF")
assert predecessor["state"] == "[_]" and predecessor["attempts"] == 1

assert spec["schema_version"] == "stage1-validation-spec/1.0"
assert spec["item_id"] == ITEM and spec["theorem_id"] == THEOREM
assert spec["argv"] == RECIPE_ARGV
assert spec["cwd"] == "." and spec["network_policy"] == "denied"
assert spec["network_enforcement"] == (
    "the recorded outer bubblewrap argv clears the environment, provides a writable private "
    "/tmp, and denies network access for Python orchestration and all Lean invocations"
)
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
assert set(spec["covered_obligation_ids"]) == {
    "M0441-ROOT", "M0441-S", "M0441-S-OMIN", "M0441-S-HEIGHT",
    "M0441-S-ALG", "M0441-B-ZERO", "M0441-B-POS", "M0441-L-COUNT",
    "M0441-T", "M0441-TRUST",
}
axiom_checked_declarations = {
    "Stage1Instances.THM_M_0441.ObligationTree.engine_compose",
    *("Stage1Instances.THM_M_0441.Proof." + name for name in PROOF_DECLARATIONS),
    *("Stage1Instances.THM_M_0441.Validation." + name for name in VALIDATION_DECLARATIONS),
}
expected_declarations = {
    "Stage1Instances.THM_M_0441.PilaWilkie",
    "Stage1Instances.THM_M_0441.pilaWilkie_iff",
    *axiom_checked_declarations,
}
assert set(spec["covered_declarations"]) == expected_declarations
assert len(spec["covered_declarations"]) == len(expected_declarations)
if receipt is not None and verify_receipt:
    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["release_grade"] is False and receipt["verdict"] == "blocked"
    assert receipt["canonical_target"] == "Stage1Instances.THM_M_0441.PilaWilkie"
    assert receipt["canonical_target_expression_sha256"] == STATEMENT_EXPRESSION_SHA256
    assert "pending" not in receipt["receipt_id"]
    assert receipt["inputs"]["validation_spec_sha256"] == sha256(HERE / "validation-spec.json")
    assert receipt["inputs"]["validator_sha256"] == sha256(Path(__file__).resolve())
    assert receipt["inputs"]["validation_probe_sha256"] == sha256(HERE / "Validation.lean")
    assert receipt["inputs"]["source_crosswalk_sha256"] == sha256(
        HERE / "source-statement-crosswalk.md"
    )
    assert receipt["recipe"] == {
        key: spec[key]
        for key in (
            "recipe_id", "cwd", "argv", "env_allowlist",
            "timeout_seconds", "network_policy", "network_enforcement", "expected_exit",
        )
    }
    assert receipt["result"]["root_kernel_closed"] is False
    assert receipt["result"]["root_closed"] is False
    assert receipt["result"]["audit_complete"] is False
    assert receipt["result"]["theorem_complete"] is False
    assert receipt["result"]["accepted_state_changed"] is False
    assert receipt["result"]["provisionally_closed_obligation_ids"] == []
    assert receipt["result"]["accepted_closed_obligation_ids"] == []
    assert receipt["result"]["frozen_graph_remaining_root_cut_set"] == REMAINING_CUT
    assert receipt["result"]["effective_remaining_root_cut_set"] == [
        SOURCE_IDENTITY_GATE,
        *REMAINING_CUT,
    ]
    assert set(receipt["changed_paths"]) == CHANGED_PATHS
    assert receipt["trust"]["elaborated_declaration_count"] == len(expected_declarations)
    assert receipt["trust"]["axiom_reported_declaration_count"] == len(
        axiom_checked_declarations
    )
    assert receipt["trust"]["accepted_foundation_profile"] is False
    assert receipt["trust"]["complete_transitive_trust_closure"] is False
    assert receipt["provenance"]["proof_dependency_master_accepted"] is False
    assert receipt["provenance"][
        "complete_terminal_body_import_artifact_source_boundary_and_tcb_closure"
    ] is False
    assert receipt["provenance"]["root_provenance_closure"] == "open"
    assert receipt["hermeticity"]["fresh_clean_checkout"] is False
    assert receipt["hermeticity"]["empty_user_package_and_build_caches"] is False
    assert receipt["hermeticity"]["cold_dependency_rebuild"] is False
    assert receipt["hermeticity"]["decision"].startswith("fail_closed")
    assert receipt["independent_validation"]["distinct_verifier_identity"] is False
    assert receipt["independent_validation"]["second_signed_attestation"] is False
    assert receipt["independent_validation"][
        "independently_implemented_minimal_release_verifier"
    ] is False
    assert receipt["independent_validation"]["decision"] == "fail_closed"
    assert receipt["result"]["complete_transitive_provenance_gate"] == "fail_closed"
    assert receipt["result"]["complete_transitive_tcb_gate"] == "fail_closed"
    assert receipt["result"]["hermetic_release_gate"] == "fail_closed"
    assert receipt["result"]["independent_verification_gate"] == "fail_closed"
    assert receipt["first_failed_release_gate"] == "S56-10.6-HERMETIC-COLD-EMPTY-CACHE"
    assert receipt["first_failed_gate"] == (
        SOURCE_IDENTITY_GATE
    )
    assert receipt["result"]["source_statement_identity_gate"] == "fail_closed"
    assert receipt["result"]["root_vector_before"] == receipt["result"]["root_vector_after"]
    assert receipt["result"]["root_vector_after"] == {"H": "H1", "M": "M3", "R": "R4"}
    assert receipt["result"]["proposed_candidate_source_classification"] == {
        "H": "H1", "M": "M5", "R": "R4"
    }
    assert receipt["result"][
        "proposed_candidate_relative_to_source_machine_debt"
    ] == "M5"
    assert receipt["result"]["upstream_artifact_disposition"] == (
        "invalidate_and_refreeze_pending_master_reconciliation"
    )
    assert receipt["remaining_root_cut_set"] == [SOURCE_IDENTITY_GATE, *REMAINING_CUT]
    assert receipt["evidence_log"]["sha256"] == (
        "72cece4f7dccf051d4e9a7f4dd419a0d7f0bf74f0c6c93fa4599a73fe17120c4"
    )
    assert receipt["evidence_log"]["bytes"] == 427
    assert receipt["evidence_log"]["exit_code"] == 0
    assert receipt["validation_started_at"] < receipt["validation_ended_at"]
    assert receipt["validated_at"] == receipt["validation_ended_at"]
    assert receipt["repository_state"]["accepted_state_changed"] is False
    assert receipt["status_boundary"].startswith(
        "Self-tested nonrelease worker evidence"
    )

formal = statement["canonical_formal_target"]
assert formal["statement_file_sha256"] == sha256(HERE / "Statement.lean")
assert formal["elaborated_expression_sha256"] == STATEMENT_EXPRESSION_SHA256
assert registry["root_obligation_id"] == "M0441-ROOT"
assert registry["frozen_against_statement_sha256"] == sha256(HERE / "Statement.lean")
assert registry["frozen_against_anchor_audit_sha256"] == sha256(HERE / "anchor-audit.json")
assert len(registry["obligations"]) == 21
closure = graphs["closure_boundary"]
assert closure["closed_obligations"] == []
assert closure["conditionally_composed_obligations"] == ["M0441-T"]
assert closure["root_closed"] is False
assert closure["audit_complete"] is False
assert closure["theorem_complete"] is False
assert closure["remaining_root_cut_set"] == REMAINING_CUT

assert proof_receipt["support_state"] == "provisional_worker_selftest"
assert proof_receipt["accepted"] is False
assert proof_receipt["provisionally_closed_obligation_ids"] == []
assert proof_receipt["partial_progress_toward_obligation_ids"] == PARTIAL_IDS
assert proof_receipt["accepted_closed_obligation_ids"] == []
assert proof_receipt["proof_body"]["source_sha256"] == sha256(HERE / "Proof.lean")
assert proof_receipt["inputs"]["Statement.lean"] == sha256(HERE / "Statement.lean")
assert proof_receipt["inputs"]["ObligationTree.lean"] == sha256(HERE / "ObligationTree.lean")
assert proof_receipt["inputs"]["obligation-registry.json"] == sha256(
    HERE / "obligation-registry.json"
)
assert proof_receipt["inputs"]["typed-graphs.json"] == sha256(HERE / "typed-graphs.json")
assert proof_receipt["inputs"]["anchor-audit.json"] == sha256(HERE / "anchor-audit.json")
assert proof_receipt["result"]["root_kernel_closed"] is False
assert proof_receipt["result"]["theorem_complete"] is False
assert proof_receipt["remaining_root_cut_set"] == REMAINING_CUT
assert proof_blocker["provisionally_closed_obligation_ids"] == []
assert proof_blocker["root_closed"] is False
assert proof_blocker["theorem_complete"] is False

for relative in CHANGED_PATHS - {".stage1-worker-selftest.json"}:
    data = (ROOT / relative).read_bytes()
    assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())

if receipt is not None and verify_receipt:
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
    ):
        assert receipt["inputs"][key] == sha256(HERE / name), key

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
assert "CountingEngine" not in source_without_comments(
    (HERE / "Validation.lean").read_text(encoding="utf-8")
)
assert "theorem pilaWilkie : PilaWilkie" not in all_source

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
assert anchor["repo_local"]["mathlib_revision"] == MATHLIB_REVISION
assert anchor["repo_local"]["exact_closure_found"] is False
assert statement["checked_transport"] == "Stage1Instances.THM_M_0441.pilaWilkie_iff"
statement_source = (HERE / "Statement.lean").read_text(encoding="utf-8")
assert "forall (n : Nat)" in statement_source
assert "forall T : Nat" in statement_source
assert "exists c : Real, 0 < c" in statement_source
assert "theorem pilaWilkie_iff" in statement_source and "Iff.rfl" in statement_source
crosswalk_source = (HERE / "source-statement-crosswalk.md").read_text(encoding="utf-8")
assert "positive-dimensional semialgebraic subsets" in crosswalk_source
assert "positive dimension encoded by nontriviality" in crosswalk_source
assert "every natural `T >= 1`" in crosswalk_source

account_home = Path(pwd.getpwuid(os.getuid()).pw_dir)
toolchain_bin = account_home / ".elan" / "toolchains" / (
    "leanprover--lean4---v4.29.0"
) / "bin"
lean = toolchain_bin / "lean"
lake = toolchain_bin / "lake"
assert lean.is_file() and lake.is_file(), "pinned local Lean toolchain is unavailable"
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
lean_path = run([str(lake), "env", "printenv", "LEAN_PATH"], cwd=LEAN_ROOT, env=fixed_env).strip()
bwrap = Path(shutil.which("bwrap") or "")
assert lean.is_file() and lake.is_file() and bwrap.is_file()
assert sha256(lean) == LEAN_SHA256 and sha256(lake) == LAKE_SHA256
assert bwrap == Path("/usr/bin/bwrap") and sha256(bwrap) == BWRAP_SHA256
assert sha256(Path("/usr/bin/python3")) == PYTHON_SHA256
assert LEAN_COMMIT in run([str(lean), "--version"], cwd=LEAN_ROOT, env=fixed_env)

tmp = Path(tempfile.mkdtemp(prefix="stage1-m0441-validation-", dir="/tmp"))
try:
    for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
        shutil.copy2(HERE / name, tmp / name)
    (tmp / "home").mkdir()

    def isolated_lean(args: list[str], *, module_path: bool = False) -> str:
        path = f"{tmp}:{lean_path}" if module_path else lean_path
        return run(
            [
                str(lake),
                "env",
                "lean",
                "--trust=0",
                *args,
            ],
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

composition = "Stage1Instances.THM_M_0441.ObligationTree.engine_compose"
assert reported_axioms(obligation_output, composition) <= EXPECTED_AXIOMS
for short_name in PROOF_DECLARATIONS:
    declaration = "Stage1Instances.THM_M_0441.Proof." + short_name
    assert reported_axioms(proof_output, declaration) <= EXPECTED_AXIOMS
for short_name in VALIDATION_DECLARATIONS:
    declaration = "Stage1Instances.THM_M_0441.Validation." + short_name
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
    if verify_receipt:
        assert receipt is not None and packet["known_failures"] == receipt["known_failures"]
    actual_changes = {
        line[3:] for line in run(
            ["git", "status", "--short", "--untracked-files=all"]
        ).splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual_changes == CHANGED_PATHS, (actual_changes, CHANGED_PATHS)
    packet_bytes = selftest_path.read_bytes()
    assert packet_bytes.endswith(b"\n") and b"\r" not in packet_bytes
    assert all(not line.endswith((b" ", b"\t")) for line in packet_bytes.splitlines())

print("PASS THM-M-0441 network-isolated trust-zero replay of the frozen Lean target")
print("PASS conditional composition, 14 proof declarations, and 3 differential declarations use only the selected classical axiom subset")
print("PASS frozen hashes, proof receipt, placeholder scan, pinned mathlib provenance, and honest open-M3 boundary")
print("OPEN source-identity transport and M0441-C-PARAM; hermetic release and distinct-runner verification fail closed")
