#!/usr/bin/env python3
"""Fail-closed release reconciliation for S56-M-0626-RELEASE."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0626"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM = "S56-M-0626-RELEASE"
THEOREM = "THM-M-0626"
BASE_REVISION = "f023dbc3411d83201065d1a1156d7406b81135d4"
BASE_TREE = "3b3a73ec19293a2a9b8d9c7e67f0d25da2a511b4"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
EXPECTED_INPUTS = {
    "Statement.lean": "eb03b777ac803b993a4787a8b58bd3f8f132218bda961bec4b4d1445a88bcca6",
    "ObligationTree.lean": "8fbab093179985a82443e342fc90b172a9341ce90b3b6784a325aa3a0be6da3c",
    "Proof.lean": "218bc7aa1465996a3edb8aea41bd0598f48f1f432c3737396803e57c502ef115",
    "Validation.lean": "c998787b09a37730cebb47e18c39aac1deb634ed92164a3cd493e42956f37d41",
    "statement.json": "4fea5d02ece498fda1908baa03b88b1fc3a6a7c6efec4ef6940f069b66519c26",
    "anchor-audit.json": "007066e76f0bfde71bfcbecafa34d0ffc6d00808037a8a91394a5b680abaddc8",
    "obligation-registry.json": "9d2b1ee334d5403dce7cf9c0c435dc852808ab09f06c1c37a9c73c3450e6eef0",
    "typed-graphs.json": "b92113c2bdc30f9919ae968efcf7c13e52947a0c61792fc938aa94528413189a",
    "proof-receipt.json": "a4c10934c7e3697b32057216d21aab4aa4719dcdea3c5d317bc9a23cfd73560d",
    "validation-spec.json": "406bfbfe7779e69f4314223094bb1e6e458e84332e096cac491a8a6fbda480bc",
    "validation-receipt.json": "11ada21d656ddf6deb28fb316147ad6af27f3915c5b3133d4d2f2c77f2062a18",
    "instance.json": "928a0578538c75dbe48067defe2351d9f000085073f7f868a250d92d3f1a6db5",
    "task-dag.json": "ee92bfb8b39e6d50f6ce30b19a49736aea6290a5aecd4e5e97c8e7824f20fc2b",
    "check_proof.sh": "af3792e3547a6a23847a77537a06298cc14b816966df36a070b4c8b3be688396",
}
EXPECTED_TOOL_INPUTS = {
    "lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/README.md",
    f"Stage1_Instances/{THEOREM}/check_release.py",
    f"Stage1_Instances/{THEOREM}/release-decision.json",
    f"Stage1_Instances/{THEOREM}/release-receipt.json",
    f"Stage1_Instances/{THEOREM}/release-spec.json",
    f"Stage1_Instances/{THEOREM}/release-validation.md",
}


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict), path
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(argv: list[str], *, cwd: Path = ROOT) -> str:
    result = subprocess.run(
        argv,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=180,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(f"command failed ({result.returncode}): {argv!r}\n{result.stdout}")
    return result.stdout


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["git", *args], cwd=cwd).strip()


def without_comments(source: str) -> str:
    source = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
    return re.sub(r"--.*$", "", source, flags=re.MULTILINE)


def assert_axioms(output: str, declaration: str) -> None:
    no_axioms = f"'{declaration}' does not depend on any axioms" in output
    match = re.search(
        re.escape(f"'{declaration}' depends on axioms: [") + r"(.*?)]",
        output,
        re.DOTALL,
    )
    assert no_axioms or match is not None, declaration
    if match:
        observed = {part.strip() for part in match.group(1).split(",") if part.strip()}
        assert observed <= EXPECTED_AXIOMS, (declaration, observed)


def replay_lean() -> None:
    output = run(["bash", str(HERE / "check_proof.sh")])
    declarations = (
        "IsPreconnected.image",
        "IsConnected.image",
        "Stage1Instances.THM_M_0626.Proof.relativePreimages",
        "Stage1Instances.THM_M_0626.Proof.imageCoverPullback",
        "Stage1Instances.THM_M_0626.Proof.imageHitPullback",
        "Stage1Instances.THM_M_0626.Proof.sourceIntersection",
        "Stage1Instances.THM_M_0626.Proof.intersectionPushforward",
        "Stage1Instances.THM_M_0626.Proof.separationEngine",
        "Stage1Instances.THM_M_0626.Proof.imagePreconnected",
        "Stage1Instances.THM_M_0626.Proof.imageNonempty",
        "Stage1Instances.THM_M_0626.Proof.localConnectedImage_components",
        "Stage1Instances.THM_M_0626.Proof.localConnectedImage_mathlib",
        "Stage1Instances.THM_M_0626.Proof.connectedImage",
        "Stage1Instances.THM_M_0626.Proof.connectedImage_via_components",
        "Stage1Instances.THM_M_0626.Proof.connectedImage_via_exactAssembly",
    )
    for declaration in declarations:
        assert_axioms(output, declaration)
    assert output.count("Declarations are sorry-free!") == len(declarations)


def main() -> None:
    decision = load(HERE / "release-decision.json")
    receipt = load(HERE / "release-receipt.json")
    spec = load(HERE / "release-spec.json")
    validation = load(HERE / "validation-receipt.json")
    proof = load(HERE / "proof-receipt.json")
    instance = load(HERE / "instance.json")
    graphs = load(HERE / "typed-graphs.json")
    local_dag = load(HERE / "task-dag.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    targets = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 1320
    assert target["lifecycle_mode"] == "planned" and target["theorem_complete"] is False
    assert target["baseline"] == "L0" and target["rework_required"] is True

    release_item = next(row for row in execution["items"] if row["id"] == ITEM)
    validation_item = next(
        row for row in execution["items"] if row["id"] == "S56-M-0626-VALIDATION"
    )
    assert release_item == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 1320,
        "phase": "release",
        "layer": 6,
        "state": "[ ]",
        "depends_on": ["S56-M-0626-VALIDATION"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Reconcile evidence and decide the exact theorem-completion verdict.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    assert validation_item["state"] == "[_]"
    local_release = next(row for row in local_dag["tasks"] if row["id"] == ITEM)
    assert local_release["state"] == "open"

    for name, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"reconciled input drifted: {name}"
    for name, expected in EXPECTED_TOOL_INPUTS.items():
        assert sha256(LEAN_ROOT / name) == expected, f"tool input drifted: {name}"
    assert decision["reconciled_inputs"] == EXPECTED_INPUTS

    assert decision["item_id"] == receipt["item_id"] == ITEM
    assert decision["theorem_id"] == receipt["theorem_id"] == THEOREM
    assert decision["intent"] == "release"
    assert decision["decision_support"] == "provisional_worker_selftest"
    assert decision["base_revision"] == receipt["base_revision"] == BASE_REVISION
    assert decision["base_tree"] == receipt["base_tree"] == BASE_TREE
    dependency = decision["dependency"]
    assert dependency["item_id"] == validation["item_id"] == "S56-M-0626-VALIDATION"
    assert dependency["receipt_id"] == validation["receipt_id"]
    assert dependency["receipt_sha256"] == sha256(HERE / "validation-receipt.json")
    assert dependency["support_state"] == validation["support_state"]
    assert dependency["release_grade"] is validation["release_grade"] is False
    assert dependency["accepted"] is validation["accepted"] is False
    assert dependency["master_accepted"] is False
    assert decision["release_recipe_id"] == spec["recipe_id"]
    assert decision["node_receipt_id"] == receipt["receipt_id"]
    assert decision["provisional_receipt_ids_inspected"] == [
        proof["receipt_id"], validation["receipt_id"]
    ]

    assert spec["schema_version"] == "stage1-validation-recipe/1.0"
    assert spec["item_id"] == ITEM and spec["theorem_id"] == THEOREM
    assert spec["cwd"] == "."
    assert spec["argv"] == ["python3", "-B", f"Stage1_Instances/{THEOREM}/check_release.py"]
    assert spec["env_allowlist"] == {} and spec["timeout_seconds"] == 180
    assert spec["network_policy"] == "denied" and spec["expected_exit"] == 0

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["depends_on"] == ["S56-M-0626-VALIDATION"]
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]"
    assert receipt["release_grade"] is receipt["content_addressed"] is False
    assert receipt["accepted"] is receipt["master_accepted"] is False
    for name, expected in receipt["inputs"].items():
        if name.startswith("Stage1_") or name.startswith("."):
            path = ROOT / name
        else:
            path = LEAN_ROOT / name
        assert sha256(path) == expected, f"release receipt input drifted: {name}"
    for key in (
        "recipe_id", "cwd", "argv", "env_allowlist", "timeout_seconds",
        "network_policy", "expected_exit", "covered_obligation_ids", "covered_declarations",
    ):
        assert receipt["recipe"][key] == spec[key]

    result = decision["decision"]
    assert result["verdict"] == "blocked"
    assert result["lifecycle_before"] == result["lifecycle_after"] == "planned"
    assert result["root_vector_before"] == result["root_vector_after"] == ["H1", "M3", "R4"]
    assert result["audit_complete"] is result["theorem_complete"] is False
    assert result["audit_z"] == result["theorem_z"] == "blocked"
    assert result["release_accepted"] is False
    assert decision["accepted_receipt_ids"] == []
    assert result["first_failed_gate"]["gate_id"] == "S56-10.2-DEPENDENCY-ACCEPTANCE"
    assert result["first_failed_release_gate"]["gate_id"] == "S56-10.6-HERMETIC-COLD-BUILD"
    receipt_result = receipt["result"]
    assert receipt_result["exit_code"] == 0 and receipt_result["verdict"] == "blocked"
    assert receipt_result["root_vector_before"] == receipt_result["root_vector_after"] == ["H1", "M3", "R4"]
    assert receipt_result["audit_complete"] is receipt_result["theorem_complete"] is False
    assert receipt_result["accepted_receipt_ids"] == []
    assert receipt_result["first_failed_gate"] == "S56-10.2-DEPENDENCY-ACCEPTANCE"
    assert receipt_result["first_failed_release_gate"] == "S56-10.6-HERMETIC-COLD-BUILD"
    assert receipt["known_failures"] == decision["known_failures"]
    assert set(receipt["changed_paths"]) == set(decision["changed_paths"]) == CHANGED_PATHS

    reconciliation = decision["evidence_reconciliation"]
    assert reconciliation["exact_root_kernel_replay"].startswith("provisional_pass")
    assert reconciliation["accepted_root_vector"] == ["H1", "M3", "R4"]
    assert reconciliation["accepted_closed_obligations"] == []
    for key in (
        "accepted_exact_root_kernel_closure", "authoritative_graph_reconciled",
        "audit_z_accepted", "pinpoint_h0_independent_review", "independent_r0_review",
        "complete_provenance_foundation_tcb_closure", "hermetic_cold_offline_replay",
        "sbom_license_archive_closure", "independent_clean_runner_attestations",
        "independently_implemented_minimal_verifier", "protected_ci_and_mutation_evidence",
        "deterministic_release_bundle", "master_acceptance",
    ):
        assert reconciliation[key] is False, key

    assert instance["lifecycle"] == "planned"
    assert instance["root_vector"] == {"H": "H1", "M": "M3", "R": "R4"}
    assert instance["accepted_receipt_ids"] == []
    assert instance["audit_complete"] is instance["theorem_complete"] is False
    boundary = graphs["closure_boundary"]
    assert boundary["root_closed"] is False and boundary["root_machine_debt"] == "M3"
    assert boundary["accepted_closed_obligations"] == []
    assert boundary["audit_complete"] is boundary["theorem_complete"] is False
    assert proof["accepted"] is False and proof["result"]["root_kernel_closed"] is True
    assert validation["accepted"] is validation["release_grade"] is False
    assert validation["result"]["exact_root_kernel_closed"] is True
    assert validation["result"]["accepted_root_machine_debt"] == "M3"

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by|extern)\b|"
        r"^[ \t]*(?:axiom|constant|opaque|unsafe)\b",
        re.MULTILINE,
    )
    for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
        assert prohibited.search(without_comments((HERE / name).read_text(encoding="utf-8"))) is None

    manifest = load(LEAN_ROOT / "lake-manifest.json")
    mathlib_entry = next(row for row in manifest["packages"] if row["name"] == "mathlib")
    assert mathlib_entry["rev"] == MATHLIB_REVISION
    assert MATHLIB.resolve().is_dir(), "pinned mathlib artifact is unavailable"
    assert git("rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert git("status", "--porcelain=v1", cwd=MATHLIB) == ""
    replay_lean()

    assert set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert packet["item_id"] == ITEM and packet["state"] == "[_]"
    assert packet["base_revision"] == BASE_REVISION
    assert set(packet["changed_paths"]) == CHANGED_PATHS
    assert packet["known_failures"] == decision["known_failures"]
    status = run(["git", "status", "--short", "--untracked-files=all"])
    actual_changed = {
        line[3:] for line in status.splitlines() if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual_changed == CHANGED_PATHS, (actual_changed, CHANGED_PATHS)

    readme = (HERE / "README.md").read_text(encoding="utf-8")
    handoff = (HERE / "release-validation.md").read_text(encoding="utf-8")
    for public in (readme, handoff):
        for fragment in ("`blocked`", "`[H1, M3, R4]`", "`AUDIT-Z`", "`THEOREM-Z`"):
            assert fragment in public, fragment
    for relative in CHANGED_PATHS:
        data = (ROOT / relative).read_bytes()
        assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())

    print("PASS release inputs: target, DAG dependency, receipts, graph, and hashes agree")
    print("PASS current Lean replay: exact root and component reconstruction are sorry-free")
    print("PASS fail-closed state: lifecycle planned; accepted root H1/M3/R4; accepted receipts 0")
    print("BLOCKED S56-10.2-DEPENDENCY-ACCEPTANCE: validation is provisional and unaccepted")
    print("BLOCKED S56-10.6-HERMETIC-COLD-BUILD and independent release gates")
    print("verdict=blocked audit_complete=false theorem_complete=false")


if __name__ == "__main__":
    main()
