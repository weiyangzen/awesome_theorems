#!/usr/bin/env python3
"""Fail-closed release reconciliation for S56-M-1244-RELEASE."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile


if not __debug__:
    raise SystemExit("check_release.py must run without Python optimization")


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-1244"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM = "S56-M-1244-RELEASE"
THEOREM = "THM-M-1244"
BASE_REVISION = "443b8bbc23bf35a1e7a4bb7b3183073f76bbee2b"
BASE_TREE = "c5771c47c12b80aba613e6d844570f83b39ded6d"
EXPRESSION_SHA256 = "eeff335a47ceaf9d469f25e1570640f17008c1f38d8173499a5429e7ab6397b3"
DENOMINATOR_SHA256 = "edecb957b6903682647ae02dbfff3d6bdd693e6ddf2decd18721fdcae702c297"
VALIDATION_RECEIPT_SHA256 = "da6d468dfbe7ba19ffd43b751c03bdadc7cba5638c424dec87fdeb7b69c52d03"
EXPECTED_INPUTS = {
    "intake.json": "85313807e57ccf8c46d2c5dd1b68c606d8af1cd507e27b38b4efbb612fbbdf24",
    "statement.json": "40c235b0fcc33b49169fc18eb8992c0e4aa7c684709f74711dab99f16b0d0e84",
    "anchor_audit.json": "e5773083e9187011d8fe2e8e928ab6e34dea15d582d669774241c076876e1d2b",
    "obligation-registry.json": "bbf8a6a8990b8d468da92cbcd048f66ca66185747adc8932e09f2931d477911f",
    "typed-graphs.json": "7bc58e69698479b0bb80f6af24f38b056f69376a725dea90e6642fe21a5d866f",
    "proof-receipt.json": "42b078de85cbf52d01e7c6b8a75a1858439f3433c982018ca60820351ee4e248",
    "validation-receipt.json": VALIDATION_RECEIPT_SHA256,
    "source_statement_crosswalk.md": "c26cd3fec9291038534dd9c88656525ab1d0283773b9446e4b65fecff2bfe53f",
    "anchor_audit.md": "5e39afaa30c3288f749b32d0e008bd2d4c895ce7c4a19932cbbfb71e97548d3b",
}
AUTHORITY_INPUTS = {
    "Docs/Stage1_Targets_rev-5.6.json": "02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c",
    "Docs/Stage1_Execution_DAG_rev-5.6.json": "0bb2f433832fe71156aa46c0828102ec3fb61a00dec81fae129c2826a59f63ca",
    "Docs/Stage1_Blueprint_rev-5.6.md": "c09f9f713bdbc820559e41e1e1840423d60cc2af666aeaf5f3c88587de77f161",
    "skills/execute-stage1-rev56/SKILL.md": "26d47a66c6535feabb8bbf1051fd55d76a53fe761f4b3d953f86b97ec86152b8",
    "Formalizations/Lean/lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "Formalizations/Lean/lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
ALL_OBLIGATIONS = [
    "M1244-ROOT", "M1244-S-DEFS", "M1244-S-DOMAIN", "M1244-S-BOUNDARY",
    "M1244-S-FOUNDATION", "M1244-N-MEASURE", "M1244-N-ENTROPY",
    "M1244-N-REGULARITY", "M1244-B-ZEROMASS", "M1244-C-COORD",
    "M1244-L-UPSTREAM", "M1244-L-POINTWISE", "M1244-L-INTEGRAL",
    "M1244-T-PACKAGES", "M1244-T-ASSEMBLE", "M1244-X-SOURCE",
    "M1244-X-PROVENANCE", "M1244-X-TRUST",
]
ROOT_CUT = ["M1244-L-UPSTREAM", "M1244-L-INTEGRAL"]
SUMMARY_LINES = [
    "PASS THM-M-1244 release inputs: authority, receipts, registry, graph, and hashes agree",
    "PASS fresh canonical statement elaboration with pinned Lean 4.29.0 and existing pinned mathlib artifacts",
    "PASS provisional evidence boundary: exact frozen root replay observed, accepted obligations and receipts remain empty",
    "BLOCKED dependency.S56-M-1244-VALIDATION.master_acceptance: validation is provisional and non-release-grade",
    "BLOCKED AUDIT-Z: source fidelity, H0/R0, graph, provenance, trust, and public reconciliation remain open",
    "BLOCKED THEOREM-Z: accepted M0, cold/offline, SBOM, independent-verifier, bundle, and master gates remain open",
    "verdict=blocked; lifecycle=planned; root=H1/M4/R3; audit_complete=false; theorem_complete=false",
]


def fail(message: str) -> None:
    raise SystemExit(f"release-decision: FAIL: {message}")


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def reject_duplicate_keys(pairs: list[tuple[str, object]]) -> dict:
    result: dict[str, object] = {}
    for key, value in pairs:
        require(key not in result, f"duplicate JSON key: {key}")
        result[key] = value
    return result


def load(path: Path) -> dict:
    value = json.loads(
        path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicate_keys
    )
    require(isinstance(value, dict), f"JSON object required: {path}")
    return value


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(argv: list[str], *, cwd: Path = ROOT, env: dict[str, str] | None = None) -> str:
    result = subprocess.run(
        argv,
        cwd=cwd,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=240,
        check=False,
    )
    require(result.returncode == 0, f"command failed ({result.returncode}): {argv!r}\n{result.stdout}")
    return result.stdout


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["git", *args], cwd=cwd).strip()


def explicit_lean_path() -> str:
    paths = []
    for name in (
        "batteries", "Qq", "aesop", "proofwidgets", "importGraph",
        "LeanSearchClient", "plausible", "Cli",
    ):
        path = LEAN_ROOT / ".lake" / "packages" / name / ".lake" / "build" / "lib" / "lean"
        if path.is_dir():
            paths.append(str(path.resolve()))
    mathlib_build = MATHLIB / ".lake" / "build" / "lib" / "lean"
    require(mathlib_build.is_dir(), "pinned mathlib compiled artifacts are unavailable")
    paths.append(str(mathlib_build.resolve()))
    return os.pathsep.join(paths)


def replay_statement() -> None:
    require(MATHLIB.is_dir(), "pinned mathlib package is unavailable")
    require(git("rev-parse", "HEAD", cwd=MATHLIB) == "8a178386ffc0f5fef0b77738bb5449d50efeea95",
            "mathlib revision drifted")
    require(git("rev-parse", "HEAD^{tree}", cwd=MATHLIB) == "bdc39a3123201dae413a9d9be56ec242c19e5c2b",
            "mathlib tree drifted")
    require(git("status", "--porcelain=v1", "--untracked-files=all", cwd=MATHLIB) == "",
            "mathlib package is dirty")

    env = os.environ.copy()
    env.update({
        "LANG": "C.UTF-8",
        "LC_ALL": "C.UTF-8",
        "TZ": "UTC",
        "LEAN_NUM_THREADS": "1",
        "LEAN_PATH": explicit_lean_path(),
    })
    lean = Path(run(["lake", "env", "which", "lean"], cwd=MATHLIB, env=env).strip())
    require(lean.is_file(), "Lean executable is unavailable")
    require(digest(lean) == "3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf",
            "Lean executable digest drifted")
    version = run([str(lean), "--version"], cwd=MATHLIB, env=env)
    require("4.29.0" in version and "98dc76e3c0a9b856c9b98726b713fb04fab16740" in version,
            "Lean version drifted")
    with tempfile.TemporaryDirectory(prefix="thm-m-1244-release-", dir="/tmp") as tmp_name:
        source = Path(tmp_name) / "Statement.lean"
        source.write_bytes((HERE / "Statement.lean").read_bytes())
        output = run(
            ["lake", "env", "lean", "--trust=0", "-t0", str(source)],
            cwd=MATHLIB,
            env=env,
        )
    require("error:" not in output, "canonical statement elaboration reported an error")
    require("GaussianLogSobolevTarget" in output, "canonical declaration was not elaborated")


def main() -> None:
    require(sys.flags.optimize == 0, "optimized Python disables fail-closed assertions")
    decision = load(HERE / "release-decision.json")
    spec = load(HERE / "release-spec.json")
    receipt = load(HERE / "release-receipt.json")
    targets = load(ROOT / "Docs" / "Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")
    intake = load(HERE / "intake.json")
    statement = load(HERE / "statement.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    proof = load(HERE / "proof-receipt.json")
    validation = load(HERE / "validation-receipt.json")

    require(git("rev-parse", "HEAD") == BASE_REVISION, "base revision drifted")
    require(git("rev-parse", "HEAD^{tree}") == BASE_TREE, "base tree drifted")
    for relative, expected in EXPECTED_INPUTS.items():
        require(digest(HERE / relative) == expected, f"reconciled input drifted: {relative}")
    require(decision["reconciled_inputs"] == EXPECTED_INPUTS, "decision input map drifted")
    for relative, expected in AUTHORITY_INPUTS.items():
        require(digest(ROOT / relative) == expected, f"authority input drifted: {relative}")
    require(decision["authority_inputs"] == AUTHORITY_INPUTS, "decision authority map drifted")

    target = next((row for row in targets["targets"] if row["theorem_id"] == THEOREM), None)
    require(target is not None, "target absent from manifest")
    require(target["execution_rank"] == 425, "execution rank drifted")
    require(target["baseline"] == "L0" and target["rework_required"] is True,
            "uniform baseline drifted")
    require(target["legacy_artifacts_accepted"] is False, "legacy evidence became accepted")
    require(target["lifecycle_mode"] == "planned" and target["theorem_complete"] is False,
            "manifest status drifted")

    release_item = next((row for row in execution["items"] if row["id"] == ITEM), None)
    require(release_item == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 425,
        "phase": "release",
        "layer": 6,
        "state": "[ ]",
        "depends_on": ["S56-M-1244-VALIDATION"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Reconcile evidence and decide the exact theorem-completion verdict.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }, "release execution item drifted")
    predecessor = next(
        (row for row in execution["items"] if row["id"] == "S56-M-1244-VALIDATION"), None
    )
    require(predecessor is not None and predecessor["state"] == "[_]",
            "validation dependency is not provisional [_]")
    require(predecessor["attempts"] == 1, "validation attempt count drifted")

    accepted_vector = {"human": "H1", "machine": "M4", "readability": "R3"}
    require(intake["lifecycle_mode"] == "planned", "instance lifecycle drifted")
    require(intake["root_vector"] == accepted_vector, "accepted root vector drifted")
    require(intake["theorem_complete"] is False, "instance claims theorem completion")
    formal = statement["canonical_formal_target"]
    require(formal["elaborated_expression_sha256"] == EXPRESSION_SHA256,
            "canonical expression drifted")
    require(registry["root_obligation_id"] == "M1244-ROOT", "root obligation drifted")
    require(registry["denominator_sha256"] == DENOMINATOR_SHA256,
            "obligation denominator drifted")
    require([row["obligation_id"] for row in registry["obligations"]] == ALL_OBLIGATIONS,
            "obligation inventory drifted")
    require(graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256,
            "graph denominator drifted")
    boundary = graphs["closure_boundary"]
    require(boundary["root_closed"] is boundary["audit_complete"] is
            boundary["theorem_complete"] is False, "typed graph claims terminal completion")
    require(boundary["remaining_root_cut_set"] == ROOT_CUT, "authoritative root cut drifted")

    require(proof["accepted"] is False and proof["proposed_state"] == "[_]",
            "proof receipt became accepted")
    require(proof["accepted_closed_obligation_ids"] == [], "proof grants accepted closure")
    require(proof["result"]["root_kernel_closed"] is True and
            proof["result"]["accepted_root_closed"] is False,
            "proof provisional boundary drifted")
    require(validation["receipt_id"] == "S56-M-1244-VALIDATION-local-20260715T003707Z",
            "wrong validation receipt")
    require(digest(HERE / "validation-receipt.json") == VALIDATION_RECEIPT_SHA256,
            "validation receipt bytes drifted")
    require(validation["accepted"] is validation["release_grade"] is
            validation["content_addressed"] is False,
            "validation became accepted or release-grade")
    require(validation["accepted_receipt_ids"] == validation["accepted_closed_obligation_ids"] == [],
            "validation grants accepted state")
    require(validation["result"]["exact_root_kernel_replay"] == "provisional_pass",
            "validation lost exact-root evidence")
    require(validation["result"]["proof_master_acceptance"] == "fail_closed" and
            validation["result"]["hermetic_cold_offline_replay"] == "fail_closed" and
            validation["result"]["independent_distinct_runner"] == "fail_closed",
            "validation release boundaries drifted")
    require(validation["result"]["audit_complete"] is
            validation["result"]["theorem_complete"] is False,
            "validation claims terminal completion")

    require(decision["schema_version"] == "stage1-release-decision/1.0",
            "decision schema drifted")
    require(decision["item_id"] == ITEM and decision["theorem_id"] == THEOREM,
            "decision identity drifted")
    require(decision["phase"] == decision["intent"] == "release", "decision intent drifted")
    require(decision["verdict"] == "blocked" and decision["release_grade"] is
            decision["release_accepted"] is False, "decision claims release")
    require(decision["lifecycle_before"] == decision["lifecycle_after"] == "planned",
            "blocked decision advanced lifecycle")
    require(decision["accepted_receipt_ids"] == [], "worker accepted a receipt")
    require(decision["root_vector"]["accepted_before"] ==
            decision["root_vector"]["accepted_after"] == accepted_vector,
            "blocked decision changed the accepted vector")
    require(decision["terminal_decisions"] == {
        "audit_complete": False,
        "theorem_complete": False,
        "audit_z": "blocked",
        "theorem_z": "blocked",
    }, "terminal decisions do not fail closed")
    require(decision["first_failed_gate"]["gate_id"] ==
            "dependency.S56-M-1244-VALIDATION.master_acceptance",
            "first failed gate drifted")
    require(decision["first_failed_release_gate"]["gate_id"] ==
            "S56-10.6-HERMETIC-COLD-BUILD", "first release gate drifted")
    require(decision["authoritative_remaining_root_cut_set"] == ROOT_CUT,
            "decision root cut drifted")
    require(decision["dependency"] == {
        "item_id": "S56-M-1244-VALIDATION",
        "scheduler_projection": "[_]",
        "receipt_id": "S56-M-1244-VALIDATION-local-20260715T003707Z",
        "receipt_sha256": VALIDATION_RECEIPT_SHA256,
        "support_state": "provisional_worker_selftest",
        "accepted": False,
        "release_grade": False,
        "content_addressed": False,
        "master_accepted": False,
    }, "dependency ledger drifted")
    for key in (
        "accepted_exact_root", "validation_dependency_master_accepted",
        "authoritative_graph_reconciled", "audit_inventory_and_source_boundaries_accepted",
        "human_source_fidelity_resolved", "pinpoint_h0_and_independent_source_review",
        "independent_r0_review", "complete_transitive_provenance_and_tcb",
        "immutable_clean_release_input", "cold_empty_cache_offline_replay",
        "complete_sbom_license_and_offline_archive",
        "deterministic_content_addressed_release_bundle",
        "two_distinct_signed_runner_attestations", "independently_implemented_minimal_verifier",
        "protected_ci_and_required_adversarial_gates", "master_acceptance",
    ):
        require(decision["evidence_reconciliation"][key] is False,
                f"release silently cleared {key}")

    require(spec["schema_version"] == "stage1-validation-recipe/1.0",
            "release recipe schema drifted")
    require(spec["item_id"] == ITEM and spec["theorem_id"] == THEOREM,
            "release recipe identity drifted")
    require(spec["argv"] == ["python3", "-I", "-B", str(Path(__file__).relative_to(ROOT))],
            "release recipe argv drifted")
    require(spec["cwd"] == "." and spec["timeout_seconds"] == 300,
            "release recipe resources drifted")
    require(spec["network_policy"] == "denied" and spec["expected_exit"] == 0,
            "release network/exit contract drifted")
    require(spec["covered_obligation_ids"] == ALL_OBLIGATIONS,
            "release recipe misses frozen obligations")
    require(spec["covered_decisions"] == ["AUDIT-Z", "THEOREM-Z"],
            "release recipe misses terminal decisions")

    require(receipt["schema_version"] == "stage1-node-receipt/1.0",
            "release receipt schema drifted")
    require(receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM,
            "release receipt identity drifted")
    require(receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE,
            "release receipt base drifted")
    require(receipt["proposed_state"] == "[_]" and receipt["verdict"] == "blocked",
            "release receipt state drifted")
    require(receipt["accepted"] is receipt["master_accepted"] is
            receipt["release_grade"] is receipt["release_accepted"] is False,
            "release receipt claims acceptance")
    require(receipt["accepted_receipt_ids"] ==
            receipt["accepted_closed_obligation_ids"] == [],
            "release receipt grants accepted state")
    require(receipt["decision_id"] == decision["decision_id"] and
            receipt["decision_sha256"] == digest(HERE / "release-decision.json"),
            "release receipt decision binding drifted")
    require(receipt["release_spec_sha256"] == digest(HERE / "release-spec.json"),
            "release receipt recipe binding drifted")
    require(receipt["checker_sha256"] == digest(Path(__file__).resolve()),
            "release receipt checker binding drifted")
    require(receipt["public_projection_sha256"] == digest(HERE / "release-validation.md"),
            "release receipt projection binding drifted")
    require(receipt["dependency"] == decision["dependency"],
            "decision and receipt dependency ledgers disagree")
    for key in (
        "recipe_id", "cwd", "argv", "env_allowlist", "timeout_seconds",
        "network_policy", "network_enforcement", "expected_exit", "expected_outputs",
        "covered_obligation_ids", "covered_declarations", "covered_decisions",
        "coverage_kind", "scope_boundary",
    ):
        require(receipt["recipe"][key] == spec[key], f"receipt/spec mismatch: {key}")
    receipt_result = receipt["result"]
    require(receipt_result["verdict"] == "blocked" and
            receipt_result["lifecycle_before"] ==
            receipt_result["lifecycle_after"] == "planned",
            "receipt result advances blocked state")
    require(receipt_result["root_vector_before"] ==
            receipt_result["root_vector_after"] == accepted_vector,
            "receipt result changes accepted vector")
    require(receipt_result["accepted_receipt_ids"] ==
            receipt_result["accepted_closed_obligation_ids"] == [],
            "receipt result grants acceptance")
    require(receipt_result["authoritative_remaining_root_cut_set"] == ROOT_CUT,
            "receipt result root cut drifted")
    require(receipt_result["audit_complete"] is receipt_result["theorem_complete"] is
            receipt_result["release_accepted"] is False,
            "receipt result claims terminal completion")
    require(receipt_result["first_failed_gate"] ==
            "dependency.S56-M-1244-VALIDATION.master_acceptance",
            "receipt result first gate drifted")
    require(receipt_result["first_failed_release_gate"] ==
            "S56-10.6-HERMETIC-COLD-BUILD", "receipt result release gate drifted")
    expected_paths = {
        ".stage1-worker-selftest.json",
        f"Stage1_Instances/{THEOREM}/check_release.py",
        f"Stage1_Instances/{THEOREM}/release-decision.json",
        f"Stage1_Instances/{THEOREM}/release-receipt.json",
        f"Stage1_Instances/{THEOREM}/release-spec.json",
        f"Stage1_Instances/{THEOREM}/release-validation.md",
    }
    require(set(receipt["changed_paths"]) == expected_paths,
            "release receipt changed-path ledger drifted")
    require(receipt["known_failures"] == decision["known_failures"],
            "decision and receipt failure ledgers disagree")

    source_crosswalk = (HERE / "source_statement_crosswalk.md").read_text(encoding="utf-8")
    anchor_text = (HERE / "anchor_audit.md").read_text(encoding="utf-8")
    require("H1" in source_crosswalk and "independent" in source_crosswalk,
            "source-review debt is no longer explicit")
    require("operator norm" in anchor_text and "coordinate-square sum" in anchor_text,
            "energy/source-fidelity boundary is no longer explicit")
    public = "\n".join(
        (HERE / name).read_text(encoding="utf-8")
        for name in ("release-decision.json", "release-receipt.json", "release-validation.md")
    )
    require("/home/" not in public and ".cron/" not in public,
            "release decision leaks a private absolute path")
    require(re.search(r'"theorem_complete"\s*:\s*true', public) is None,
            "release decision claims theorem completion")

    replay_statement()
    for line in SUMMARY_LINES:
        print(line)


if __name__ == "__main__":
    main()
