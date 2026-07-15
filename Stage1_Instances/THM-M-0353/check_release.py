#!/usr/bin/env python3
"""Fail-closed release reconciliation for S56-M-0353-RELEASE."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess


if not __debug__:
    raise SystemExit("release validation requires Python assertions")

ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0353"
ITEM = "S56-M-0353-RELEASE"
THEOREM = "THM-M-0353"
BASE_REVISION = "c93e664d3a7e0383b037cfa2d5e47ba14adfb2cb"
BASE_TREE = "d8ea21a05ed52ff43d984128352a07f479aae6e6"
ROOT_VECTOR = {"H": "H1", "M": "M4", "R": "R4"}
EXPRESSION_SHA256 = (
    "planned:v1:sha256:1367304ec51ed39ff267372c97e62f55f36bde2ed1901683c076f889917bbe6f"
)
DENOMINATOR_SHA256 = (
    "4516c92f499b2c9dfc0c2097d27d1a7eb177a4965b00d4b1dcf38456d8efd0f0"
)
PROOF_RECEIPT_SHA256 = (
    "37046312afe3a15490decb23ac4688d4198d95ce3804f144a90897ae5d9ea167"
)
VALIDATION_RECEIPT_SHA256 = (
    "b03e2dd955521ffd6ea2ad28926c7ee2e068f3bd1b24f6108bb4874f39305a79"
)
VALIDATION_BASE = "b8c0a0c119a82ef435e23f9ff85bfd783db95736"
INVENTORY_IDS = [
    "M0353-ROOT",
    "M0353-T-ASSEMBLE",
    "M0353-P-MEMLP",
    "M0353-P-BASIS",
    "M0353-C-LP-VECTORS",
    "M0353-L-ORTHONORMAL",
    "M0353-L-DENSE",
    "M0353-C-HILBERT-BASIS",
    "M0353-L-GAUSSIAN-ORTH",
    "M0353-L-POLY-DENSE",
    "M0353-T-MEASURE",
    "M0353-S-NORMALIZATION",
    "M0353-X-HERMITE-POLY",
    "M0353-X-SOURCE",
    "M0353-X-TRUST",
    "M0353-X-PROVENANCE",
]
FROZEN_OPEN_CUT = ["M0353-P-MEMLP", "M0353-P-BASIS"]
UNRECONCILED_IDS = [
    "M0353-ROOT",
    "M0353-P-MEMLP",
    "M0353-P-BASIS",
    "M0353-C-LP-VECTORS",
    "M0353-L-ORTHONORMAL",
    "M0353-L-DENSE",
    "M0353-C-HILBERT-BASIS",
    "M0353-L-GAUSSIAN-ORTH",
    "M0353-L-POLY-DENSE",
    "M0353-T-MEASURE",
    "M0353-X-HERMITE-POLY",
    "M0353-X-SOURCE",
    "M0353-X-TRUST",
    "M0353-X-PROVENANCE",
]
EXPECTED_INPUTS = {
    "README.md": "27a7e9e986cd3c97e0bca15eed5344a8232a47a6e92701bc5381513a151a6525",
    "instance.json": "00478a787aaf2d703ed45d6fbf366258e7b79ebc913f515b3f19a5a86a484bc1",
    "task-dag.json": "f663ea0e3293ca14da37e4f1339f81df3ba582d3d9ed1573dae89d3eee608a8e",
    "Statement.lean": "58416bc39074209c0d725fce0a9c0dbf09725d847e2be24a77ebaa73527e2d99",
    "ObligationTree.lean": "fdd4f947aea690c1cdbfaeb1dcbff9ded6476267163c31c28f85d0792ab0dfbc",
    "Proof.lean": "8e911384a90dab39dd135b73e5205fb05cb673146e27743b2d51ca045e7b6e23",
    "Validation.lean": "8ec719b062588cc90970aaf9577bce7e540edbff14cde0225cf5217dbd96a0ed",
    "anchor-audit.json": "468b16881b49a74d5b868a3b8600b5d5b8be2c923024056e9432a2497ec7ebfe",
    "anchor-audit.md": "30169c3252efd23c46bef90b230f988fc50af6262adb4fcbdb0d2b85740bcc9d",
    "obligation-registry.json": "e87ac0a8bd1d6e1816f8816ec85d08e94686230e6afd00d294eca8f732bd6376",
    "typed-graphs.json": "868cdcbd5d6c2e049b21c8138016a96a0fdd1ba7e9eceba8ce5685032c3fc329",
    "source-statement-crosswalk.md": "8212233abf883f65e9e19cdfd0c69eed864f7b2284d11222f831384fbc7352eb",
    "proof-receipt.json": PROOF_RECEIPT_SHA256,
    "proof-validation.md": "308f01ce1d528494234585eba92398735b5c046d42a0ff1b2deff7aeead0c68c",
    "validation-spec.json": "08bef6ab179af2b9c56faca3c7e8fe3c488334ab027723b2640ca5bf77606a21",
    "validation-receipt.json": VALIDATION_RECEIPT_SHA256,
    "check_validation.py": "be06db65fe166809694f364f422fe8d00feb851d7abfacc5c3005035d0e9b89b",
    "validation-phase.md": "306ab9430f20f55c0399d4c03a7e175077c22c1ccfa2ab3989709c0fff0beaa1",
    "vendor-manifest.json": "7fb077d8c7a26522e65b3c9237d8500be15be4ffc55cee8e0ba68f3b24a5ab7c",
    "VENDOR_PROVENANCE.md": "94d06437c58c3ff5a364001b50c53ae9ce1001525021c0dfef2eb7b22f5ea700",
    "Vendor/LICENSE": "2d3b806e6fd270f11819d0f797f721747adb0d497760e1b9053b6cd1fae4cf54",
    "Vendor/GaussianField/HermiteFunctions.lean": (
        "e25548a1e042a61b340e24931dc05fd49bcaa6cf1daf68c335859df58d3b3d49"
    ),
    "check_proof.sh": "1726c71d35d2dfd586e35acc95451eb4822df40dae392a9c8140c6b99b7fcabf",
}
EXPECTED_AUTHORITY = {
    "Docs/Stage1_Targets_rev-5.6.json": "02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c",
    "Docs/Stage1_Execution_DAG_rev-5.6.json": "e4c99404c6ce0f157d5567ac76cbac7470870ed9a25ae9d2afea24bca18859aa",
    "Docs/Stage1_Blueprint_rev-5.6.md": "a8fd3d878262ba7488c9fdd75b419e4aa32a6bd1d2831c5737c0c743bd3833a5",
    "Docs/Blueprint_Guidelines.md": "a06c07b5ca1b270b4935ad3dab893e9a0e078c29c8da2ef9dca1e71193310535",
    "skills/execute-stage1-rev56/SKILL.md": "26d47a66c6535feabb8bbf1051fd55d76a53fe761f4b3d953f86b97ec86152b8",
    "Formalizations/Lean/lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "Formalizations/Lean/lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
EXPECTED_RELEASE = {
    "release-spec.json": "b934598bf39a71703c3480ca98b077639be41a5f8f25ce1542f5638187f81517",
    "release-decision.json": "4900e2d48e3d212e4469cda42757abba71f6ff39c98048f91216d186b5deb756",
    "release-validation.md": "053a3cbfbe46fe947bab1e429e275c9d8515fdb0a6b68440bcd6989a6eab20ed",
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
    "PASS reconciled provisional proof evidence: exact root was sorry-free at trust zero with the recorded axioms",
    "BLOCKED dependency.S56-M-0353-VALIDATION.master_acceptance",
    "BLOCKED current validation freshness: recorded recipe is bound to ancestor b8c0a0c1",
    "BLOCKED AUDIT-Z and THEOREM-Z; accepted root remains H1/M4/R4",
    "BLOCKED immutable cold release, complete trust/SBOM, distinct verification, and deterministic bundle gates",
    "verdict=blocked audit_complete=false theorem_complete=false accepted_receipts=0",
)
KNOWN_FAILURES = [
    "S56-M-0353-VALIDATION and every transitive phase receipt remain provisional rather than dependency-ordered master accepted or release-grade.",
    "The integrated validation recipe is snapshot-bound to b8c0a0c119a82ef435e23f9ff85bfd783db95736 and fails its HEAD freshness assertion at the current integrated base; its historical result is not current release evidence.",
    "The authoritative planned instance remains H1/M4/R4 with accepted_proof_state=[], while the frozen graph remains root-open at M0353-P-MEMLP and M0353-P-BASIS and binds no accepted evidence.",
    "The frozen weighted-polynomial-density architecture is not accepted as reconciled with the vendored Gaussian-moment and Fourier-uniqueness proof route and local complex adapter.",
    "The primary-source crosswalk is not independently accepted H0, and no required node has independently accepted R0 evidence.",
    "The observed axiom set has no accepted theorem-specific foundation policy, and complete transitive declaration, source-origin, compiled-artifact, TCB, computation, SBOM, archive, and license closure are absent.",
    "The current source replay reuses the automation-provided shared warm pinned artifacts; there is no immutable clean input, empty-cache cold offline restoration, two distinct signed runners, independently implemented minimal verifier, protected release CI, or deterministic release bundle.",
    "Accepted state remains H1/M4/R4 with audit_complete=false and theorem_complete=false; no M0-P/E0/E1, AUDIT-Z, THEOREM-Z, release, or theorem-completion credit is granted.",
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
        assert re.fullmatch(r"[0-9a-f]{64}", expected), (name, expected)
        assert sha256(HERE / name) == expected, name

    targets = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    instance = load(HERE / "instance.json")
    tasks = load(HERE / "task-dag.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    proof = load(HERE / "proof-receipt.json")
    validation = load(HERE / "validation-receipt.json")
    decision = load(HERE / "release-decision.json")
    receipt = load(HERE / "release-receipt.json")
    spec = load(HERE / "release-spec.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")

    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 846 and target["baseline"] == "L0"
    assert target["rework_required"] is True and target["lifecycle_mode"] == "planned"
    assert target["theorem_complete"] is False
    release_item = next(row for row in execution["items"] if row["id"] == ITEM)
    validation_item = next(
        row for row in execution["items"] if row["id"] == "S56-M-0353-VALIDATION"
    )
    assert release_item == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 846,
        "phase": "release",
        "layer": 6,
        "state": "[ ]",
        "depends_on": [validation_item["id"]],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Reconcile evidence and decide the exact theorem-completion verdict.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    assert validation_item["state"] == "[_]" and validation_item["attempts"] == 1

    assert instance["lifecycle"] == tasks["lifecycle"] == "planned"
    assert instance["root_vector"] == ROOT_VECTOR
    assert instance["accepted_proof_state"] == tasks["accepted_states"] == []
    assert instance["audit_complete"] is instance["theorem_complete"] is False
    assert all(row["state"] == "open" for row in tasks["tasks"])
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert registry["frozen_denominators"]["inventory"] == INVENTORY_IDS
    assert graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert graphs["closure_boundary"] == {
        "root_closed": False,
        "theorem_complete": False,
        "minimal_open_root_cut": FROZEN_OPEN_CUT,
    }

    assert sha256(HERE / "proof-receipt.json") == PROOF_RECEIPT_SHA256
    assert proof["canonical_target_expression_sha256"] == EXPRESSION_SHA256
    assert proof["accepted"] is False and proof["accepted_closed_obligation_ids"] == []
    assert proof["result"]["root_kernel_closed"] is True
    assert proof["result"]["accepted_root_closed"] is proof["result"]["theorem_complete"] is False
    assert sha256(HERE / "validation-receipt.json") == VALIDATION_RECEIPT_SHA256
    assert validation["base_revision"] == VALIDATION_BASE
    assert validation["accepted"] is validation["release_grade"] is False
    assert validation["verdict"] == "blocked" and validation["accepted_receipt_ids"] == []
    assert validation["result"]["audit_complete"] is validation["result"]["theorem_complete"] is False
    assert validation["result"]["accepted_closed_obligation_ids"] == []
    assert validation["remaining_root_cut_set"] == FROZEN_OPEN_CUT
    assert validation["first_failed_gate"] == "dependency.S56-M-0353-PROOF.master_acceptance"

    assert decision["schema_version"] == "stage1-release-decision/1.0"
    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert decision["item_id"] == receipt["item_id"] == packet["item_id"] == ITEM
    assert decision["theorem_id"] == receipt["theorem_id"] == THEOREM
    assert decision["phase"] == receipt["phase"] == "release"
    assert decision["intent"] == receipt["intent"] == "release"
    assert decision["depends_on"] == receipt["depends_on"] == [validation_item["id"]]
    assert decision["execution_rank"] == receipt["execution_rank"] == 846
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
        "dependency.S56-M-0353-VALIDATION.master_acceptance"
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
        "receipt_base_revision": VALIDATION_BASE,
        "current_snapshot_recipe_replayable": False,
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
    assert spec["cwd"] == "." and spec["network_policy"] == "denied"
    assert spec["expected_exit"] == 0 and spec["covered_obligation_ids"] == INVENTORY_IDS
    assert spec["covered_decisions"] == ["AUDIT-Z", "THEOREM-Z"]
    assert spec["coverage_kind"] == "negative_release_reconciliation_no_closure_credit"

    assert set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert packet["state"] == receipt["proposed_state"] == decision["proposed_state"] == "[_]"
    assert packet["base_revision"] == BASE_REVISION
    assert "truthfully blocked" in packet["output_summary"]
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
    assert "theorem hermiteCompletenessTarget_proof : HermiteCompletenessTarget := by" in (
        HERE / "Proof.lean"
    ).read_text(encoding="utf-8")
    for relative in CHANGED_PATHS - {".stage1-worker-selftest.json"}:
        assert_text_hygiene(ROOT / relative)

    print(expected_stdout, end="")


if __name__ == "__main__":
    main()
