#!/usr/bin/env python3
"""Fail-closed narrow validation for S56-M-1272-VALIDATION."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-1272"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
ITEM = "S56-M-1272-VALIDATION"
THEOREM = "THM-M-1272"
EXPECTED_MATHLIB = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
EXPECTED_MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
PROVISIONAL_IDS = [
    "M1272-L-LEVEL-BOUNDED",
    "M1272-L-PS-SUBSEQUENCE",
    "M1272-L-LIMIT-PASSAGE",
    "M1272-T-CRITICAL-LEVELS",
]
OPEN_CUT = [
    "M1272-N-SYMMETRIC",
    "M1272-C-MINIMAX",
    "M1272-L-LINKING",
    "M1272-C-DEFORMATION",
    "M1272-T-LOWER-BOUND",
]
PROOF_DECLARATIONS = {
    "Stage1Instances.THM_M_1272.bounded_values_of_level_tendsto",
    "Stage1Instances.THM_M_1272.palaisSmale_subsequence",
    "Stage1Instances.THM_M_1272.critical_point_at_level_of_subsequence",
    "Stage1Instances.THM_M_1272.fountainLimitPackage_proof",
}
PROOF_CONDITIONAL_ROOT = (
    "Stage1Instances.THM_M_1272.fountainTheoremTarget_of_minimax"
)
VALIDATION_DECLARATIONS = {
    "Stage1Instances.THM_M_1272.Validation.convergent_level_has_bounded_range",
    "Stage1Instances.THM_M_1272.Validation.extract_level_subsequence",
    "Stage1Instances.THM_M_1272.Validation.identify_level_limit",
    "Stage1Instances.THM_M_1272.Validation.independentlyReconstructedLimitPackage",
}
VALIDATION_CONDITIONAL_ROOT = (
    "Stage1Instances.THM_M_1272.Validation.independentlyValidatedConditionalRoot"
)

if sys.flags.optimize != 0:
    raise SystemExit("validation requires Python optimization to be disabled")
if os.environ.get("STAGE1_NETWORK_DENIED") != "1":
    raise SystemExit("validation must run inside the network-denied wrapper")


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict), path
    return value


def run(
    argv: list[str],
    *,
    cwd: Path = ROOT,
    env: dict[str, str] | None = None,
    timeout: int = 900,
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
    if result.returncode:
        raise SystemExit(
            f"validation failed ({result.returncode}): {argv!r}\n{result.stdout}"
        )
    return result.stdout


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["/usr/bin/git", *args], cwd=cwd).strip()


def without_comments(source: str) -> str:
    source = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
    return re.sub(r"--.*$", "", source, flags=re.MULTILINE)


def axiom_reports(output: str) -> dict[str, set[str]]:
    reports: dict[str, set[str]] = {}
    for declaration, body in re.findall(
        r"'([^']+)' depends on axioms:\s*\[([^]]*)\]", output, re.DOTALL
    ):
        reports[declaration] = {
            part.strip()
            for part in body.replace("\n", " ").split(",")
            if part.strip()
        }
    return reports


def sandboxed_lean(
    lean: str, lean_path: str, tmp: Path, source_name: str
) -> str:
    env = {
        "HOME": str(tmp / "home"),
        "TMPDIR": str(tmp),
        "LANG": "C.UTF-8",
        "LC_ALL": "C.UTF-8",
        "TZ": "UTC",
        "LEAN_NUM_THREADS": "1",
        "LEAN_PATH": f"{tmp}:{lean_path}",
    }
    return run(
        [
            lean,
            "--trust=0",
            "-t0",
            "-o",
            source_name.replace(".lean", ".olean"),
            source_name,
        ],
        cwd=tmp,
        env=env,
        timeout=900,
    )


spec = load(HERE / "validation-spec.json")
receipt = load(HERE / "validation-receipt.json")
instance = load(HERE / "instance.json")
statement = load(HERE / "statement.json")
anchor = load(HERE / "anchor-audit.json")
registry = load(HERE / "obligation-registry.json")
graphs = load(HERE / "typed-graphs.json")
old_specs = load(HERE / "validation-specs.json")
proof_receipt = load(HERE / "proof-receipt.json")
execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")

assert spec["item_id"] == receipt["item_id"] == ITEM
assert spec["theorem_id"] == receipt["theorem_id"] == THEOREM
assert len(spec["recipes"]) == 1
recipe = spec["recipes"][0]
assert receipt["recipe"] == recipe
assert recipe["recipe_id"] == "S56-M-1272-VALIDATION-fail-closed-v1"
assert recipe["cwd"] == "."
assert recipe["argv"] == [
    "/usr/bin/bash",
    "Stage1_Instances/THM-M-1272/check_validation.sh",
]
assert recipe["env_allowlist"] == {
    "LANG": "C.UTF-8",
    "LC_ALL": "C.UTF-8",
    "TZ": "UTC",
    "LEAN_NUM_THREADS": "1",
    "PATH": (
        "explicitly variable for tool discovery; every invoked executable "
        "is identity-checked"
    ),
}
assert recipe["timeout_seconds"] == 900
assert recipe["expected_exit"] == 0 and recipe["network_policy"] == "denied"
assert recipe["network_enforcement"] == (
    "the complete Python recipe and every child process run inside bubblewrap "
    "--unshare-net with --clearenv and a read-only host filesystem"
)
assert recipe["expected_outputs"] == [
    {
        "path_or_stream": "stdout",
        "semantic_hash_policy": (
            "contains PASS THM-M-1272 narrow validation and explicit "
            "fail-closed root and release gates"
        ),
    }
]
assert recipe["covered_obligation_ids"] == PROVISIONAL_IDS
assert set(recipe["covered_declarations"]) == (
    PROOF_DECLARATIONS | VALIDATION_DECLARATIONS
)
assert receipt["repository_state"]["commit"] == git("rev-parse", "HEAD")
assert receipt["repository_state"]["tree"] == git("rev-parse", "HEAD^{tree}")
assert receipt["base_revision"] == receipt["repository_state"]["commit"]
assert receipt["base_tree"] == receipt["repository_state"]["tree"]
lake_link = LEAN_ROOT / ".lake"
assert lake_link.is_symlink()
assert hashlib.sha256(os.readlink(lake_link).encode()).hexdigest() == receipt[
    "repository_state"
]["pre_existing_untracked_symlink_text_sha256"]

validation_item = next(row for row in execution["items"] if row["id"] == ITEM)
proof_item = next(
    row for row in execution["items"] if row["id"] == "S56-M-1272-PROOF"
)
assert validation_item["phase"] == "validation"
assert validation_item["state"] in {"[ ]", "[_]"}
assert validation_item["depends_on"] == [proof_item["id"]]
assert validation_item["owned_paths"] == [f"Stage1_Instances/{THEOREM}"]
assert proof_item["state"] == "[_]"

assert statement["canonical_formal_target"]["statement_file_sha256"] == digest(
    HERE / "Statement.lean"
)
assert statement["canonical_formal_target"]["elaborated_expression_sha256"] == (
    "529bd5aeec0b1e9e58034f05dc03531a3fd9063547aeb54b68d5c0821d46cd31"
)
assert registry["root_obligation_id"] == "M1272-ROOT"
assert registry["denominator_sha256"] == graphs["registry_denominator_sha256"]

closure = graphs["closure_boundary"]
assert closure["root_closed"] is False
assert closure["root_machine_debt"] == "M3"
assert closure["theorem_complete"] is False
assert closure["first_open_cut_set"] == [
    "M1272-T-LOWER-BOUND",
    "M1272-T-CRITICAL-LEVELS",
]
assert receipt["result"]["authoritative_graph_state"] == (
    "stale relative to proof receipt and pending master reconciliation"
)

assert proof_receipt["item_id"] == proof_item["id"]
assert proof_receipt["theorem_id"] == THEOREM
assert proof_receipt["support_state"] == "provisional_worker_selftest"
assert proof_receipt["accepted"] is False
assert proof_receipt["provisionally_closed_obligation_ids"] == PROVISIONAL_IDS
assert proof_receipt["open_root_cut_set"] == OPEN_CUT
assert proof_receipt["result"]["root_kernel_closed"] is False
assert proof_receipt["result"]["theorem_complete"] is False
assert proof_receipt["proof_body"]["source_sha256"] == digest(HERE / "Proof.lean")
assert proof_receipt["inputs"]["statement_sha256"] == digest(HERE / "Statement.lean")
assert proof_receipt["inputs"]["obligation_tree_sha256"] == digest(
    HERE / "ObligationTree.lean"
)
assert proof_receipt["inputs"]["obligation_registry_sha256"] == digest(
    HERE / "obligation-registry.json"
)
assert proof_receipt["inputs"]["typed_graphs_sha256"] == digest(
    HERE / "typed-graphs.json"
)
assert proof_receipt["inputs"]["validation_specs_sha256"] == digest(
    HERE / "validation-specs.json"
)
assert proof_receipt["inputs"]["anchor_audit_sha256"] == digest(
    HERE / "anchor-audit.json"
)
fingerprints = {
    row["obligation_id"]: row["statement_fingerprint"]
    for row in registry["obligations"]
}
for obligation_id in PROVISIONAL_IDS:
    assert proof_receipt["obligation_statement_fingerprints"][obligation_id] == (
        fingerprints[obligation_id]
    )

assert old_specs["item_id"] == "S56-M-1272-OBLIGATION_TREE"
old_argv = {tuple(row["argv"]) for row in old_specs["recipes"]}
assert old_argv == {
    ("python3", "Stage1_Instances/THM-M-1272/check_obligation_tree.py"),
    ("python3", "Stage1_Instances/THM-M-1272/check_lean_composition.py"),
}
assert receipt["result"]["legacy_validation_specs_gate"] == "fail_closed"

assert instance["foundation_profile"] == (
    "Lean 4 dependent type theory with mathlib analysis; statement is "
    "noncomputable and asserts no proof"
)
assert receipt["result"]["foundation_profile_gate"] == "fail_closed"
assert receipt["result"]["complete_transitive_tcb_gate"] == "fail_closed"

for relative, expected in receipt["inputs"].items():
    assert digest(ROOT / relative) == expected, f"stale validation input: {relative}"

prohibited = re.compile(
    r"\b(?:sorry|admit|sorryAx|implemented_by|native_decide|extern|opaque)\b"
    r"|^[ \t]*(?:axiom|unsafe|constant)\b",
    re.MULTILINE,
)
for name in (
    "Statement.lean",
    "AnchorAudit.lean",
    "ObligationTree.lean",
    "Proof.lean",
    "Validation.lean",
):
    source = without_comments((HERE / name).read_text(encoding="utf-8"))
    assert prohibited.search(source) is None, f"prohibited proof device in {name}"
validation_source = without_comments(
    (HERE / "Validation.lean").read_text(encoding="utf-8")
)
assert not re.search(r"^import\s+Proof\s*$", validation_source, re.MULTILINE)
for declaration in (
    "bounded_values_of_level_tendsto",
    "palaisSmale_subsequence",
    "critical_point_at_level_of_subsequence",
    "fountainLimitPackage_proof",
    "fountainTheoremTarget_of_minimax",
):
    assert declaration not in validation_source

assert digest(LEAN_ROOT / "lean-toolchain") == (
    "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2"
)
assert digest(LEAN_ROOT / "lake-manifest.json") == (
    "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81"
)
manifest = load(LEAN_ROOT / "lake-manifest.json")
mathlib_record = next(p for p in manifest["packages"] if p["name"] == "mathlib")
assert mathlib_record["rev"] == EXPECTED_MATHLIB
mathlib = (LEAN_ROOT / ".lake" / "packages" / "mathlib").resolve()
assert mathlib.is_dir(), "pinned mathlib artifact is unavailable"
assert run(["/usr/bin/git", "rev-parse", "HEAD"], cwd=mathlib).strip() == EXPECTED_MATHLIB
assert run(["/usr/bin/git", "rev-parse", "HEAD^{tree}"], cwd=mathlib).strip() == (
    EXPECTED_MATHLIB_TREE
)
assert run(["/usr/bin/git", "status", "--porcelain=v1"], cwd=mathlib) == ""

provenance = receipt["selected_provenance"]
anchor_mathlib = next(
    row for row in anchor["immutable_dependencies"] if row["name"] == "mathlib"
)
assert anchor_mathlib["revision"] == provenance["revision"] == EXPECTED_MATHLIB
assert provenance["tree"] == EXPECTED_MATHLIB_TREE
assert run(["/usr/bin/git", "remote", "get-url", "origin"], cwd=mathlib).strip() == (
    provenance["remote"]
)
for record in provenance["selected_import_sources"]:
    source = mathlib / record["file"]
    olean = mathlib / record["olean"]
    assert digest(source) == record["source_sha256"]
    assert run(
        ["/usr/bin/git", "rev-parse", f"HEAD:{record['file']}"], cwd=mathlib
    ).strip() == record["git_blob"]
    assert digest(olean) == record["olean_sha256"]
assert digest(mathlib / "LICENSE") == provenance["license_sha256"]

lean = os.environ["STAGE1_LEAN_BIN"]
lean_path = os.environ["STAGE1_LEAN_PATH"]
lake = str(Path(lean).with_name("lake"))
assert digest(Path(lean)) == receipt["environment"]["lean_executable_sha256"]
assert digest(Path(lake)) == receipt["environment"]["lake_executable_sha256"]
assert digest(Path(shutil.which("bwrap") or "")) == receipt["environment"][
    "bubblewrap_sha256"
]
assert digest(Path(sys.executable)) == receipt["environment"][
    "python_executable_sha256"
]
assert digest(Path("/usr/bin/git")) == receipt["environment"][
    "git_executable_sha256"
]

with tempfile.TemporaryDirectory(prefix="m1272-validation-") as tmp_name:
    tmp = Path(tmp_name)
    (tmp / "home").mkdir()
    for name in (
        "Statement.lean",
        "AnchorAudit.lean",
        "ObligationTree.lean",
        "Proof.lean",
        "Validation.lean",
    ):
        shutil.copy2(HERE / name, tmp / name)
    outputs = {
        name: sandboxed_lean(lean, lean_path, tmp, name)
        for name in (
            "Statement.lean",
            "AnchorAudit.lean",
            "ObligationTree.lean",
            "Proof.lean",
            "Validation.lean",
        )
    }

proof_reports = axiom_reports(outputs["Proof.lean"])
assert proof_reports == {
    **{declaration: EXPECTED_AXIOMS for declaration in PROOF_DECLARATIONS},
    PROOF_CONDITIONAL_ROOT: EXPECTED_AXIOMS,
}
validation_reports = axiom_reports(outputs["Validation.lean"])
assert validation_reports == {
    **{declaration: EXPECTED_AXIOMS for declaration in VALIDATION_DECLARATIONS},
    VALIDATION_CONDITIONAL_ROOT: EXPECTED_AXIOMS,
}
combined_output = "\n".join(outputs.values())
assert "declaration uses 'sorry'" not in combined_output
assert "sorryAx" not in combined_output
assert "error:" not in combined_output

result = receipt["result"]
assert result["accepted_closed_obligation_ids"] == []
assert result["locally_revalidated_provisional_obligation_ids"] == PROVISIONAL_IDS
assert result["root_closed"] is False
assert result["root_machine_debt"] == "M3"
assert result["audit_complete"] is False
assert result["theorem_complete"] is False
assert digest(ROOT / result["stdout_stderr_path"]) == result[
    "stdout_stderr_sha256"
]
receipt_basis = {
    "spec": receipt["recipe"],
    "inputs": receipt["inputs"],
    "result": {
        key: result[key]
        for key in (
            "exit_code",
            "stdout_stderr_sha256",
            "locally_revalidated_provisional_obligation_ids",
            "root_closed",
            "root_machine_debt",
            "foundation_profile_gate",
            "root_kernel_closure_gate",
            "complete_transitive_provenance_gate",
            "complete_transitive_tcb_gate",
            "hermetic_release_gate",
            "independent_distinct_runner_gate",
        )
    },
    "base_revision": receipt["base_revision"],
    "base_tree": receipt["base_tree"],
}
receipt_digest = hashlib.sha256(
    json.dumps(receipt_basis, sort_keys=True, separators=(",", ":")).encode()
).hexdigest()
assert receipt["receipt_id"] == f"{ITEM}-BLOCKED-{receipt_digest[:16]}"
for gate in (
    "foundation_profile_gate",
    "root_kernel_closure_gate",
    "complete_transitive_provenance_gate",
    "complete_transitive_tcb_gate",
    "hermetic_release_gate",
    "independent_distinct_runner_gate",
    "legacy_validation_specs_gate",
):
    assert result[gate] == "fail_closed"
assert receipt["release_grade"] is False
assert receipt["support_state"] == "provisional_worker_selftest"
assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False

selftest_path = ROOT / ".stage1-worker-selftest.json"
selftest = load(selftest_path)
assert set(selftest) == {
    "item_id",
    "changed_paths",
    "commands",
    "output_summary",
    "base_revision",
    "known_failures",
    "state",
}
assert selftest["item_id"] == ITEM and selftest["state"] == "[_]"
assert selftest["base_revision"] == receipt["base_revision"]
assert selftest["changed_paths"] == receipt["changed_paths"]
assert selftest["known_failures"] == receipt["known_failures"]

print("PASS THM-M-1272 narrow validation")
print(
    "kernel: four partial proof obligations and four separately reconstructed "
    "probes replayed at trust zero with network denied"
)
print(
    "trust: machine reports only propext, Classical.choice, Quot.sound; "
    "no sorry or prohibited local device"
)
print(
    "provenance: proof hashes, selected mathlib sources/oleans/license, "
    "clean pin, and tool identities agree"
)
print(
    "root open: symmetric normalization, minimax construction, linking, "
    "odd deformation, and lower-bound package remain unproved"
)
print(
    "blocked: proof master acceptance, accepted foundation profile, cold "
    "empty-cache release replay, complete trust/provenance, and distinct-runner verification"
)
