#!/usr/bin/env python3
"""Fail-closed reconciliation check for S56-M-0325-RELEASE."""

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
HERE = ROOT / "Stage1_Instances" / "THM-M-0325"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
ITEM = "S56-M-0325-RELEASE"
THEOREM = "THM-M-0325"
BASE_REVISION = "34729c0dff13ac1d1a2781d9c1ea4bf7c6a35398"
BASE_TREE = "dde7f823b850641fc7dade0380327b6ac013ac07"
DENOMINATOR_SHA256 = "4c41e44f32c7c300ac25319a49fd14dcf197599756525b2dec8dcdce4207703c"
EXPRESSION_SHA256 = "b4daa662b6b3f7cc1578975aeaf9fd097ef586b209bd0d26d4262c59ac59cf82"
LEAN_TOOLCHAIN = "leanprover/lean4:v4.29.0"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
LEAN_SHA256 = "3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf"
LAKE_SHA256 = "a608ff084d7e2af228b92a29d7c2fd083ba0580e46889175ec74a81678c98359"
BWRAP_SHA256 = "0abea81db798ebf6b4742ac0664802d97521547a353c2a0dbdc21d76cbbfd2c0"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_REMOTE = "https://github.com/leanprover-community/mathlib4.git"
MATHLIB_LICENSE_SHA256 = "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1"
FLT_REGULAR_REVISION = "56161b6eb5281fbfe9c38f2bcec0f429ebc11a27"
FLT_REGULAR_TREE = "32c9eace926573a9981787ae97643e520353c893"
FLT_REGULAR_REMOTE = "https://github.com/leanprover-community/flt-regular.git"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
EXPECTED_OLEANS = {
    "Statement.olean": "5da713d6cd67197fa4d54b69ee1ac0c6aebaec8d545748297800cf5f09ccdd7d",
    "ObligationTree.olean": "6588e3bc5a2d045319df89401047b1a133b7d5b0adc47bc8c44e9832931a7d2a",
    "AnchorAudit.olean": "7e864ef4728c00f185c095d830f32be1cfceedec398dfcdb367e9bbd48ced1d0",
    "Proof.olean": "3fb550337b224daed7bc786339a3da72f9dc440df0147b028ac2d144bfd6afc1",
}
CANONICAL_OBLIGATION_IDS = [
    "M0325-ROOT", "M0325-S-DEFINITIONS", "M0325-S-BOUNDARY",
    "M0325-S-FOUNDATION", "M0325-N-FINITE-SPAN", "M0325-N-GRAM",
    "M0325-K-TRANSFORM", "M0325-R-RANDOM", "M0325-B-MEASURABLE",
    "M0325-B-SCALAR", "M0325-L-EXPECTATION", "M0325-T-PACKAGE",
    "M0325-T-ASSEMBLE", "M0325-X-SOURCE", "M0325-X-PROVENANCE",
]
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
EXPECTED_INPUTS = {
    "Docs/Stage1_Targets_rev-5.6.json": "02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c",
    "Docs/Stage1_Execution_DAG_rev-5.6.json": "88ee0472b5725f574eb69ef852e0f0d4ee24cac8f911e6216a4b2d38846da101",
    "Docs/Stage1_Blueprint_rev-5.6.md": "312abb632138e0976fa04f5c24cdfb955e8deed6696cdce01c30faaf238ad62e",
    "skills/execute-stage1-rev56/SKILL.md": "26d47a66c6535feabb8bbf1051fd55d76a53fe761f4b3d953f86b97ec86152b8",
    "Stage1_Instances/THM-M-0325/README.md": "62da5d1b28a30f7b875b30475ad89580a7622eecaeb27c185d906d87633ee563",
    "Stage1_Instances/THM-M-0325/scope-map.md": "915b7959bcaf43034dbcf8f6019694128a66f06ccbfebc219f0a5064b4828249",
    "Stage1_Instances/THM-M-0325/source-statement-crosswalk.md": "18acd851bb81936c81c60896ee6ef27b1cb50503005b2cf05e28485a45ecfb82",
    "Stage1_Instances/THM-M-0325/Statement.lean": "a24ef5cd7e7ee64b388eeb36d2881c66f85630deca58f63440de5dd72098eb1e",
    "Stage1_Instances/THM-M-0325/ObligationTree.lean": "224e289bd647e8154c50d2756d62bf72c8201ad48cde442d85ad7655da60abf8",
    "Stage1_Instances/THM-M-0325/AnchorAudit.lean": "56f2a86f4be164368d65ccd893d7be0776876ef7653970ab41f95401c9d9719e",
    "Stage1_Instances/THM-M-0325/Proof.lean": "3d1c12641a8d7f3cb5331c44079312ba4b80612d62e5ffedba645e9aa83d0a9a",
    "Stage1_Instances/THM-M-0325/instance.json": "fdf244b395ac91974ae68eeb7e64f5c34384d6f29e4d6852f8a101a0888ab73d",
    "Stage1_Instances/THM-M-0325/task-dag.json": "cf27f23c22f870683d1359be50b65b64648ce9d5871892d4f5f0c097467f5816",
    "Stage1_Instances/THM-M-0325/statement.json": "a6bee1f7353bf8963da181fd5ddc0ed73b7a193b9dce6d794795566dabf834e2",
    "Stage1_Instances/THM-M-0325/anchor-audit.json": "fb87d78fbdb668ec985e9a104c48d38ee43ec4ab984a19fa8f79ec3785220d6e",
    "Stage1_Instances/THM-M-0325/obligation-registry.json": "9afd64086d56f8fb871e3f5e48bf9d38a01cba7b3ac8e6dd544a0fcb99a9587b",
    "Stage1_Instances/THM-M-0325/typed-graphs.json": "420e72dedc91e7545b64b158394c271e564de8b07437bcd67d57c22866fa0f8b",
    "Stage1_Instances/THM-M-0325/proof-receipt-slot35.json": "0953d0285eac48bdcd525eb381c3a1e7ea5f9be987ff413d5a3e2c72026d52d8",
    "Stage1_Instances/THM-M-0325/proof-blocker-slot35.json": "803596496eb995ea523cb9428886bb1ff13bbd61d4ddddfaca5ca4ae539002de",
    "Stage1_Instances/THM-M-0325/validation-spec.json": "dae058f59ef4e8c36d4151fd146433b3ce57297f5cbdba0057d7a7c05b38fd35",
    "Stage1_Instances/THM-M-0325/validation-receipt.json": "fca4f0c5d4a2bd6eae83395861d0d3c93158c0c44e9ef27810509c22a71248ac",
    "Stage1_Instances/THM-M-0325/validation-blocker.json": "76aa43e93df5e1e0493c72a93ac0a5dbca6c2e64565cfc0300e6619ad6a97c61",
    "Stage1_Instances/THM-M-0325/validation-phase.md": "e8198ee51a29370abe80bcacf353e3c076888ea99d521000679099fc895cba75",
}
RELEASE_INPUT_BINDINGS = {
    f"Stage1_Instances/{THEOREM}/release-spec.json": "9ae1b6d001fbc751aff19ced16facea9e41a6e6f9feffb0fe025412ac01b1841",
    f"Stage1_Instances/{THEOREM}/release-decision.json": "dc25700adc06fdb006937729cf45ec1c5f26fadf87c118e2004fcb6bb7cc1750",
    f"Stage1_Instances/{THEOREM}/release-validation.md": "30e60c8dc8f1fd8147f3c894d33b7bb0eef666fa8dbbec87bf7c9cccc6c484f2",
    **{
        relative: digest
        for relative, digest in EXPECTED_INPUTS.items()
        if relative.startswith(f"Stage1_Instances/{THEOREM}/")
        and relative not in {
            f"Stage1_Instances/{THEOREM}/README.md",
            f"Stage1_Instances/{THEOREM}/scope-map.md",
            f"Stage1_Instances/{THEOREM}/validation-phase.md",
        }
    },
}
EVIDENCE_RECONCILIATION = {
    "target_membership_and_order": "pass",
    "statement_elaboration_and_transport": "provisional_pass",
    "conditional_composition_elaboration": "provisional_pass_no_root_credit",
    "partial_local_body_elaboration": "provisional_pass_no_frozen_obligation_credit",
    "exact_root_proof_body_present": False,
    "exact_root_kernel_closed": False,
    "authoritative_graph_reconciled": False,
    "pinpoint_h0_primary_source_review": False,
    "independent_r0_readable_review": False,
    "audit_z_accepted": False,
    "accepted_foundation_provenance_trust_tcb_closure": False,
    "immutable_clean_release_input": False,
    "hermetic_cold_empty_cache_offline_replay": False,
    "sbom_license_supply_chain_archive": False,
    "two_distinct_signed_runner_attestations": False,
    "independently_implemented_minimal_verifier": False,
    "protected_ci_and_mutation_gates": False,
    "deterministic_content_addressed_release_bundle": False,
    "master_acceptance": False,
    "observed_axioms_for_replayed_partial_declarations_subset_of": [
        "propext", "Classical.choice", "Quot.sound",
    ],
    "placeholder_and_unsafe_scan": "pass for the four target Lean modules",
    "project_lake_preflight": (
        "pass for pinned Lean selection and clean pinned flt-regular source; "
        "no update, build, fetch, clone, or cache mutation was performed"
    ),
    "narrow_warm_cache_replay": (
        "pass with fresh temporary oleans and network denied; explicitly nonrelease evidence"
    ),
}
REMAINING_RELEASE_CUT_SET = [
    "master acceptance of S56-M-0325-VALIDATION and its transitive prerequisites",
    "placeholder-free construction of M0325-K-TRANSFORM and every remaining child needed for M0325-T-PACKAGE and the exact root",
    "append-only reconciliation of instance, typed graphs, receipts, metrics, and public surfaces",
    "accepted pinpoint H0 primary-source theorem, assumptions, normalization, errata, and source-to-node crosswalk",
    "accepted R0 node-specific reconstruction with independent reader review",
    "accepted root foundation, axiom, declaration-dependency, provenance, trust, and TCB closure",
    "immutable clean source and dependency snapshot with empty-cache network-denied cold build and offline restoration",
    "complete SBOM, licenses, and supply-chain archive",
    "two signed attestations from independently provisioned clean runners with no shared writable cache",
    "independently implemented minimal release verifier",
    "protected CI plus required mutation, adversarial, differential, and metamorphic gate evidence",
    "deterministic content-addressed release bundle and master acceptance",
]
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/check_release.py",
    f"Stage1_Instances/{THEOREM}/release-decision.json",
    f"Stage1_Instances/{THEOREM}/release-receipt.json",
    f"Stage1_Instances/{THEOREM}/release-spec.json",
    f"Stage1_Instances/{THEOREM}/release-validation.md",
}
KNOWN_FAILURES = [
    "S56-M-0325-VALIDATION is provisional, release_grade=false, unaccepted by the master, and bound to historical base dafb8b51 rather than the current release base.",
    "No exact root proof body exists; target_of_proofPackage is only a conditional identity, and M0325-T-PACKAGE remains open with first substantive blocker M0325-K-TRANSFORM.",
    "The authoritative planned instance remains H2/M4/R4 while provisional graph and validation evidence classify the root H2/M3/R4; no accepted reconciliation permits promotion.",
    "Pinpoint primary-source fidelity, source-to-node coverage, an independently reviewed R0 reconstruction, and AUDIT-Z are absent.",
    "The accepted foundation, complete transitive declaration provenance, trust/TCB profile, dependency-object inventory, SBOM, licenses, and supply-chain archive are incomplete.",
    "The automation-provided .lake link is untracked and reuses shared compiled artifacts; the successful project preflight and fresh temporary warm-cache replay are nonrelease evidence only.",
    "No immutable clean empty-cache cold build, offline archive restoration, deterministic release bundle, protected release CI/mutation evidence, two distinct signed runners, or independently implemented minimal verifier exists.",
]
PASS_OUTPUT = (
    "PASS S56-M-0325-RELEASE reconciliation\n"
    "verdict=blocked lifecycle=planned authoritative_root_vector=H2/M4/R4\n"
    "audit_complete=false theorem_complete=false accepted_receipts=0\n"
    "first_failed_gate=S56-10.2-DEPENDENCY-ACCEPTANCE\n"
    "root_kernel_closed=false remaining_root_cut_set=M0325-T-PACKAGE\n"
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


def canonical_json_id(document: dict, omitted_field: str) -> str:
    body = dict(document)
    body.pop(omitted_field, None)
    payload = json.dumps(body, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return "sha256:" + hashlib.sha256(payload).hexdigest()


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
    assert output.count(no_axioms) + len(matches) == 1, declaration
    if not matches:
        return set()
    return {part.strip() for part in matches[0].split(",") if part.strip()}


def assert_text_hygiene(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data, path
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines()), path


def replay_lean() -> dict[str, str]:
    toolchain_root = Path.home() / ".elan" / "toolchains" / "leanprover--lean4---v4.29.0"
    lean = toolchain_root / "bin" / "lean"
    lake = toolchain_root / "bin" / "lake"
    bwrap = Path(shutil.which("bwrap") or "")
    assert lean.is_file() and lake.is_file() and bwrap.is_file()
    assert sha256(lean) == LEAN_SHA256
    assert sha256(lake) == LAKE_SHA256
    assert sha256(bwrap) == BWRAP_SHA256

    fixed_env = os.environ.copy()
    fixed_env.update({
        "ELAN_TOOLCHAIN": LEAN_TOOLCHAIN,
        "LANG": "C.UTF-8",
        "LC_ALL": "C.UTF-8",
        "TZ": "UTC",
        "LEAN_NUM_THREADS": "1",
    })
    assert LEAN_COMMIT in run([str(lean), "--version"], env=fixed_env)
    compiled_dirs = sorted(
        path.resolve()
        for path in (LEAN_ROOT / ".lake" / "packages").glob("*/.lake/build/lib/lean")
        if path.is_dir()
    )
    assert compiled_dirs and any("/mathlib/" in str(path) for path in compiled_dirs)
    lean_path = ":".join(str(path) for path in compiled_dirs)

    tmp = Path(tempfile.mkdtemp(prefix="stage1-m0325-release-", dir="/tmp"))
    try:
        for name in ("Statement.lean", "ObligationTree.lean", "AnchorAudit.lean", "Proof.lean"):
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
        actual_oleans = {
            name: sha256(tmp / name)
            for name in EXPECTED_OLEANS
        }
        assert actual_oleans == EXPECTED_OLEANS, actual_oleans
    finally:
        shutil.rmtree(tmp)

    combined = "\n".join((statement_output, obligation_output, anchor_output, proof_output))
    assert "error:" not in combined and "declaration uses 'sorry'" not in combined
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
    return actual_oleans


def main() -> None:
    if sys.flags.optimize != 0:
        raise RuntimeError("release checker requires Python assertions")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    for relative, expected in EXPECTED_INPUTS.items():
        assert sha256(ROOT / relative) == expected, f"reconciled input drifted: {relative}"

    targets = load(ROOT / "Docs" / "Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")
    instance = load(HERE / "instance.json")
    local_dag = load(HERE / "task-dag.json")
    statement = load(HERE / "statement.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    proof_receipt = load(HERE / "proof-receipt-slot35.json")
    validation = load(HERE / "validation-receipt.json")
    decision = load(HERE / "release-decision.json")
    receipt = load(HERE / "release-receipt.json")
    spec = load(HERE / "release-spec.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")

    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 214
    assert target["baseline"] == "L0" and target["rework_required"] is True
    assert target["lifecycle_mode"] == "planned" and target["theorem_complete"] is False

    release_item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert release_item == {
        "id": ITEM, "theorem_id": THEOREM, "execution_rank": 214,
        "phase": "release", "layer": 6, "state": "[ ]",
        "depends_on": ["S56-M-0325-VALIDATION"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Reconcile evidence and decide the exact theorem-completion verdict.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0, "children": [],
    }
    validation_item = next(
        row for row in execution["items"] if row["id"] == "S56-M-0325-VALIDATION"
    )
    proof_item = next(row for row in execution["items"] if row["id"] == "S56-M-0325-PROOF")
    assert validation_item["state"] == proof_item["state"] == "[_]"
    assert validation_item["attempts"] == proof_item["attempts"] == 1
    local_release = next(row for row in local_dag["tasks"] if row["id"] == ITEM)
    assert local_release["state"] == "open"
    assert local_release["depends_on"] == ["S56-M-0325-VALIDATION"]

    authoritative_vector = {"H": "H2", "M": "M4", "R": "R4"}
    provisional_vector = {"H": "H2", "M": "M3", "R": "R4"}
    assert instance["lifecycle"] == "planned"
    assert instance["root_vector"] == authoritative_vector
    assert instance["accepted_proof_state"] == []
    assert instance["audit_complete"] is instance["theorem_complete"] is False
    assert statement["canonical_formal_target"]["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert registry["denominator_sha256"] == graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert registry["frozen_denominators"]["inventory"] == CANONICAL_OBLIGATION_IDS
    assert [row["obligation_id"] for row in registry["obligations"]] == CANONICAL_OBLIGATION_IDS
    assert registry["status_observed_after_freeze"]["root_machine_debt"] == "M3"
    closure = graphs["closure_boundary"]
    assert closure["root_closed"] is closure["audit_complete"] is False
    assert closure["theorem_complete"] is False
    assert closure["remaining_root_cut_set"] == ["M0325-T-PACKAGE"]

    assert proof_receipt["accepted"] is False
    assert proof_receipt["result"]["root_kernel_closed"] is False
    assert proof_receipt["supported_obligation_ids"] == []
    assert validation["receipt_id"] == canonical_json_id(validation, "receipt_id")
    assert validation["support_state"] == "provisional_worker_selftest"
    assert validation["accepted"] is validation["release_grade"] is False
    assert validation["content_addressed"] is False
    assert validation["base_revision"] != BASE_REVISION
    assert validation["result"]["root_kernel_closed"] is False
    assert validation["result"]["audit_complete"] is validation["result"]["theorem_complete"] is False
    assert validation["accepted_receipt_ids"] == []
    assert validation["first_failed_gate"] == "dependency.S56-M-0325-PROOF.not_complete"
    assert validation["remaining_root_cut_set"] == ["M0325-T-PACKAGE"]

    lean_source = "\n".join(
        source_without_comments((HERE / name).read_text(encoding="utf-8"))
        for name in ("Statement.lean", "ObligationTree.lean", "AnchorAudit.lean", "Proof.lean")
    )
    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|implemented_by|native_decide)\b|"
        r"^[ \t]*(?:axiom|constant|opaque|unsafe|extern)\b",
        re.MULTILINE,
    )
    assert prohibited.search(lean_source) is None
    assert "theorem proof : GrothendieckInequalityTarget" not in lean_source
    assert "theorem proof : GrothendieckProofPackage" not in lean_source
    assert "def GrothendieckProofPackage : Prop :=\n  GrothendieckInequalityTarget" in lean_source
    assert "(package : GrothendieckProofPackage" in lean_source
    assert "exact package" in lean_source

    mathlib = (LEAN_ROOT / ".lake" / "packages" / "mathlib").resolve()
    assert git("rev-parse", "HEAD", cwd=mathlib) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == MATHLIB_TREE
    assert git("status", "--porcelain=v1", "--untracked-files=all", cwd=mathlib) == ""
    assert git("remote", "get-url", "origin", cwd=mathlib) == MATHLIB_REMOTE
    assert sha256(mathlib / "LICENSE") == MATHLIB_LICENSE_SHA256
    lake_link = LEAN_ROOT / ".lake"
    assert lake_link.is_symlink()
    flt_regular = lake_link.resolve() / "packages" / "flt-regular"
    assert git("rev-parse", "HEAD", cwd=flt_regular) == FLT_REGULAR_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=flt_regular) == FLT_REGULAR_TREE
    assert git("status", "--porcelain=v1", "--untracked-files=all", cwd=flt_regular) == ""
    assert git("remote", "get-url", "origin", cwd=flt_regular) == FLT_REGULAR_REMOTE

    actual_oleans = replay_lean()

    assert spec["schema_version"] == "stage1-validation-recipe/1.0"
    assert spec["item_id"] == ITEM and spec["theorem_id"] == THEOREM
    assert spec["base_revision"] == BASE_REVISION and spec["base_tree"] == BASE_TREE
    assert spec["cwd"] == "."
    assert spec["argv"] == ["python3", "-I", "-B", f"Stage1_Instances/{THEOREM}/check_release.py"]
    assert spec["network_policy"] == "denied" and spec["expected_exit"] == 0
    assert spec["covered_obligation_ids"] == CANONICAL_OBLIGATION_IDS
    assert spec["expected_olean_sha256"] == EXPECTED_OLEANS
    assert spec["coverage_semantics"].startswith("All 15 obligation IDs receive fail-closed")

    assert decision["decision_id"] == canonical_json_id(decision, "decision_id")
    assert decision["item_id"] == ITEM and decision["theorem_id"] == THEOREM
    assert decision["base_revision"] == BASE_REVISION and decision["base_tree"] == BASE_TREE
    assert decision["decision_support"] == "provisional_worker_selftest"
    assert decision["proposed_state"] == "[_]" and decision["verdict"] == "blocked"
    assert decision["release_spec_sha256"] == sha256(HERE / "release-spec.json")
    dependency = decision["dependency"]
    assert dependency["item_id"] == validation["item_id"] == "S56-M-0325-VALIDATION"
    assert dependency["receipt_id"] == validation["receipt_id"]
    assert dependency["receipt_sha256"] == sha256(HERE / "validation-receipt.json")
    assert dependency["receipt_base_revision"] == validation["base_revision"]
    assert dependency["support_state"] == validation["support_state"]
    assert dependency["accepted"] is dependency["release_grade"] is False
    assert dependency["master_accepted"] is False
    assert dependency["fresh_for_release_base"] is False
    state = decision["authoritative_state"]
    assert state["lifecycle_before"] == state["lifecycle_after"] == "planned"
    assert state["root_vector_before"] == state["root_vector_after"] == authoritative_vector
    assert state["provisional_architecture_vector"] == provisional_vector
    terminal = decision["terminal_decisions"]
    assert terminal["audit_complete"] is terminal["theorem_complete"] is False
    assert terminal["audit_z"] == terminal["theorem_z"] == "blocked"
    assert terminal["release_accepted"] is False
    assert decision["accepted_receipt_ids"] == []
    assert decision["first_failed_gate"]["gate_id"] == "S56-10.2-DEPENDENCY-ACCEPTANCE"
    assert decision["next_failed_theorem_gate"]["obligation_id"] == "M0325-K-TRANSFORM"
    assert decision["authoritative_remaining_root_cut_set"] == ["M0325-T-PACKAGE"]
    assert decision["evidence_reconciliation"] == EVIDENCE_RECONCILIATION
    assert decision["remaining_release_cut_set"] == REMAINING_RELEASE_CUT_SET
    assert decision["known_failures"] == KNOWN_FAILURES

    assert receipt["receipt_id"] == canonical_json_id(receipt, "receipt_id")
    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]"
    assert receipt["accepted"] is receipt["release_grade"] is False
    assert receipt["content_addressed_release_evidence"] is False
    assert receipt["verdict"] == "blocked" and receipt["decision_id"] == decision["decision_id"]
    assert receipt["checker_binding"]["path"] == f"Stage1_Instances/{THEOREM}/check_release.py"
    assert receipt["checker_binding"]["sha256"] == sha256(Path(__file__).resolve())
    assert receipt["input_bindings"] == RELEASE_INPUT_BINDINGS
    for relative, expected in RELEASE_INPUT_BINDINGS.items():
        assert sha256(ROOT / relative) == expected, f"release binding drifted: {relative}"
    for key in (
        "recipe_id", "cwd", "argv", "env_allowlist", "timeout_seconds",
        "network_policy", "network_enforcement", "expected_exit",
        "expected_outputs", "covered_obligation_ids", "covered_declarations",
        "expected_olean_sha256",
    ):
        assert receipt["recipe"][key] == spec[key], key
    assert set(receipt["recipe"]) == set(spec) - {
        "schema_version", "item_id", "theorem_id", "intent", "base_revision",
        "base_tree", "scope_boundary",
    } | {"stdout_semantic_sha256"}
    assert receipt["recipe"]["stdout_semantic_sha256"] == hashlib.sha256(
        PASS_OUTPUT.encode("utf-8")
    ).hexdigest()
    result = receipt["result"]
    assert result["exit_code"] == 0 and result["verdict"] == "blocked"
    assert result["fresh_olean_sha256"] == actual_oleans == EXPECTED_OLEANS
    assert result["root_kernel_closed"] is result["audit_complete"] is False
    assert result["theorem_complete"] is False
    assert result["authoritative_root_vector"] == authoritative_vector
    assert result["provisional_architecture_root_vector"] == provisional_vector
    assert result["exact_root_body_present"] is False
    assert result["accepted_receipt_ids"] == []
    assert result["hermetic_release_gate"] == "fail_closed"
    assert result["independent_verification_gate"] == "fail_closed"
    worker_evidence = receipt["worker_evidence_packet"]
    assert worker_evidence["task_ids"] == [ITEM]
    assert worker_evidence["canonical_obligation_ids"] == CANONICAL_OBLIGATION_IDS
    assert worker_evidence["exact_statement_delta"] == "none"
    assert worker_evidence["proof_body_delta"] == "none"
    assert worker_evidence["typed_graph_delta"] == "none"
    assert worker_evidence["composition_certificates_inspected"] == [{
        "declaration": "Stage1Instances.THM_M_0325.target_of_proofPackage",
        "classification": "conditional identity; no root or proof-package closure credit",
    }]
    symlink_evidence = receipt["nonrelease_input_set"]
    assert symlink_evidence["lake_symlink_payload_sha256"] == hashlib.sha256(
        os.readlink(LEAN_ROOT / ".lake").encode("utf-8")
    ).hexdigest()
    untracked_hashes = receipt["untracked_artifact_evidence"]["artifact_sha256"]
    expected_untracked = CHANGED_PATHS - {f"Stage1_Instances/{THEOREM}/release-receipt.json"}
    assert set(untracked_hashes) == expected_untracked
    for relative, expected in untracked_hashes.items():
        assert sha256(ROOT / relative) == expected, relative
    assert receipt["output_evidence"]["stdout_semantic_sha256"] == hashlib.sha256(
        PASS_OUTPUT.encode("utf-8")
    ).hexdigest()
    assert receipt["known_failures"] == KNOWN_FAILURES
    assert receipt["remaining_root_cut_set"] == ["M0325-T-PACKAGE"]
    assert set(receipt["changed_paths"]) == CHANGED_PATHS

    assert set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert packet["item_id"] == ITEM and packet["state"] == "[_]"
    assert packet["base_revision"] == BASE_REVISION
    assert set(packet["changed_paths"]) == CHANGED_PATHS
    assert packet["known_failures"] == KNOWN_FAILURES
    actual_changes = {
        line[3:] for line in git(
            "status", "--short", "--untracked-files=all", "--",
            f"Stage1_Instances/{THEOREM}", ".stage1-worker-selftest.json",
        ).splitlines()
    }
    assert actual_changes == CHANGED_PATHS, (actual_changes, CHANGED_PATHS)

    for relative in CHANGED_PATHS:
        assert_text_hygiene(ROOT / relative)

    print(PASS_OUTPUT, end="")


if __name__ == "__main__":
    main()
