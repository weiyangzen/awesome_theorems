#!/usr/bin/env python3
"""Fail-closed narrow validation for S56-M-1291-VALIDATION."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-1291"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM = "S56-M-1291-VALIDATION"
THEOREM = "THM-M-1291"
BASE_REVISION = "a1a7e939e58f103f5ff5d23af51437fa8658aa04"
BASE_TREE = "d881fd9641fa3e5f3ebe5082b35672981e90adcf"
EXPRESSION_SHA256 = "d33af3afa4d754bac48547f753d7bda319f46e538766e7c763fa437376599884"
DENOMINATOR_SHA256 = "4331556ba27d32b56189b66a2438dd243ec27af5396f615cc98bb7a763be4748"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_REMOTE = "https://github.com/leanprover-community/mathlib4.git"
MATHLIB_LICENSE_SHA256 = "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
LEAN_TOOLCHAIN = "leanprover/lean4:v4.29.0"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
MACHINE_IDS = [
    "M1291-ROOT",
    "M1291-S-STATEMENT",
    "M1291-S-MEASURABILITY",
    "M1291-S-BOUNDARY",
    "M1291-S-FOUNDATION",
    "M1291-B-SUBUNIT",
    "M1291-B-SUPERUNIT",
    "M1291-B-MERGE",
    "M1291-L-POINTWISE",
    "M1291-L-TRUNCATION",
    "M1291-L-TAIL",
    "M1291-T-INTEGRAL",
    "M1291-T-ALGEBRA",
    "M1291-T-ASSEMBLE",
]
TRUST_DECLARATIONS = [
    "Stage1Instances.THM_M_1291.rpow_add_le_weighted",
    "Stage1Instances.THM_M_1291.abs_rpow_norm_sub_rpow_norm_sub_le_weighted",
    "Stage1Instances.THM_M_1291.rpow_coeff_tendsto_zero",
    "Stage1Instances.THM_M_1291.truncatedError_nonneg",
    "Stage1Instances.THM_M_1291.truncatedError_le",
    "Stage1Instances.THM_M_1291.integrable_of_ae_tendsto_of_uniform_integral_bound",
    "Stage1Instances.THM_M_1291.abs_rpow_norm_add_sub_rpow_norm_le",
    "Stage1Instances.THM_M_1291.splittingLimit_subunit",
    "Stage1Instances.THM_M_1291.splittingLimit_superunit",
    "Stage1Instances.THM_M_1291.brezisLiebTarget_proof",
]
EXPECTED_INPUTS = {
    "Statement.lean": "ef19e70e68cd8c9179130141706954825b7de8529ecef6aec1dc6e87c76dd92f",
    "Proof.lean": "a5e3f1e9abd93eb15b124eb7bdd8fd3e860154e7f5bada6326f6d88115ecdbc9",
    "statement.json": "8d40d41aced47bc55716b67c6bba43a9c2489f887acd00ea3e8e18fa86c031fb",
    "anchor-audit.json": "73af9e5e2684eb44c168186204372a46ba8c507a3249840eef2cec9b58d06403",
    "obligation-registry.json": "b432ca10fd9904d2a94fc51391dac293b8cffcd23339a5196d50db7eba4f05a7",
    "typed-graphs.json": "b6f34e8196e95a4c043b5868be326f3cc377c7629adbf9334d71aca1f9a317bc",
    "validation-specs.json": "606da9f56786306136b50a9a59ace3875be0ac4b5a70795855cb9c64eb9cacee",
    "proof-receipt.json": "e7a32f380d5537bb49cb5a1a58affda62e58c7ecb50b6c82011ead48d32ff014",
    "source-statement-crosswalk.md": "3544bc9220f7855118cd63edeac8ef362af534196ca57d57db0e405e1f89ef53",
    "check_obligation_tree.py": "f80f4a2c1fbb9eacfddd4694ca13904804e421071d3293ba76c3330530ce7518",
    "Validation.lean": "8d9a105d0375254dfe0b7e96f0454e7ffa8821b025105bf3498fc2ad26bade98",
    "check_validation.sh": "429a5ff515401f8d02e78b8e8290a492624a8ca1e9e55cb098f622fe91bda0bc",
    "validation-spec.json": "81dbad7a7c7cccf74d09164b8f68bc365f20dbaf8971235657aff2f04da0f4a7",
}
EXPECTED_TOOL_INPUTS = {
    "lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
MATHLIB_SOURCES = {
    "Mathlib/Analysis/MeanInequalitiesPow.lean": (
        "9e374a5d1316bdf34a6eaa6c65af1216faf4be7d",
        "a57a98dcddef9c9f1b6e1efbe55f3fa7fa3744d7b65aa82af5ae4881ca231d8b",
    ),
    "Mathlib/MeasureTheory/Integral/Bochner/Basic.lean": (
        "587ad1e81dc387ba2835c29c4ef7aa05c5efd82e",
        "b2e4b3eb233147e1dc8d2cb8fa4eae1773badbf1e37234dd7e8dfd54d9dd0a0a",
    ),
    "Mathlib/MeasureTheory/Integral/DominatedConvergence.lean": (
        "3aeb4ace15863cef3af283800c10f7d670c3727c",
        "967aff89500aeff8a1a94358c79bb3200c4e77bdfabe1e6481d2beeda67f6191",
    ),
    "Mathlib/MeasureTheory/Integral/Lebesgue/Add.lean": (
        "17113077f84df615241945254dde4dfeed2cd23a",
        "992bbef3b374a1bc0d2677d91e48195121d4adc86d08ccae8c0f735b7a596186",
    ),
}
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/Validation.lean",
    f"Stage1_Instances/{THEOREM}/check_validation.py",
    f"Stage1_Instances/{THEOREM}/check_validation.sh",
    f"Stage1_Instances/{THEOREM}/validation-phase.md",
    f"Stage1_Instances/{THEOREM}/validation-receipt.json",
    f"Stage1_Instances/{THEOREM}/validation-spec.json",
}
SUMMARY_LINES = (
    "PASS THM-M-1291 narrow validation",
    "PASS network-isolated trust-zero kernel replay: exact statement, complete local proof, and proof-only trust probe elaborated",
    "PASS hygiene: Lean transitive sorry collectors and a nested-comment-aware prohibited-construct scan passed",
    "PASS selected provenance: frozen local hashes, proof-body identity, selected mathlib source/blob/license, clean pin, and tool identities agree",
    "FAIL CLOSED authority: proof is only provisional; registry and typed graphs accept no proof evidence; accepted root remains H2/M3/R4",
    "FAIL CLOSED node coverage: planned node fingerprints, missing terminal body IDs, and absent composition/evidence links require master reconciliation",
    "FAIL CLOSED foundation/trust: observed axioms are unaccepted and complete transitive declaration, compiled-artifact, and TCB closure are absent",
    "FAIL CLOSED hermetic release: shared warm .lake is not an empty-cache clean-checkout offline replay or deterministic bundle",
    "FAIL CLOSED independent release: trust-only probe shares this worker, checkout, kernel, and cache; no distinct signed runner or minimal verifier exists",
    "audit_complete=false; theorem_complete=false",
)
RECIPE_STARTED = time.monotonic()
RECIPE_TIMEOUT_SECONDS = 900.0


if sys.flags.optimize:
    raise SystemExit("validation failed: Python optimization disables fail-closed assertions")


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict), path
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(argv: list[str], *, cwd: Path = ROOT) -> str:
    remaining = RECIPE_TIMEOUT_SECONDS - (time.monotonic() - RECIPE_STARTED)
    if remaining <= 0:
        raise TimeoutError("validation recipe exceeded its 900-second wall-clock bound")
    result = subprocess.run(
        argv,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=remaining,
        check=False,
    )
    if result.returncode:
        raise RuntimeError(
            f"validation failed ({result.returncode}): {argv!r}\n{result.stdout}"
        )
    return result.stdout


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["git", *args], cwd=cwd).strip()


def elan_binary(name: str) -> Path:
    env = dict(os.environ)
    env["ELAN_TOOLCHAIN"] = LEAN_TOOLCHAIN
    result = subprocess.run(
        ["elan", "which", name],
        cwd=LEAN_ROOT,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=30,
        check=False,
    )
    if result.returncode:
        raise RuntimeError(f"cannot resolve pinned {name}: {result.stdout}")
    path = Path(result.stdout.strip())
    assert path.is_file(), f"pinned {name} executable missing"
    return path


def code_without_comments(source: str) -> str:
    output: list[str] = []
    depth = 0
    index = 0
    while index < len(source):
        if source.startswith("/-", index):
            depth += 1
            index += 2
        elif depth and source.startswith("-/", index):
            depth -= 1
            index += 2
        elif depth:
            index += 1
        elif source.startswith("--", index):
            newline = source.find("\n", index)
            index = len(source) if newline < 0 else newline
        else:
            output.append(source[index])
            index += 1
    assert depth == 0, "unterminated Lean block comment"
    return "".join(output)


def observed_axioms(output: str, declaration: str) -> set[str]:
    match = re.search(
        re.escape(f"'{declaration}' depends on axioms: [") + r"(.*?)]",
        output,
        re.DOTALL,
    )
    if match is None:
        assert f"'{declaration}' does not depend on any axioms" in output, declaration
        return set()
    return {part.strip() for part in match.group(1).split(",") if part.strip()}


def assert_text_hygiene(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())


def main() -> None:
    targets = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    statement = load(HERE / "statement.json")
    anchor = load(HERE / "anchor-audit.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    frozen_specs = load(HERE / "validation-specs.json")
    proof_receipt = load(HERE / "proof-receipt.json")
    spec = load(HERE / "validation-spec.json")
    receipt = load(HERE / "validation-receipt.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 462 and target["baseline"] == "L0"
    assert target["lifecycle_mode"] == "planned"
    assert target["rework_required"] is True and target["theorem_complete"] is False
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item["theorem_id"] == THEOREM and item["execution_rank"] == 462
    assert item["phase"] == "validation" and item["layer"] == 5
    assert item["state"] in {"[ ]", "[_]"}
    assert item["depends_on"] == ["S56-M-1291-PROOF"]
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM}"]
    assert item["deliverable"] == (
        "Run hermetic kernel, trust, provenance, and independent validation gates."
    )
    assert item["completion_gate"] == (
        "rev-5.6 node-specific receipt and master acceptance"
    )
    assert isinstance(item["attempts"], int) and item["attempts"] >= 0
    assert item["children"] == []
    predecessor = next(
        row for row in execution["items"] if row["id"] == "S56-M-1291-PROOF"
    )
    assert predecessor["state"] in {"[_]", "[x]"}
    assert isinstance(predecessor["attempts"], int) and predecessor["attempts"] >= 1

    for name, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"stale validation input: {name}"
    for name, expected in EXPECTED_TOOL_INPUTS.items():
        assert sha256(LEAN_ROOT / name) == expected, f"changed tool input: {name}"
    formal = statement["canonical_formal_target"]
    assert formal["declaration_or_expression"] == (
        "Stage1Instances.THM_M_1291.BrezisLiebTarget"
    )
    assert formal["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert formal["statement_file_sha256"] == EXPECTED_INPUTS["Statement.lean"]
    assert registry["frozen_against_statement_sha256"] == EXPECTED_INPUTS["Statement.lean"]
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert registry["frozen_denominators"]["required_machine"] == MACHINE_IDS
    assert graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    closure = graphs["closure_boundary"]
    assert closure["closed_obligations"] == [] and closure["root_closed"] is False
    assert closure["remaining_root_cut_set"] == ["M1291-T-INTEGRAL"]
    assert closure["composition_certificates"] == []
    assert closure["audit_complete"] is closure["theorem_complete"] is False

    assert proof_receipt["item_id"] == "S56-M-1291-PROOF"
    assert proof_receipt["accepted"] is False
    assert proof_receipt["canonical_target_expression_sha256"] == EXPRESSION_SHA256
    assert proof_receipt["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert proof_receipt["provisionally_closed_obligation_ids"] == MACHINE_IDS
    assert proof_receipt["accepted_closed_obligation_ids"] == []
    assert proof_receipt["proof_body"]["source_sha256"] == EXPECTED_INPUTS["Proof.lean"]
    assert proof_receipt["result"]["root_kernel_closed"] is True
    assert proof_receipt["result"]["accepted_root_closed"] is False
    assert proof_receipt["result"]["theorem_complete"] is False
    assert len(proof_receipt["exact_declarations"]) == 3
    assert all(
        row["terminal_proof_body_id"] is None for row in registry["obligations"]
    )
    assert all(
        not node["evidence_ids"] and node["provenance_id"] == "pending"
        for node in graphs["nodes"]
    )
    assert any(
        row["statement_fingerprint"].startswith("planned:v1:")
        for row in registry["obligations"]
    )
    assert frozen_specs["item_id"] == "S56-M-1291-OBLIGATION_TREE"
    assert all(
        recipe["argv"]
        == ["python3", f"Stage1_Instances/{THEOREM}/check_obligation_tree.py"]
        for recipe in frozen_specs["recipes"]
    )

    assert anchor["root_machine_classification"] == "M4"
    assert anchor["theorem_proved"] is anchor["theorem_complete"] is False
    crosswalk = (HERE / "source-statement-crosswalk.md").read_text(encoding="utf-8")
    assert "not `H0`" in crosswalk

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by|extern|oracle)\b|"
        r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
        r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
        r"(?:axiom|constant|opaque|unsafe)\b",
        re.MULTILINE,
    )
    for name in ("Statement.lean", "Proof.lean", "Validation.lean"):
        source = code_without_comments((HERE / name).read_text(encoding="utf-8"))
        assert prohibited.search(source) is None, f"prohibited source token in {name}"
    validation = code_without_comments((HERE / "Validation.lean").read_text())
    assert "import Proof" in validation
    assert "theorem " not in validation and "def " not in validation
    for declaration in TRUST_DECLARATIONS:
        assert f"assert_no_sorry {declaration}" in validation
        assert f"#print sorries {declaration}" in validation
        assert f"#print axioms {declaration}" in validation

    manifest = load(LEAN_ROOT / "lake-manifest.json")
    mathlib_entry = next(row for row in manifest["packages"] if row["name"] == "mathlib")
    assert mathlib_entry["rev"] == mathlib_entry["inputRev"] == MATHLIB_REVISION
    assert MATHLIB.resolve().is_dir(), "pinned mathlib artifact is unavailable"
    assert git("rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert git("remote", "get-url", "origin", cwd=MATHLIB) == MATHLIB_REMOTE
    assert git("status", "--porcelain=v1", "--untracked-files=all", cwd=MATHLIB) == ""
    for relative, (blob, source_digest) in MATHLIB_SOURCES.items():
        assert git("rev-parse", f"HEAD:{relative}", cwd=MATHLIB) == blob
        assert sha256(MATHLIB / relative) == source_digest
    assert sha256(MATHLIB / "LICENSE") == MATHLIB_LICENSE_SHA256

    lean = elan_binary("lean")
    lake = elan_binary("lake")
    lean_version = run([str(lean), "--version"], cwd=LEAN_ROOT)
    lake_version = run([str(lake), "--version"], cwd=LEAN_ROOT)
    assert "4.29.0" in lean_version and LEAN_COMMIT in lean_version
    assert "5.0.0-src+98dc76e" in lake_version
    tools = {
        "lean": lean,
        "lake": lake,
        "python": Path(os.path.realpath(sys.executable)),
        "git": Path(os.path.realpath(shutil.which("git") or "")),
        "bash": Path(os.path.realpath(shutil.which("bash") or "")),
        "bubblewrap": Path(os.path.realpath(shutil.which("bwrap") or "")),
        "elan": Path(os.path.realpath(shutil.which("elan") or "")),
    }
    expected_tools = {
        "lean": "3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf",
        "lake": "a608ff084d7e2af228b92a29d7c2fd083ba0580e46889175ec74a81678c98359",
        "python": "b8d8288faefdd300201f43fcf00f6f539a27218eeed3a3dff5ab10b9c4c99700",
        "git": "8a48eefa306b9a2a9c3e576784a74ad7485779279e5a46ec43361a1864760e45",
        "bash": "3efccc187bafa75ff1e37d246270ab3e7aa559f242c7a52bf3ec2a1b5450bdbd",
        "bubblewrap": "0abea81db798ebf6b4742ac0664802d97521547a353c2a0dbdc21d76cbbfd2c0",
        "elan": "840179e70803ef373c2ec53342d6a45ea7d022533e4145489fc1278b4f716385",
    }
    assert {name: sha256(path) for name, path in tools.items()} == expected_tools

    kernel_output = run(["bash", str(HERE / "check_validation.sh")])
    assert kernel_output.count("Declarations are sorry-free!") == len(TRUST_DECLARATIONS)
    assert "declaration uses 'sorry'" not in kernel_output
    assert "sorryAx" not in kernel_output and "error:" not in kernel_output
    for declaration in TRUST_DECLARATIONS:
        assert observed_axioms(kernel_output, declaration) <= EXPECTED_AXIOMS
    assert (
        observed_axioms(
            kernel_output, "Stage1Instances.THM_M_1291.brezisLiebTarget_proof"
        )
        == EXPECTED_AXIOMS
    )

    assert spec["schema_version"] == "stage1-validation-recipe/1.0"
    assert spec["item_id"] == ITEM and spec["theorem_id"] == THEOREM
    assert spec["cwd"] == "."
    assert spec["argv"] == [
        "python3", "-I", "-B", f"Stage1_Instances/{THEOREM}/check_validation.py"
    ]
    assert set(spec["env_allowlist"]) == {
        "PATH", "HOME", "PYTHONPATH", "LANG", "LC_ALL", "TZ", "LEAN_NUM_THREADS"
    }
    assert spec["timeout_seconds"] == 900
    assert spec["network_policy"] == "denied" and spec["expected_exit"] == 0
    assert "--unshare-net" in spec["network_enforcement"]
    assert spec["covered_obligation_ids"] == MACHINE_IDS
    assert receipt["recipe"] == spec

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["phase"] == "validation" and receipt["intent"] == "validate"
    assert receipt["depends_on"] == ["S56-M-1291-PROOF"]
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["release_grade"] is receipt["content_addressed_release_evidence"] is False
    assert receipt["canonical_target"] == {
        "declaration": "Stage1Instances.THM_M_1291.BrezisLiebTarget",
        "elaborated_expression_sha256": EXPRESSION_SHA256,
        "statement_source_sha256": EXPECTED_INPUTS["Statement.lean"],
        "registry_denominator_sha256": DENOMINATOR_SHA256,
        "exact_statement_delta": "none",
    }
    assert receipt["covered_obligation_ids"] == MACHINE_IDS
    assert receipt["accepted_closed_obligation_ids"] == []
    assert receipt["validated_declarations"] == spec["covered_declarations"]
    for name, expected in EXPECTED_INPUTS.items():
        assert receipt["inputs"][name] == expected, name
    assert receipt["inputs"]["check_validation.py"] == sha256(HERE / "check_validation.py")
    assert receipt["inputs"]["validation-phase.md"] == sha256(HERE / "validation-phase.md")
    expected_kernel_sha = hashlib.sha256(kernel_output.encode("utf-8")).hexdigest()
    assert receipt["result"]["kernel_output_sha256"] == expected_kernel_sha
    assert receipt["result"]["kernel_output_bytes"] == len(kernel_output.encode("utf-8"))
    assert receipt["result"]["network_isolated_trust_zero_replay"] == "pass"
    assert receipt["result"]["exact_root_kernel_replay"] == "provisional_pass"
    assert receipt["result"]["observed_axioms"] == [
        "propext", "Classical.choice", "Quot.sound"
    ]
    assert "transitive Lean sorry closure" in receipt["result"][
        "placeholder_and_unsafe_scan"
    ]
    assert receipt["result"]["selected_provenance"] == (
        "pass_with_incomplete_transitive_closure"
    )
    assert receipt["result"]["proof_master_acceptance"] == "fail_closed"
    assert receipt["result"][
        "node_specific_proof_body_and_composition_mapping"
    ] == "fail_closed"
    assert receipt["result"]["accepted_root_machine_debt"] == "M3"
    assert receipt["result"]["accepted_root_closed"] is False
    assert receipt["result"]["audit_complete"] is receipt["result"]["theorem_complete"] is False
    assert receipt["first_failed_gate"] == "dependency.S56-M-1291-PROOF.master_acceptance"
    assert receipt["first_failed_release_gate"] == "S56-10.6-HERMETIC-COLD-BUILD"
    assert receipt["trust"]["machine_reported_axioms"] == [
        "propext", "Classical.choice", "Quot.sound"
    ]
    assert receipt["trust"]["accepted_foundation_policy"] is False
    assert receipt["trust"]["tcb_gate"] == "fail_closed"
    assert receipt["provenance"]["terminal_declaration"] == TRUST_DECLARATIONS[-1]
    assert receipt["provenance"]["complete_provenance_gate"] == "fail_closed"
    independent = receipt["independent_validation"]
    assert independent["same_worker_trust_probe"] == "pass"
    assert independent["proof_independent_exact_root_probe"] is False
    assert independent["distinct_runner"] is independent["distinct_verifier_identity"] is False
    assert independent["release_gate"] == "fail_closed"
    assert receipt["root_vector_before"] == receipt[
        "root_vector_after_worker_selftest"
    ] == {"H": "H2", "M": "M3", "R": "R4"}
    assert receipt["freshness"]["revocation_state"] == "not_revoked"
    assert receipt["status_boundary"].startswith(
        "Self-tested validation-node evidence"
    )

    assert set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert packet["item_id"] == ITEM and packet["state"] == "[_]"
    assert packet["base_revision"] == BASE_REVISION
    assert set(receipt["changed_paths"]) == set(packet["changed_paths"]) == CHANGED_PATHS
    assert receipt["commands"] == packet["commands"]
    assert receipt["output_summary"] == packet["output_summary"]
    assert receipt["output_summary"] == list(SUMMARY_LINES)
    assert receipt["known_failures"] == packet["known_failures"]
    untracked_hashes = receipt["environment"]["worktree_state"][
        "untracked_input_sha256"
    ]
    assert set(untracked_hashes) == CHANGED_PATHS - {
        f"Stage1_Instances/{THEOREM}/validation-receipt.json"
    }
    for relative, expected in untracked_hashes.items():
        assert sha256(ROOT / relative) == expected, relative
    link_target = os.readlink(LEAN_ROOT / ".lake").encode("utf-8")
    assert hashlib.sha256(link_target).hexdigest() == receipt["environment"][
        "worktree_state"
    ]["preexisting_untracked_link_target_sha256"]

    status = git(
        "status", "--porcelain=v1", "--untracked-files=all", "--",
        str(HERE), str(ROOT / ".stage1-worker-selftest.json"),
    )
    actual_changed = {
        line[3:] if line[:2] == "??" else line[2:].lstrip()
        for line in status.splitlines()
    }
    assert actual_changed == CHANGED_PATHS, (actual_changed, CHANGED_PATHS)
    for relative in CHANGED_PATHS:
        assert_text_hygiene(ROOT / relative)
    for path in (HERE / "validation-receipt.json", HERE / "validation-phase.md"):
        text = path.read_text(encoding="utf-8")
        assert "/home/" not in text and ".cron/" not in text
        assert "theorem_complete=true" not in text

    print("\n".join(SUMMARY_LINES))


if __name__ == "__main__":
    main()
