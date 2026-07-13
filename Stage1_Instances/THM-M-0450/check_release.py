#!/usr/bin/env python3
"""Fail-closed reconciliation check for S56-M-0450-RELEASE."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
import re
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0450"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM = "S56-M-0450-RELEASE"
THEOREM = "THM-M-0450"
BASE_REVISION = "db3681c9e2616e7be7e8b5fde7fe48c77d6df6fe"
BASE_TREE = "03ebac35e51f1236b49c6a3110b748d45c6c2682"
VALIDATION_RECEIPT_SHA256 = (
    "ac0c90344973eb217597971de9ce69b48736f36081cbb32739feb7b87f6cc159"
)
STATEMENT_FINGERPRINT = (
    "lean:Stage1Instances.THM_M_0450.ExactTarget@"
    "25441c035ace49d13ff9f5f2d0a1c1fbd6c5df9c76ad9674e9fbff0c870a68c1"
)
DENOMINATOR_SHA256 = (
    "72f2ac93d10c6e4c5b106c189ee5823c50970d512e054fb247b6796ad00d8e24"
)
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
INVENTORY_IDS = [
    "M0450-ROOT",
    "M0450-S",
    "M0450-T-ASSEMBLE",
    "M0450-B-WEAKMW",
    "M0450-B-KUMMER",
    "M0450-B-QUOTIENT",
    "M0450-H-HEIGHT",
    "M0450-H-NONNEG",
    "M0450-H-PARALLEL",
    "M0450-H-NORTHCOTT",
    "M0450-X-TRANSPORT",
    "M0450-X-SOURCE",
    "M0450-X-PROVENANCE",
    "M0450-X-TRUST",
]
GRAPH_CUT = [
    "M0450-B-WEAKMW",
    "M0450-H-HEIGHT",
    "M0450-X-TRANSPORT",
    "M0450-X-SOURCE",
    "M0450-X-PROVENANCE",
    "M0450-X-TRUST",
]
VECTOR = {"H": "H1", "M": "M3", "R": "R3"}
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/check_release.py",
    f"Stage1_Instances/{THEOREM}/release-decision.json",
    f"Stage1_Instances/{THEOREM}/release-phase.md",
    f"Stage1_Instances/{THEOREM}/release-receipt.json",
    f"Stage1_Instances/{THEOREM}/release-spec.json",
}
UPSTREAM_INPUTS = {
    "Statement.lean": "fcec6a21a86d796e75a2e66f1c9ef2a5ab57ab6835a2511a19c78909ff60c1af",
    "ObligationTree.lean": "026c26cf037f0de96c2719f882cf0307703c09c19b3120377871ac6648c61b85",
    "Proof.lean": "fd34aa7255fad4a878cac37ac116b0e4afeec0d3fda854ca96da91e1140848fc",
    "Validation.lean": "af99ba05e040f5a2ebd18aa7b621fbfcae126ddd290d2677b5fdf873748aa8b4",
    "intake.json": "a577a3813b4acb5a66c5d308a314ab6732ade0e209ce35955763c0296633c8cb",
    "statement.json": "2f01be0b3bb57829dd7d583607ec4f8b94b7029626c65b845ee2ce8705acead5",
    "anchor-audit.json": "7be4cb52b88c9a71e680ff927ebfae628e3120fca5a218dcfba564cb08af7d19",
    "obligation-registry.json": "3ca6f63a8dd5f0deb5af4a9c492c6834fb832c50c42498caba37f42e51b58e4f",
    "typed-graphs.json": "0911a73bcf074ce82d599c7f08ea005934538dc58ebfa83ecf589386d8898a63",
    "proof-receipt.json": "46968de57e83ee17832633e58341b2a7e2d22fc346d0245dc67d73f890f11e4b",
    "validation-spec.json": "7cc7d22e1a78ad21d13115c498b1c0201976a7199d6c9c8603b330fdfc4708a0",
    "validation-receipt.json": VALIDATION_RECEIPT_SHA256,
    "check_validation.py": "2d199e13245b6152bacb0528a343a0f2210f3676bbdb1a0026134a723c374b03",
}
AUTHORITY_INPUTS = {
    "Docs/Stage1_Targets_rev-5.6.json": (
        "02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c"
    ),
    "Docs/Stage1_Execution_DAG_rev-5.6.json": (
        "7b5818855c1b018a84b705c1c173a8b48b616e9ec0dffb3700aac9da3cfd6d44"
    ),
    "skills/execute-stage1-rev56/SKILL.md": (
        "26d47a66c6535feabb8bbf1051fd55d76a53fe761f4b3d953f86b97ec86152b8"
    ),
}
TOOL_INPUTS = {
    "lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict), path
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(
    argv: list[str], *, cwd: Path = ROOT, timeout: int = 360
) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        argv,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=timeout,
        check=False,
    )
    assert result.returncode == 0, (
        f"command failed ({result.returncode}): {argv!r}\n{result.stdout}"
    )
    return result


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["git", *args], cwd=cwd).stdout.strip()


def without_comments(source: str) -> str:
    source = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
    return re.sub(r"--.*$", "", source, flags=re.MULTILINE)


def assert_text_hygiene(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n"), f"missing final newline: {path}"
    assert b"\r" not in data and b"\x00" not in data, f"bad bytes: {path}"
    assert all(
        not line.endswith((b" ", b"\t")) for line in data.splitlines()
    ), f"trailing whitespace: {path}"


def main() -> None:
    if sys.flags.optimize != 0:
        raise RuntimeError("release checker requires Python assertions")

    decision = load(HERE / "release-decision.json")
    receipt = load(HERE / "release-receipt.json")
    spec = load(HERE / "release-spec.json")
    validation = load(HERE / "validation-receipt.json")
    proof = load(HERE / "proof-receipt.json")
    intake = load(HERE / "intake.json")
    statement = load(HERE / "statement.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")
    execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")
    targets = load(ROOT / "Docs" / "Stage1_Targets_rev-5.6.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    for name, expected in UPSTREAM_INPUTS.items():
        assert sha256(HERE / name) == expected, f"upstream input drifted: {name}"
    for name, expected in AUTHORITY_INPUTS.items():
        assert sha256(ROOT / name) == expected, f"authority input drifted: {name}"
    for name, expected in TOOL_INPUTS.items():
        assert sha256(LEAN_ROOT / name) == expected, f"tool input drifted: {name}"

    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 92
    assert target["lifecycle_mode"] == "planned"
    assert target["baseline"] == "L0" and target["rework_required"] is True
    assert target["legacy_artifacts_accepted"] is False
    assert target["theorem_complete"] is False

    release_item = next(row for row in execution["items"] if row["id"] == ITEM)
    validation_item = next(
        row
        for row in execution["items"]
        if row["id"] == "S56-M-0450-VALIDATION"
    )
    assert release_item == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 92,
        "phase": "release",
        "layer": 6,
        "state": "[ ]",
        "depends_on": ["S56-M-0450-VALIDATION"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": (
            "Reconcile evidence and decide the exact theorem-completion verdict."
        ),
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    assert validation_item["state"] == "[_]"
    assert validation_item["depends_on"] == ["S56-M-0450-PROOF"]

    assert spec["schema_version"] == "stage1-validation-recipe/1.0"
    assert spec["item_id"] == receipt["item_id"] == decision["item_id"] == ITEM
    assert spec["theorem_id"] == receipt["theorem_id"] == THEOREM
    assert spec["recipe_id"] == decision["release_recipe_id"]
    assert spec["argv"] == [
        "python3",
        "-B",
        f"Stage1_Instances/{THEOREM}/check_release.py",
    ]
    assert spec["cwd"] == "." and spec["timeout_seconds"] == 360
    assert spec["network_policy"] == "partially_enforced_nested_lean_only"
    assert spec["expected_exit"] == 0
    assert spec["covered_obligation_ids"] == INVENTORY_IDS

    assert decision["theorem_id"] == THEOREM and decision["execution_rank"] == 92
    assert decision["phase"] == decision["intent"] == "release"
    assert decision["base_revision"] == receipt["base_revision"] == BASE_REVISION
    assert decision["base_tree"] == receipt["base_tree"] == BASE_TREE
    assert decision["decision_support"] == receipt["support_state"]
    assert decision["proposed_state"] == receipt["proposed_state"] == "[_]"
    assert decision["release_grade"] is receipt["release_grade"] is False
    assert receipt["accepted"] is False and receipt["master_acceptance"] is False
    assert receipt["decision_id"] == decision["decision_id"]
    decided_at = datetime.fromisoformat(decision["decided_at"])
    validated_at = datetime.fromisoformat(receipt["validated_at"])
    now = datetime.now(timezone.utc)
    assert decided_at.tzinfo is not None and decided_at.astimezone(timezone.utc) <= now
    assert validated_at.tzinfo is not None and validated_at.astimezone(timezone.utc) <= now
    assert decided_at == validated_at
    assert decision["decision_id"].endswith("20260714T021800+0800")
    assert receipt["receipt_id"].endswith("20260714T021800+0800")
    assert decision["canonical_statement_fingerprint"] == STATEMENT_FINGERPRINT
    assert receipt["statement_fingerprint"] == STATEMENT_FINGERPRINT
    assert decision["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert receipt["registry_denominator_sha256"] == DENOMINATOR_SHA256

    dependency = decision["dependency"]
    assert dependency["item_id"] == validation["item_id"]
    assert dependency["receipt_id"] == validation["receipt_id"]
    assert dependency["receipt_sha256"] == VALIDATION_RECEIPT_SHA256
    assert dependency["support_state"] == validation["support_state"]
    assert dependency["release_grade"] is validation["release_grade"] is False
    assert dependency["accepted"] is False and dependency["master_accepted"] is False
    assert validation["support_state"] == "provisional_worker_selftest"
    assert decision["provisional_receipt_ids_inspected"] == [
        proof["receipt_id"],
        validation["receipt_id"],
    ]

    assert intake["lifecycle_mode"] == "planned"
    assert intake["root_vector"] == {
        "human": "H1",
        "machine": "M3",
        "readability": "R3",
    }
    assert intake["theorem_complete"] is False
    assert statement["lean"]["normalized_expression_output_sha256"] == (
        STATEMENT_FINGERPRINT.rsplit("@", 1)[1]
    )
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert registry["frozen_denominators"]["inventory"] == INVENTORY_IDS
    closure = graphs["closure_boundary"]
    assert closure["root_closed"] is False
    assert closure["audit_complete"] is closure["theorem_complete"] is False
    assert closure["remaining_root_cut_set"] == GRAPH_CUT
    assert set(closure["closed_obligations"]) == {"M0450-S"}
    assert closure["conditionally_composed_obligations"] == ["M0450-T-ASSEMBLE"]

    assert proof["support_state"] == "provisional_worker_selftest"
    assert proof["closed_obligation_ids"] == []
    assert proof["result"]["root_closed"] is False
    assert proof["result"]["theorem_complete"] is False
    assert proof["remaining_root_cut_set"] == GRAPH_CUT
    assert validation["accepted_closed_obligation_ids"] == []
    assert validation["result"]["root_closed"] is False
    assert validation["result"]["audit_complete"] is False
    assert validation["result"]["theorem_complete"] is False
    for gate in (
        "complete_transitive_provenance_gate",
        "complete_transitive_tcb_gate",
        "hermetic_release_gate",
        "independent_distinct_runner_gate",
    ):
        assert validation["result"][gate] == "fail_closed", gate

    assert decision["verdict"] == receipt["result"]["verdict"] == "blocked"
    assert decision["lifecycle_before"] == decision["lifecycle_after"] == "planned"
    assert decision["root_vector_before"] == decision["root_vector_after"] == VECTOR
    assert receipt["result"]["root_vector_before"] == VECTOR
    assert receipt["result"]["root_vector_after"] == VECTOR
    assert decision["audit_complete"] is decision["theorem_complete"] is False
    assert receipt["result"]["audit_complete"] is False
    assert receipt["result"]["theorem_complete"] is False
    assert decision["release_accepted"] is receipt["result"]["release_accepted"] is False
    assert decision["accepted_receipt_ids"] == receipt["accepted_receipt_ids"] == []
    assert decision["first_failed_gate"]["gate_id"] == (
        "S56-10.2-DEPENDENCY-ACCEPTANCE"
    )
    assert decision["first_failed_mathematical_gate"]["gate_id"] == (
        "M0450-B-WEAKMW"
    )
    assert decision["first_failed_release_gate"]["gate_id"] == (
        "S56-RELEASE-IMMUTABLE-CLEAN-INPUT"
    )
    assert decision["next_failed_release_gate"]["gate_id"] == (
        "S56-10.6-HERMETIC-COLD-BUILD"
    )
    assert decision["authoritative_graph_remaining_root_cut_set"] == GRAPH_CUT
    assert receipt["remaining_root_cut_set"] == GRAPH_CUT
    assert decision["known_failures"] == receipt["known_failures"]
    assert decision["retry_condition"] == receipt["retry_condition"]
    assert decision["invalidation_inputs"] == receipt["invalidation_inputs"]

    reconciliation = decision["evidence_reconciliation"]
    for key in (
        "checked_unconditional_weak_mordell_weil_package_present",
        "checked_unconditional_elliptic_height_package_present",
        "accepted_exact_root_kernel_closure",
        "authoritative_graph_reconciled",
        "audit_z_accepted",
        "pinpoint_h0_review",
        "independent_r0_review",
        "complete_provenance_foundation_tcb_closure",
        "immutable_clean_release_input",
        "hermetic_cold_offline_replay",
        "sbom_license_archive_closure",
        "two_independent_signed_runner_attestations",
        "independently_implemented_minimal_release_verifier",
        "protected_ci_and_adversarial_gates",
        "deterministic_content_addressed_release_bundle",
        "master_acceptance",
    ):
        assert reconciliation[key] is False, key
    assert reconciliation["accepted_closed_obligation_ids"] == []
    remaining = "\n".join(decision["remaining_theorem_completion_gates"])
    for fragment in (
        "M0450-B-WEAKMW",
        "M0450-H-HEIGHT",
        "H0 pinpoint",
        "R0 obligation-anchored",
        "AUDIT-Z",
        "empty-cache network-denied cold build",
        "two signed attestations",
        "minimal release verifier",
        "deterministic content-addressed release bundle",
    ):
        assert fragment in remaining, fragment

    for name, expected in receipt["upstream_input_bindings"].items():
        assert name in UPSTREAM_INPUTS and sha256(HERE / name) == expected
    for name, expected in receipt["authority_input_bindings"].items():
        assert name in AUTHORITY_INPUTS and sha256(ROOT / name) == expected
    for name, expected in receipt["tool_input_bindings"].items():
        assert name in TOOL_INPUTS and sha256(LEAN_ROOT / name) == expected
    for key in (
        "recipe_id",
        "cwd",
        "argv",
        "env_allowlist",
        "timeout_seconds",
        "network_policy",
        "network_enforcement",
        "expected_exit",
        "expected_outputs",
        "covered_obligation_ids",
        "covered_declarations",
        "scope_boundary",
    ):
        assert receipt["recipe"][key] == spec[key], key

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by|extern)\b|"
        r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
        r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
        r"(?:axiom|constant|opaque|unsafe)\b",
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
        assert prohibited.search(source) is None, f"prohibited construct in {name}"

    manifest = load(LEAN_ROOT / "lake-manifest.json")
    mathlib_entry = next(row for row in manifest["packages"] if row["name"] == "mathlib")
    assert mathlib_entry["rev"] == MATHLIB_REVISION
    assert MATHLIB.resolve().is_dir(), "pinned mathlib artifact is unavailable"
    assert git("rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert git("status", "--porcelain=v1", cwd=MATHLIB) == ""

    replay = run(
        ["python3", "-B", str(HERE / "check_validation.py")], timeout=360
    ).stdout
    assert "PASS THM-M-0450 narrow validation" in replay
    assert "root open: weak Mordell-Weil and elliptic height packages remain unproved" in replay
    assert "blocked: proof master acceptance, cold empty-cache release replay" in replay
    assert git("status", "--porcelain=v1", cwd=MATHLIB) == ""

    assert set(packet) == {
        "item_id",
        "changed_paths",
        "commands",
        "output_summary",
        "base_revision",
        "known_failures",
        "state",
    }
    assert packet["item_id"] == ITEM and packet["state"] == "[_]"
    assert packet["base_revision"] == BASE_REVISION
    assert set(packet["changed_paths"]) == CHANGED_PATHS
    assert packet["known_failures"] == decision["known_failures"]
    assert receipt["changed_paths"] == sorted(CHANGED_PATHS)

    status = git("status", "--short", "--untracked-files=all")
    actual_changes = {
        line[3:]
        for line in status.splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual_changes == CHANGED_PATHS, sorted(actual_changes)
    for relative in CHANGED_PATHS:
        assert_text_hygiene(ROOT / relative)

    print("PASS S56-M-0450-RELEASE reconciliation")
    print("verdict=blocked lifecycle=planned recorded_root_vector=H1/M3/R3")
    print("root_closed=false audit_complete=false theorem_complete=false")
    print("first_failed_gate=S56-10.2-DEPENDENCY-ACCEPTANCE")
    print("first_mathematical_gap=M0450-B-WEAKMW and M0450-H-HEIGHT")
    print("next_release_gate=S56-10.6-HERMETIC-COLD-BUILD")


if __name__ == "__main__":
    main()
