#!/usr/bin/env python3
"""Fail-closed release reconciliation for S56-M-0319-RELEASE."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess


if not __debug__:
    raise SystemExit("release validation requires Python assertions")

ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0319"
ITEM = "S56-M-0319-RELEASE"
THEOREM = "THM-M-0319"
BASE_REVISION = "80f0191c83a1bb4026c2d490be957cf109464de1"
BASE_TREE = "b89a01cfc623bf97d1896fb3534a1ac24381fa71"
ROOT_VECTOR = {"H": "H1", "M": "M4", "R": "R4"}
EXPRESSION_SHA256 = (
    "2e4dc02230de7a1c08fdf4a19ef0ec1da107297972dee0e85d893bdb33d6a514"
)
DENOMINATOR_SHA256 = (
    "9d15b5eafa794b7f3cc1e83d4006447c90a75f8d8175bbaeb4b50fe8306ccee8"
)
PROOF_RECEIPT_SHA256 = (
    "3330f95b90aa4a2dd09187d4326bfeda1f2b671e6e6462c1e939b4d77982df90"
)
VALIDATION_RECEIPT_SHA256 = (
    "4786c82eeadf4d89a53e256ced8875a51988b6e8e5c9c8b769a5b2f2d3229a33"
)
INVENTORY_IDS = [
    "M0319-ROOT",
    "M0319-S-DEFINITIONS",
    "M0319-S-BOUNDARY",
    "M0319-S-FOUNDATION",
    "M0319-T-SUBTYPE",
    "M0319-N-FINITE-DIM",
    "M0319-R-CONVEX-CUBE",
    "M0319-L-UNIT-CUBE",
    "M0319-T-EXTERNAL",
    "M0319-X-INTEGRATION",
    "M0319-X-SOURCE",
    "M0319-X-PROVENANCE",
]
FROZEN_OPEN_CUT = ["M0319-T-EXTERNAL"]
UNRECONCILED_IDS = [
    "M0319-ROOT",
    "M0319-S-FOUNDATION",
    "M0319-R-CONVEX-CUBE",
    "M0319-L-UNIT-CUBE",
    "M0319-T-EXTERNAL",
    "M0319-X-INTEGRATION",
    "M0319-X-PROVENANCE",
]
EXPECTED_INPUTS = {
    "README.md": "ca1f7e08ee2667b6ffaf1f72478aad5c6e5eebf54c8c280f489f84fa2881b063",
    "instance.json": "a879bb26874c531fbf628a8cab1f72f2ee9ac45866430dbeb29c8bb36bd261a9",
    "task-dag.json": "cbad5a4d5f276a8081825d9558039de2c3ebb333c0b2304bf7bf070bc0292564",
    "Statement.lean": "1b2804bde5a77937dc470ccf1f6e54856d98b86e268b5dc30fe19f0a84bc440a",
    "ObligationTree.lean": "e80086143cdf2bf3b2e5ab42da94217dffddd062dd157609b6565c8a8de67cbd",
    "Proof.lean": "793e81e88075d53b3a1a11226808a12bf910bf89f4323ecee701ae125bdd2f38",
    "Validation.lean": "d1323014a1c1d339683d3ac463a18071085163c68b103215504ec8cc222f7187",
    "statement.json": "fecb49cb5ce1392bd29c3eef365c55a003dca217b9dab415bab2ad9cb8e3e1ca",
    "anchor-audit.json": "747de378a621b873e2eb5f96016c6d7429c350e7dbb619d20f1994b6af70f524",
    "obligation-registry.json": "6e0d9d0b3ff8044cd0162c47b3f8aee57ecf4070fcc517b38a1b58011e398d2f",
    "typed-graphs.json": "983c863161c535ecaee625f7b34b1f52dc5852beaa75189eaaf561175a644428",
    "source-statement-crosswalk.md": "20694f6cc26c947b18af187bac350f89a57ba03ab97c0c42c980c2f4aaf26abb",
    "proof-receipt.json": PROOF_RECEIPT_SHA256,
    "proof-blocker.json": "191816f73c04567fcdf4b67f6cbf51d876ee668855c881f4685526780562d0cd",
    "validation-spec.json": "966e657d4e7c45d73d4554fc5153f29a101e375fe61969a39678b7e615e6a11e",
    "validation-receipt.json": VALIDATION_RECEIPT_SHA256,
    "check_validation.py": "c8befa2250af3dc8ddd0fce0ab722cda9c3bb6418e1deb3c4b6d3784670761f0",
    "validation-phase.md": "1f7571d67ccab33b889b408468ad9e69921fe23e8ca2c335a29e260696dcf04b",
    "vendor-manifest.json": "d344d645fc61ac6a4cc3e8c22dc803bff84312c1ebe25a508469e6ab54f98bc7",
    "VENDOR_PROVENANCE.md": "c6736160e360ea36b3a1be90cd9036716069e56e4b52e9f413ed9d02fdaf8c2f",
    "Vendor/LICENSE": "956bddafa77f8b8ad428bb35cf59424b0ddd0933ebab506037b97a20fab1a5d0",
    "Vendor/Gametheory/Scarf.lean": "210dc01a3b823527ce3c4c079879ee897ef6f7aefb9e9a15406a20eeedcb92a6",
    "Vendor/Gametheory/ScarfPath.lean": "d9e661c3e46e9d0ffcdbed7ca62696d6baed5aa77f5e834002d307b30c86b2bd",
    "Vendor/Gametheory/Brouwer.lean": "8cb62d7ae0820c620e9665a9124e2f07b7b5c20da8455a44a633b1e6e8948110",
    "check_proof.sh": "3b1f4b0708e13445b5b45a07c1209195e16d2b610e29d83bf4d734b6f3a51b67",
}
EXPECTED_AUTHORITY = {
    "Docs/Stage1_Targets_rev-5.6.json": "02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c",
    "Docs/Stage1_Execution_DAG_rev-5.6.json": "157c510f0eb573d9f0a1ca1d2550434e5786927cd3bf44c6ae650884ea46e0df",
    "Docs/Stage1_Blueprint_rev-5.6.md": "5cfad5ca4137eec0b06fd8b615223b94cc493f831086beb40a5ce7a28841860b",
    "Docs/Blueprint_Guidelines.md": "a06c07b5ca1b270b4935ad3dab893e9a0e078c29c8da2ef9dca1e71193310535",
    "skills/execute-stage1-rev56/SKILL.md": "26d47a66c6535feabb8bbf1051fd55d76a53fe761f4b3d953f86b97ec86152b8",
    "Formalizations/Lean/lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "Formalizations/Lean/lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
EXPECTED_RELEASE = {
    "release-spec.json": "e3001603bd5e19f97f49d9e5a7738250bfc14c86c809aecf24bdebe70f56ad7e",
    "release-decision.json": "897fec20fb33d6f41abc6593da64e912fb53230c85d2622dc320de53d69e4068",
    "release-validation.md": "8748f29cfbb91853f6484d3916f84549ce07ff494090b1b0e7a4fb58a12ac1f1",
}
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/check_release.py",
    f"Stage1_Instances/{THEOREM}/release-decision.json",
    f"Stage1_Instances/{THEOREM}/release-receipt.json",
    f"Stage1_Instances/{THEOREM}/release-spec.json",
    f"Stage1_Instances/{THEOREM}/release-validation.md",
}
SUMMARY_LINES = (
    "PASS release reconciliation: authority, target inputs, and provisional receipts are hash-bound",
    "PASS current warm proof evidence: exact root is sorry-free at trust zero with the recorded axioms",
    "BLOCKED dependency.S56-M-0319-VALIDATION.master_acceptance",
    "BLOCKED AUDIT-Z and THEOREM-Z; accepted root remains H1/M4/R4",
    "BLOCKED immutable cold release, distinct verification, and deterministic bundle gates",
    "verdict=blocked audit_complete=false theorem_complete=false accepted_receipts=0",
)
KNOWN_FAILURES = [
    "S56-M-0319-VALIDATION and every transitive phase receipt remain provisional rather than dependency-ordered master accepted or release-grade.",
    "The authoritative instance, target-local task DAG, obligation registry, and typed graph remain planned and pre-proof, retain accepted_states=[], and keep M0319-T-EXTERNAL as the open root cut.",
    "The frozen graph models the former Harfe and cube route, while Proof.lean uses an MIT-licensed simplex theorem, finite partition of unity, and compact displacement minimization; no accepted graph, provenance, or composition reconciliation exists.",
    "The primary human source mapping is not independently accepted H0, and no required node has independently accepted R0 evidence.",
    "The observed axiom set has no accepted theorem-specific foundation policy, and complete transitive declaration, source-origin, compiled-artifact, TCB, computation, SBOM, archive, and license closure are absent.",
    "The integrated validation recipe is stale at current HEAD; its historical network-isolated result and the current proof replay both reuse shared warm artifacts and are nonrelease evidence.",
    "There is no immutable clean source snapshot, empty-cache cold offline reproduction, two distinct signed runner attestations, independently implemented minimal verifier, protected release CI evidence, deterministic release bundle, or master acceptance.",
    "Accepted state remains H1/M4/R4 with audit_complete=false and theorem_complete=false; no M0/E0/E1, AUDIT-Z, THEOREM-Z, release, or theorem-completion credit is granted.",
]


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


def git(*args: str) -> str:
    result = subprocess.run(
        ["/usr/bin/git", *args], cwd=ROOT, text=True, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, timeout=30, check=False,
    )
    assert result.returncode == 0, result.stdout
    return result.stdout.strip()


def assert_text_hygiene(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines()), path


def main() -> None:
    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    for name, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == expected, name
    for name, expected in EXPECTED_AUTHORITY.items():
        assert sha256(ROOT / name) == expected, name
    for name, expected in EXPECTED_RELEASE.items():
        assert sha256(HERE / name) == expected, name

    targets = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    instance = load(HERE / "instance.json")
    tasks = load(HERE / "task-dag.json")
    statement = load(HERE / "statement.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    proof = load(HERE / "proof-receipt.json")
    validation = load(HERE / "validation-receipt.json")
    decision = load(HERE / "release-decision.json")
    receipt = load(HERE / "release-receipt.json")
    spec = load(HERE / "release-spec.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")

    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 685 and target["baseline"] == "L0"
    assert target["rework_required"] is True and target["lifecycle_mode"] == "planned"
    assert target["theorem_complete"] is False
    release_item = next(row for row in execution["items"] if row["id"] == ITEM)
    validation_item = next(
        row for row in execution["items"] if row["id"] == "S56-M-0319-VALIDATION"
    )
    assert release_item["state"] == "[ ]" and release_item["attempts"] == 0
    assert release_item["depends_on"] == [validation_item["id"]]
    assert validation_item["state"] == "[_]" and validation_item["attempts"] == 1

    assert instance["lifecycle"] == tasks["lifecycle"] == "planned"
    assert instance["root_vector"] == ROOT_VECTOR
    assert instance["accepted_proof_state"] == tasks["accepted_states"] == []
    assert instance["audit_complete"] is instance["theorem_complete"] is False
    assert all(row["state"] == "open" for row in tasks["tasks"])
    assert statement["canonical_formal_target"]["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert registry["frozen_denominators"]["inventory"] == INVENTORY_IDS
    assert graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert graphs["closure_boundary"] == {
        "root_closed": False,
        "minimal_open_root_cut": FROZEN_OPEN_CUT,
        "theorem_complete": False,
    }

    assert sha256(HERE / "proof-receipt.json") == PROOF_RECEIPT_SHA256
    assert proof["accepted"] is False and proof["accepted_receipt_ids"] == []
    assert proof["accepted_closed_obligation_ids"] == []
    assert proof["result"]["root_kernel_inhabitant_observed"] is True
    assert proof["result"]["accepted_root_closed"] is proof["result"]["theorem_complete"] is False
    assert proof["graph_reconciliation_pending"]["unreconciled_obligation_ids"] == UNRECONCILED_IDS
    assert sha256(HERE / "validation-receipt.json") == VALIDATION_RECEIPT_SHA256
    assert validation["accepted"] is validation["release_grade"] is False
    assert validation["verdict"] == "blocked" and validation["accepted_receipt_ids"] == []
    assert validation["result"]["audit_complete"] is validation["result"]["theorem_complete"] is False
    assert validation["result"]["accepted_closed_obligation_ids"] == []
    assert validation["remaining_root_cut_set"] == FROZEN_OPEN_CUT
    assert validation["first_failed_gate"] == "dependency.S56-M-0319-PROOF.master_acceptance"

    assert decision["schema_version"] == "stage1-release-decision/1.0"
    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert decision["item_id"] == receipt["item_id"] == packet["item_id"] == ITEM
    assert decision["theorem_id"] == receipt["theorem_id"] == THEOREM
    assert decision["phase"] == receipt["phase"] == "release"
    assert decision["intent"] == receipt["intent"] == "release"
    assert decision["depends_on"] == receipt["depends_on"] == [validation_item["id"]]
    assert decision["execution_rank"] == receipt["execution_rank"] == 685
    assert decision["decision_id"] == receipt["decision_id"] == receipt["receipt_id"]
    assert decision["verdict"] == receipt["verdict"] == "blocked"
    assert decision["base_revision"] == receipt["base_revision"] == BASE_REVISION
    assert decision["base_tree"] == receipt["base_tree"] == BASE_TREE
    assert decision["lifecycle_before"] == decision["lifecycle_after"] == "planned"
    assert decision["root_vector"]["accepted_before"] == ROOT_VECTOR
    assert decision["root_vector"]["accepted_after"] == ROOT_VECTOR
    assert decision["accepted_receipt_ids"] == decision["accepted_closed_obligation_ids"] == []
    assert decision["terminal_decisions"] == {
        "audit_complete": False,
        "theorem_complete": False,
        "audit_z": "blocked",
        "theorem_z": "blocked",
        "release_accepted": False,
    }
    assert decision["authoritative_remaining_root_cut_set"] == FROZEN_OPEN_CUT
    assert decision["unreconciled_architecture_obligation_ids"] == UNRECONCILED_IDS
    assert decision["first_failed_gate"]["node_gate"] == (
        "dependency.S56-M-0319-VALIDATION.master_acceptance"
    )
    assert decision["evidence_reconciliation"]["integrated_validation_recipe_current"] is False

    expected_dependency = {
        "item_id": validation_item["id"],
        "scheduler_projection": "[_]",
        "receipt_id": validation["receipt_id"],
        "receipt_sha256": VALIDATION_RECEIPT_SHA256,
        "support_state": "provisional_worker_selftest",
        "accepted": False,
        "release_grade": False,
        "master_accepted": False,
        "verdict": "blocked",
    }
    assert decision["dependency"] == receipt["dependency"] == expected_dependency
    assert receipt["accepted"] is receipt["master_accepted"] is False
    assert receipt["release_grade"] is receipt["release_accepted"] is False
    assert receipt["accepted_receipt_ids"] == receipt["accepted_closed_obligation_ids"] == []
    assert receipt["decision_sha256"] == sha256(HERE / "release-decision.json")
    assert receipt["release_spec_sha256"] == sha256(HERE / "release-spec.json")
    assert receipt["public_projection_sha256"] == sha256(HERE / "release-validation.md")
    assert re.fullmatch(r"[0-9a-f]{64}", receipt["checker_sha256"])
    assert receipt["result"]["root_vector_before"] == ROOT_VECTOR
    assert receipt["result"]["root_vector_after"] == ROOT_VECTOR
    assert receipt["result"]["authoritative_remaining_root_cut_set"] == FROZEN_OPEN_CUT
    assert receipt["result"]["audit_complete"] is receipt["result"]["theorem_complete"] is False
    expected_stdout = "\n".join(SUMMARY_LINES) + "\n"
    assert receipt["execution"]["checker_stdout_sha256"] == hashlib.sha256(
        expected_stdout.encode()
    ).hexdigest()
    assert receipt["execution"]["checker_stdout_bytes"] == len(expected_stdout.encode())
    assert receipt["known_failures"] == decision["known_failures"] == packet["known_failures"] == KNOWN_FAILURES

    for path, expected in receipt["input_bindings"].items():
        assert expected == sha256(ROOT / path), path
    expected_binding_paths = {
        *(f"Stage1_Instances/{THEOREM}/{name}" for name in EXPECTED_INPUTS),
        *EXPECTED_AUTHORITY,
    }
    assert set(receipt["input_bindings"]) == expected_binding_paths

    assert spec["schema_version"] == "stage1-validation-recipe/1.0"
    assert spec["item_id"] == ITEM and spec["theorem_id"] == THEOREM
    assert spec["cwd"] == "." and spec["network_policy"] == "denied_not_required"
    assert spec["expected_exit"] == 0 and spec["covered_obligation_ids"] == INVENTORY_IDS
    assert spec["covered_decisions"] == ["AUDIT-Z", "THEOREM-Z"]
    assert spec["coverage_kind"] == "negative_release_reconciliation_no_closure_credit"

    assert set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert packet["state"] == receipt["proposed_state"] == decision["proposed_state"] == "[_]"
    assert packet["base_revision"] == BASE_REVISION
    assert "verdict is blocked" in packet["output_summary"]
    assert "audit_complete=false" in packet["output_summary"]
    assert "theorem_complete=false" in packet["output_summary"]
    assert set(packet["changed_paths"]) == set(receipt["changed_paths"]) == CHANGED_PATHS
    assert set(receipt["repository_state"]["changed_paths"]) == CHANGED_PATHS

    actual = {
        line[3:] for line in git("status", "--short", "--untracked-files=all").splitlines()
    }
    actual.discard("Formalizations/Lean/.lake")
    assert actual == CHANGED_PATHS, (actual, CHANGED_PATHS)
    assert (ROOT / "Formalizations/Lean/.lake").is_symlink()
    assert re.search(
        r"theorem\s+brouwerFixedPoint\s*:\s*BrouwerFixedPointTarget\s*:=",
        (HERE / "Proof.lean").read_text(encoding="utf-8"),
    )
    for relative in CHANGED_PATHS - {".stage1-worker-selftest.json"}:
        assert_text_hygiene(ROOT / relative)

    print(expected_stdout, end="")


if __name__ == "__main__":
    main()
