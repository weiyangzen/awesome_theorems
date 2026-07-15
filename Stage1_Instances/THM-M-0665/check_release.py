#!/usr/bin/env python3
"""Fail-closed release reconciliation for S56-M-0665-RELEASE."""

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


if not __debug__:
    raise SystemExit("release validation requires Python assertions")

ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0665"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
ITEM = "S56-M-0665-RELEASE"
THEOREM = "THM-M-0665"
BASE_REVISION = "1228bcced6922a2593bfd2fcd1e51e2b0c3091e4"
BASE_TREE = "b3af9672c556b77329b9b44d52cc720397c6e43d"
VALIDATION_BASE_REVISION = "443b8bbc23bf35a1e7a4bb7b3183073f76bbee2b"
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
EXPRESSION_SHA256 = "da66c715ce12af9ff6dfb55a721665c8240358c0ee547062b3d2fc10c7785944"
DENOMINATOR_SHA256 = "9aa4a6fe979874ca4baa46f7f6b12d9dd965206a2d05614e70330640ac4303e5"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
INVENTORY_IDS = [
    "M0665-ROOT", "M0665-S-EXACT", "M0665-S-DEFS", "M0665-S-BOUNDARY",
    "M0665-S-TRANSPORT", "M0665-S-FOUNDATION", "M0665-N-ALGEBRAIC",
    "M0665-N-HEIGHT", "M0665-B-DIMENSION", "M0665-B-CHARTS",
    "M0665-C-PARAM", "M0665-C-HYPERSURFACE", "M0665-L-DERIVATIVE",
    "M0665-L-ARITHMETIC", "M0665-L-DROP", "M0665-L-COUNT",
    "M0665-T-ASSEMBLE", "M0665-X-SOURCE", "M0665-X-UPSTREAM",
    "M0665-X-TCB",
]
MACHINE_IDS = INVENTORY_IDS[:17]
PARTIAL_IDS = [
    "M0665-N-ALGEBRAIC", "M0665-N-HEIGHT", "M0665-S-BOUNDARY",
    "M0665-B-DIMENSION", "M0665-L-COUNT",
]
REMAINING_CUT = [
    "M0665-C-PARAM", "M0665-L-DERIVATIVE", "M0665-L-ARITHMETIC",
    "M0665-L-DROP", "M0665-L-COUNT",
]
PROOF_DECLARATIONS = (
    "subset_algebraicPart_of_semialgebraic_preconnected_nontrivial",
    "algebraicPart_subset", "algebraicPart_mono", "normalizedRatPair_injective",
    "finite_int_natAbs_le", "finite_rat_height_le", "finite_point_height_le",
    "finite_transcendentalRationalPoints",
    "ncard_transcendentalRationalPoints_le_height_slice",
    "countingConclusion_zero_dimensional", "pilaWilkie_zero_dimensional",
    "countingConclusion_of_diff_eq_empty",
    "countingConclusion_of_semialgebraic_preconnected_nontrivial",
    "countingConclusion_empty",
)
VALIDATION_DECLARATIONS = (
    "algebraicPart_subset", "normalized_components_bounded",
    "zero_dimensional_height",
)
UPSTREAM_INPUTS = {
    "Statement.lean": "856703261f1e12c4dd91f209bb001cb7b1a5512770117a5f4527a4804439a175",
    "Proof.lean": "27e92adba1ca818a9e0442661c34c9adc4115653ac9a593fa8057fc18d0a6d07",
    "Validation.lean": "d053503d4551c9245620337c321b4d4318a797c5009b4853c71be5b883015f59",
    "statement.json": "171e9bedcb4e6b0a274265e5168e88bdc2c1d269406b6e26dbba55c7acf17d33",
    "anchor-audit.json": "80aa453d71ead0d5385bd5db51fa9434facca89bbb40edb35e7b5308be8c9b69",
    "obligation-registry.json": "9970f070b8590a04767a90697c5f642665e49c35284d99ea854f9fbe24d6c7c4",
    "typed-graphs.json": "80cef15dbfcad6f83047e49e70a2fc92cbc173ed2c9fdbb199ee88740a7c93fe",
    "source-statement-crosswalk.md": "218aba29acb99d6f6ef292aca5e6e61acd527759f0c44c83b6372da08a581fe1",
    "instance.json": "6e0400896f8fd3cd402ebc805b573b01374dc7800950c913cf0b844d419041e9",
    "task-dag.json": "8e66260b160742e44464927fa1beede3350c58340696bea8be7ddfb530281fba",
    "proof-receipt.json": "b5347fc4202a439512ee721e8d70c6c0f289bfc881ad3e8f5b3123754a021231",
    "proof-blocker.json": "c00159b709a114173d78fd2cfe0221b3f82a3a8b09ebfed8001875d6776e3f20",
    "validation-spec.json": "9b763acf0122ddc8032a874278ff4b5fef366b089ff4afa212a42e67c7ce6ed4",
    "validation-receipt.json": "eaca5aced603ccafc806c0f9ede565b972150a5fb64a0dd7a2faa8b57b261dc6",
    "check_validation.py": "e530a8b7b22891cb6402b5a726aa8e9e0eebbb424476bad57f6ca02434aace5e",
}
AUTHORITY_INPUTS = {
    "Docs/Stage1_Targets_rev-5.6.json": "02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c",
    "Docs/Stage1_Execution_DAG_rev-5.6.json": "6a58ba59c1a825538619804a47cdf809de5893de58ef939e708339d1b4fd7761",
    "Docs/Stage1_Blueprint_rev-5.6.md": "e2a0f965efcb876706c4d880c429d8d4469f1b2d94871e6f0f673de8f50b4a2c",
    "skills/execute-stage1-rev56/SKILL.md": "26d47a66c6535feabb8bbf1051fd55d76a53fe761f4b3d953f86b97ec86152b8",
}
TOOL_INPUTS = {
    "lean-toolchain": TOOLCHAIN_SHA256,
    "lake-manifest.json": MANIFEST_SHA256,
}
RECIPE_ARGV = [
    "/usr/bin/bwrap", "--ro-bind", "/", "/", "--dev", "/dev",
    "--proc", "/proc", "--tmpfs", "/tmp", "--unshare-net",
    "--die-with-parent", "--clearenv", "--setenv", "HOME", "/tmp",
    "--setenv", "PATH", "/usr/bin:/bin", "--setenv", "LANG", "C.UTF-8",
    "--setenv", "LC_ALL", "C.UTF-8", "--setenv", "TZ", "UTC",
    "--setenv", "LEAN_NUM_THREADS", "1", "/usr/bin/python3", "-I", "-B",
    f"Stage1_Instances/{THEOREM}/check_release.py",
]
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/check_release.py",
    f"Stage1_Instances/{THEOREM}/release-decision.json",
    f"Stage1_Instances/{THEOREM}/release-phase.md",
    f"Stage1_Instances/{THEOREM}/release-receipt.json",
    f"Stage1_Instances/{THEOREM}/release-spec.json",
}
SUMMARY_LINES = (
    "PASS THM-M-0665 current network-isolated trust-zero Lean replay",
    "PASS provisional dependency, frozen denominator, and all 20 negative states reconciled",
    "OPEN H1/M3/R4; zero closed obligations; AUDIT-Z=false; THEOREM-Z=false; theorem_complete=false",
    "BLOCKED dependency acceptance, exact root, hermetic release, independent verification, and master acceptance",
)


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


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(
    argv: list[str], *, cwd: Path = ROOT, env: dict[str, str] | None = None,
    timeout: int = 900, expected_exit: int = 0,
) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        argv, cwd=cwd, env=env, text=True, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, timeout=timeout, check=False,
    )
    assert result.returncode == expected_exit, (
        f"command exited {result.returncode}, expected {expected_exit}: {argv!r}\n"
        f"{result.stdout}"
    )
    return result


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["git", *args], cwd=cwd, timeout=60).stdout.rstrip()


def source_without_comments(source: str) -> str:
    output: list[str] = []
    index = 0
    depth = 0
    in_string = False
    escaped = False
    while index < len(source):
        pair = source[index:index + 2]
        char = source[index]
        if depth:
            if pair == "/-":
                depth += 1
                index += 2
            elif pair == "-/":
                depth -= 1
                index += 2
            else:
                if char == "\n":
                    output.append("\n")
                index += 1
        elif in_string:
            output.append(char)
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
            index += 1
        elif pair == "/-":
            depth = 1
            index += 2
        elif pair == "--":
            newline = source.find("\n", index + 2)
            if newline < 0:
                break
            output.append("\n")
            index = newline + 1
        else:
            output.append(char)
            if char == '"':
                in_string = True
            index += 1
    assert depth == 0 and not in_string
    return "".join(output)


def reported_axioms(output: str, declaration: str) -> set[str]:
    pattern = re.compile(
        re.escape(f"'{declaration}' depends on axioms: [") + r"(.*?)]",
        re.DOTALL,
    )
    matches = pattern.findall(output)
    no_axioms = output.count(f"'{declaration}' does not depend on any axioms")
    assert len(matches) + no_axioms == 1, declaration
    if not matches:
        return set()
    return {part.strip() for part in matches[0].split(",") if part.strip()}


def assert_hygiene(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines()), path


def current_lean_replay() -> set[str]:
    mathlib = LEAN_ROOT / ".lake" / "packages" / "mathlib"
    account_home = Path(pwd.getpwuid(os.getuid()).pw_dir)
    toolchain_bin = account_home / ".elan/toolchains/leanprover--lean4---v4.29.0/bin"
    lean = toolchain_bin / "lean"
    lake = toolchain_bin / "lake"
    assert sha256(lean) == LEAN_SHA256 and sha256(lake) == LAKE_SHA256
    assert sha256(Path("/usr/bin/bwrap")) == BWRAP_SHA256
    assert sha256(Path("/usr/bin/python3")) == PYTHON_SHA256
    fixed_env = {
        "HOME": os.environ["HOME"],
        "PATH": f"{toolchain_bin}:/usr/bin:/bin",
        "ELAN_TOOLCHAIN": LEAN_TOOLCHAIN,
        "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8", "TZ": "UTC",
        "LEAN_NUM_THREADS": "1",
    }
    assert LEAN_COMMIT in run([str(lean), "--version"], env=fixed_env).stdout
    dependency_outputs = [
        LEAN_ROOT / ".lake/packages" / name / ".lake/build/lib/lean"
        for name in (
            "batteries", "Qq", "aesop", "plausible", "LeanSearchClient",
            "proofwidgets", "importGraph", "mathlib",
        )
    ]
    assert all(path.is_dir() for path in dependency_outputs)
    discovered = run(
        [str(lake), "env", "printenv", "LEAN_PATH"], cwd=mathlib,
        env=fixed_env,
    ).stdout.strip().split(":")
    toolchain_entries = [
        entry for entry in discovered
        if entry.endswith("/toolchains/leanprover--lean4---v4.29.0/lib/lean")
    ]
    assert len(toolchain_entries) == 1
    lean_path = ":".join([str(path) for path in dependency_outputs] + toolchain_entries)

    tmp = Path(tempfile.mkdtemp(prefix="stage1-m0665-release-", dir="/tmp"))
    try:
        for name in ("Statement.lean", "Proof.lean", "Validation.lean"):
            shutil.copy2(HERE / name, tmp / name)
        (tmp / "home").mkdir()

        def check(name: str, *, module_path: bool, write_olean: bool) -> str:
            env = dict(fixed_env)
            env["HOME"] = str(tmp / "home")
            env["LEAN_PATH"] = f"{tmp}:{lean_path}" if module_path else lean_path
            args = [str(lake), "env", "lean", "--trust=0", "-t0", "-j1",
                    "--root", str(tmp)]
            if write_olean:
                args.extend(["-o", str(tmp / Path(name).with_suffix(".olean"))])
            args.append(str(tmp / name))
            return run(args, cwd=mathlib, env=env, timeout=600).stdout

        statement_output = check("Statement.lean", module_path=False, write_olean=True)
        proof_output = check("Proof.lean", module_path=True, write_olean=True)
        validation_output = check("Validation.lean", module_path=True, write_olean=False)
    finally:
        shutil.rmtree(tmp)

    observed: set[str] = set()
    for short_name in PROOF_DECLARATIONS:
        declaration = f"Stage1Instances.THM_M_0665.Proof.{short_name}"
        axioms = reported_axioms(proof_output, declaration)
        assert axioms <= EXPECTED_AXIOMS
        observed.update(axioms)
    for short_name in VALIDATION_DECLARATIONS:
        declaration = f"Stage1Instances.THM_M_0665.Validation.{short_name}"
        axioms = reported_axioms(validation_output, declaration)
        assert axioms <= EXPECTED_AXIOMS
        observed.update(axioms)
    assert observed == EXPECTED_AXIOMS
    assert proof_output.count("Declarations are sorry-free!") == len(PROOF_DECLARATIONS)
    assert validation_output.count("Declarations are sorry-free!") == len(VALIDATION_DECLARATIONS)
    combined = "\n".join((statement_output, proof_output, validation_output))
    assert "sorryAx" not in combined and "declaration uses 'sorry'" not in combined
    assert "error:" not in combined
    return observed


def main() -> None:
    decision = load(HERE / "release-decision.json")
    receipt = load(HERE / "release-receipt.json")
    spec = load(HERE / "release-spec.json")
    statement = load(HERE / "statement.json")
    anchor = load(HERE / "anchor-audit.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    proof = load(HERE / "proof-receipt.json")
    blocker = load(HERE / "proof-blocker.json")
    validation = load(HERE / "validation-receipt.json")
    instance = load(HERE / "instance.json")
    local_dag = load(HERE / "task-dag.json")
    targets = load(ROOT / "Docs" / "Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    assert git("merge-base", "--is-ancestor", VALIDATION_BASE_REVISION, BASE_REVISION) == ""
    for name, expected in UPSTREAM_INPUTS.items():
        assert sha256(HERE / name) == expected, f"upstream input drifted: {name}"
    for name, expected in AUTHORITY_INPUTS.items():
        assert sha256(ROOT / name) == expected, f"authority input drifted: {name}"
    for name, expected in TOOL_INPUTS.items():
        assert sha256(LEAN_ROOT / name) == expected, f"tool input drifted: {name}"

    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 709
    assert target["baseline"] == "L0" and target["rework_required"] is True
    assert target["lifecycle_mode"] == "planned" and target["theorem_complete"] is False
    release_item = next(row for row in execution["items"] if row["id"] == ITEM)
    validation_item = next(
        row for row in execution["items"] if row["id"] == "S56-M-0665-VALIDATION"
    )
    assert release_item == {
        "id": ITEM, "theorem_id": THEOREM, "execution_rank": 709,
        "phase": "release", "layer": 6, "state": "[ ]",
        "depends_on": ["S56-M-0665-VALIDATION"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Reconcile evidence and decide the exact theorem-completion verdict.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0, "children": [],
    }
    assert validation_item["state"] == "[_]" and validation_item["attempts"] == 1
    assert local_dag["accepted_states"] == []
    assert next(row for row in local_dag["tasks"] if row["id"] == ITEM)["state"] == "open"

    formal = statement["canonical_formal_target"]
    assert formal["declaration_or_expression"] == "Stage1Instances.THM_M_0665.PilaWilkie"
    assert formal["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert formal["statement_file_sha256"] == UPSTREAM_INPUTS["Statement.lean"]
    assert statement["theorem_proved"] is statement["theorem_complete"] is False
    assert anchor["canonical_declaration"] == formal["declaration_or_expression"]
    assert anchor["repo_local"]["exact_closure_found"] is False
    assert instance["lifecycle"] == "planned"
    assert instance["root_vector"] == {"H": "H1", "M": "M3", "R": "R4"}
    assert instance["audit_complete"] is instance["theorem_complete"] is False

    assert registry["root_obligation_id"] == "M0665-ROOT"
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert registry["frozen_denominators"]["inventory"] == INVENTORY_IDS
    assert registry["frozen_denominators"]["required_machine"] == MACHINE_IDS
    root = next(row for row in registry["obligations"] if row["obligation_id"] == "M0665-ROOT")
    assert root["terminal_proof_body_id"] is None and root["machine_eligibility"] == "required"
    closure = graphs["closure_boundary"]
    assert graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert closure["closed_obligations"] == [] and closure["root_closed"] is False
    assert closure["root_machine_debt"] == "M3"
    assert closure["remaining_root_cut_set"] == REMAINING_CUT
    assert closure["composition_certificates_checked"] == []
    assert closure["audit_complete"] is closure["theorem_complete"] is False

    assert proof["accepted"] is False and proof["proposed_state"] == "[_]"
    assert proof["provisionally_closed_obligation_ids"] == []
    assert proof["partial_progress_toward_obligation_ids"] == PARTIAL_IDS
    assert proof["result"]["root_kernel_closed"] is False
    assert proof["result"]["theorem_complete"] is False
    assert blocker["root_closed"] is blocker["theorem_complete"] is False
    assert validation["item_id"] == "S56-M-0665-VALIDATION"
    assert validation["support_state"] == "provisional_worker_selftest"
    assert validation["accepted"] is validation["release_grade"] is False
    assert validation["verdict"] == "blocked"
    assert validation["result"]["accepted_closed_obligation_ids"] == []
    assert validation["result"]["root_kernel_closed"] is False
    assert validation["result"]["root_machine_debt"] == "M3"
    assert validation["result"]["audit_complete"] is False
    assert validation["result"]["theorem_complete"] is False
    assert validation["remaining_root_cut_set"] == REMAINING_CUT
    assert validation["hermeticity"]["cold_dependency_rebuild"] is False
    assert validation["independent_validation"]["distinct_verifier_identity"] is False

    assert decision["schema_version"] == "stage1-release-decision/1.0"
    assert decision["execution_rank"] == 709
    assert decision["phase"] == decision["intent"] == "release"
    assert decision["depends_on"] == ["S56-M-0665-VALIDATION"]
    assert decision["canonical_target"] == formal["declaration_or_expression"]
    assert decision["canonical_target_expression_sha256"] == EXPRESSION_SHA256
    assert decision["item_id"] == receipt["item_id"] == spec["item_id"] == ITEM
    assert decision["theorem_id"] == receipt["theorem_id"] == spec["theorem_id"] == THEOREM
    assert decision["base_revision"] == receipt["base_revision"] == BASE_REVISION
    assert decision["base_tree"] == receipt["base_tree"] == BASE_TREE
    assert decision["inputs"] == receipt["inputs"] == UPSTREAM_INPUTS
    assert decision["authority_inputs"] == receipt["authority_inputs"] == AUTHORITY_INPUTS
    assert decision["tool_inputs"] == receipt["tool_inputs"]
    assert decision["decision_support"] == receipt["support_state"] == "provisional_worker_selftest"
    assert decision["proposed_state"] == receipt["proposed_state"] == "[_]"
    assert decision["release_grade"] is receipt["release_grade"] is False
    assert receipt["accepted"] is receipt["master_acceptance"] is False
    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["phase"] == receipt["intent"] == "release"
    assert receipt["depends_on"] == decision["depends_on"]
    assert receipt["decision_id"] == decision["decision_id"]
    assert receipt["canonical_target"] == {
        "declaration": formal["declaration_or_expression"],
        "proof_declaration": None,
        "elaborated_expression_sha256": EXPRESSION_SHA256,
        "statement_source_sha256": UPSTREAM_INPUTS["Statement.lean"],
        "registry_denominator_sha256": DENOMINATOR_SHA256,
        "exact_statement_delta": "none",
    }
    assert receipt["proof_body_location"]["root_terminal_body"] is None
    assert receipt["proof_body_location"]["partial_source_sha256"] == UPSTREAM_INPUTS[
        "Proof.lean"
    ]
    dependency = decision["dependency"]
    assert receipt["dependency"] == dependency
    assert dependency["item_id"] == validation["item_id"]
    assert dependency["scheduler_projection"] == validation_item["state"] == "[_]"
    assert dependency["receipt_id"] == validation["receipt_id"]
    assert dependency["receipt_sha256"] == sha256(HERE / "validation-receipt.json")
    assert dependency["receipt_accepted"] is dependency["master_accepted"] is False
    assert dependency["receipt_release_grade"] is False
    assert decision["accepted_receipt_ids"] == []
    assert decision["provisional_receipt_ids_inspected"] == [
        proof["receipt_id"], validation["receipt_id"]
    ]

    reconciliation = decision["evidence_reconciliation"]
    assert reconciliation["accepted_closed_obligation_ids"] == []
    assert reconciliation["authoritative_graph_remaining_root_cut_set"] == REMAINING_CUT
    for key in (
        "validation_dependency_master_accepted", "exact_root_kernel_closed",
        "checked_root_composition", "audit_inventory_and_public_reconciliation_accepted",
        "human_source_h0_accepted", "readability_r0_accepted",
        "accepted_foundation_profile", "complete_transitive_tcb_and_provenance",
        "immutable_clean_release_input", "cold_empty_cache_build",
        "offline_archive_replay", "complete_sbom_and_license_closure",
        "deterministic_release_bundle", "distinct_runner_independent_verification",
        "independently_implemented_minimal_verifier", "second_signed_attestation",
        "protected_adversarial_ci", "master_acceptance",
    ):
        assert reconciliation[key] is False, key
    terminal = decision["decision"]
    assert receipt["decision"] == terminal
    assert terminal["verdict"] == "blocked"
    assert terminal["lifecycle_before"] == terminal["lifecycle_after"] == "planned"
    assert terminal["root_vector_before"] == terminal["root_vector_after"] == {
        "H": "H1", "M": "M3", "R": "R4"
    }
    assert terminal["audit_complete"] is terminal["theorem_complete"] is False
    assert terminal["audit_z"] is terminal["theorem_z"] is False
    assert terminal["release_accepted"] is False and terminal["accepted_receipt_ids"] == []
    assert terminal["first_failed_gate"] == "S56-10.2-DEPENDENCY-ACCEPTANCE"
    assert terminal["first_failed_gate_detail"] == (
        "dependency.S56-M-0665-VALIDATION.master_acceptance"
    )
    assert terminal["first_failed_theorem_gate"] == "M0665-C-PARAM.root_closure"
    assert terminal["remaining_root_cut_set"] == REMAINING_CUT
    assert terminal["retry_condition"]
    assert receipt["known_failures"] == decision["known_failures"]
    assert receipt["status_boundary"] == decision["status_boundary"]
    assert receipt["invalidation_inputs"] == decision["invalidation_inputs"]
    assert decision["status_boundary"].startswith(
        "Self-tested negative release reconciliation only"
    )

    assert spec["schema_version"] == "stage1-validation-spec/1.0"
    assert spec["argv"] == RECIPE_ARGV and spec["cwd"] == "."
    assert spec["timeout_seconds"] == 900 and spec["network_policy"] == "denied"
    assert spec["expected_exit"] == 0 and spec["covered_obligation_ids"] == []
    assert spec["negative_status_only_obligation_ids"] == INVENTORY_IDS
    assert receipt["release_artifacts"]["release-spec.json"] == sha256(HERE / "release-spec.json")
    assert receipt["release_artifacts"]["check_release.py"] == sha256(Path(__file__))
    assert receipt["release_artifacts"]["release-decision.json"] == sha256(
        HERE / "release-decision.json"
    )
    assert receipt["repository_state"]["commit"] == BASE_REVISION
    assert receipt["repository_state"]["tree"] == BASE_TREE
    assert receipt["repository_state"]["preexisting_tracked_target_diff_empty"] is True
    assert receipt["repository_state"]["immutable_clean_release_input"] is False
    assert receipt["repository_state"]["accepted_state_changed"] is False

    all_source = "\n".join(
        source_without_comments((HERE / name).read_text(encoding="utf-8"))
        for name in ("Statement.lean", "Proof.lean", "Validation.lean")
    )
    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by|run_tac)\b|"
        r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
        r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
        r"(?:axiom|constant|opaque|unsafe|extern)\b",
        re.MULTILINE,
    )
    assert prohibited.search(all_source) is None
    assert "theorem pilaWilkie : PilaWilkie" not in all_source

    mathlib = LEAN_ROOT / ".lake" / "packages" / "mathlib"
    assert mathlib.resolve().is_dir()
    assert git("rev-parse", "HEAD", cwd=mathlib) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == MATHLIB_TREE
    assert git("remote", "get-url", "origin", cwd=mathlib) == MATHLIB_REMOTE
    assert git("status", "--porcelain=v1", "--untracked-files=all", cwd=mathlib) == ""
    assert sha256(mathlib / "LICENSE") == MATHLIB_LICENSE_SHA256
    flt_regular = LEAN_ROOT / ".lake" / "packages" / "flt-regular"
    assert flt_regular.is_dir()
    missing_head = subprocess.run(
        ["git", "rev-parse", "--verify", "HEAD^{commit}"],
        cwd=flt_regular, env={"PATH": "/usr/bin:/bin", "LANG": "C.UTF-8"},
        text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        timeout=30, check=False,
    )
    assert missing_head.returncode != 0
    observed = current_lean_replay()
    assert observed == set(receipt["current_replay"]["observed_axioms"])
    assert receipt["current_replay"]["proof_declarations_sorry_free"] == 14
    assert receipt["current_replay"]["differential_declarations_sorry_free"] == 3
    assert receipt["current_replay"]["root_kernel_closed"] is False
    assert receipt["current_replay"]["accepted_obligation_closure"] == []
    assert git("status", "--porcelain=v1", "--untracked-files=all", cwd=mathlib) == ""

    assert set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert packet["item_id"] == ITEM and packet["state"] == "[_]"
    assert packet["base_revision"] == BASE_REVISION
    assert set(packet["changed_paths"]) == set(receipt["changed_paths"]) == CHANGED_PATHS
    assert packet["commands"] == receipt["commands"]
    assert packet["output_summary"] == list(SUMMARY_LINES)
    assert packet["known_failures"] == decision["known_failures"]
    actual = {
        line[3:] if line[:2] == "??" else line[2:].lstrip()
        for line in git(
            "status", "--porcelain=v1", "--untracked-files=all", "--",
            str(HERE), str(ROOT / ".stage1-worker-selftest.json"),
        ).splitlines()
    }
    assert actual == CHANGED_PATHS, (actual, CHANGED_PATHS)
    for relative in CHANGED_PATHS:
        assert_hygiene(ROOT / relative)
    for path in (HERE / "release-decision.json", HERE / "release-receipt.json",
                 HERE / "release-phase.md"):
        public = path.read_text(encoding="utf-8")
        assert "/home/" not in public and ".cron/" not in public
        assert "theorem_complete=true" not in public

    print("\n".join(SUMMARY_LINES))


if __name__ == "__main__":
    main()
