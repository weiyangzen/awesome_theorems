#!/usr/bin/env python3
"""Fail-closed release reconciliation for S56-M-0168-RELEASE."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import time


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0168"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM = "S56-M-0168-RELEASE"
THEOREM = "THM-M-0168"
BASE_REVISION = "8714972d4cf7ae256a92b9e35032c9df1bf5745c"
BASE_TREE = "080d14e14102a733c6992aa0644e3c65d755e91b"
VALIDATION_BASE = "7505614b75de56cf10bbd196a4aaa0ca2a117064"
EXPRESSION_SHA256 = "b5cef8a8bb3b5505be6670f226315884282c53bb0040c30345f4fb0dc33254f5"
DENOMINATOR_SHA256 = "170699112c956a2921b831b9e1bb9edbbd627ece6922dda7ab1e43e4d6d389b1"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_ORIGIN = "https://github.com/leanprover-community/mathlib4.git"
MATHLIB_LICENSE_SHA256 = "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
INVENTORY_IDS = [
    "M0168-ROOT",
    "M0168-S-INTERFACE",
    "M0168-C-GRAPH",
    "M0168-N-PDE-MINIMAL",
    "M0168-L-STABILITY",
    "M0168-C-CUTOFF",
    "M0168-L-CURVATURE",
    "M0168-L-DERIVATIVE-RIGIDITY",
    "M0168-T-INTEGRATE",
    "M0168-X-SOURCE",
    "M0168-X-TRUST",
]
FROZEN_CUT = [
    "M0168-C-GRAPH",
    "M0168-N-PDE-MINIMAL",
    "M0168-L-STABILITY",
    "M0168-C-CUTOFF",
    "M0168-L-CURVATURE",
    "M0168-L-DERIVATIVE-RIGIDITY",
    "M0168-T-INTEGRATE",
]
OPEN_ROOT_CUT = FROZEN_CUT[:-1]
EXPECTED_INPUTS = {
    "README.md": "d946a1b2160998cb4b14faeee05e2efeb541b5cb34a8b032ddad616b0a08b549",
    "Statement.lean": "5e773260e93f29c5da263e749b8bd5208a7b61e344d45b588ad9cda65d311a78",
    "ObligationTree.lean": "642153a1f88af5d71a954b417b136fd95d1eaf82b8d1fdf176d60b3ace3bf24e",
    "AnchorAudit.lean": "66761bccebfce4e7655321b4d0128e8252f07b7c227d196839ff30c0972fdfb1",
    "Proof.lean": "85c6b4a484d026ce83cee32fbd449f724e3a501fc37f33c49dc05a094b0cf5db",
    "Validation.lean": "27e674bcf28dcd9992b9404237a54907541ce243fd8af6b5a9e336ae640f3fd4",
    "instance.json": "4333aea30e350687a643e027b5f2ab570e5016ba00c722a3d55adbf2d05a4268",
    "statement.json": "390945f4610500c015a125fc307ed9260cd66d756524c5ebbb9b3b99804f7d6f",
    "anchor-audit.json": "f29dd21045e7c2fdf86bb623ab5188254077e5e22b0baa0fa803a18151d4f5b7",
    "obligation-registry.json": "883e0c0a98c6d3b6e5e77adb9c5fb376c87f043dd7b80b4e882cbdb0045ed9ba",
    "typed-graphs.json": "1e8ac1d8a5906eccbd79a35b43fad6e89ee571fa4ee0bc5aa0e6b08894dcac41",
    "task-dag.json": "ed4f6447ff9458943fea6188b8a7a810af553bd9203b7b7316c89e2d1e54e2e4",
    "proof-receipt.json": "23752dfc3c852f1cc36dd990a08bf7a69844e6879b715bd8a0bc6c17d3fe99e3",
    "validation-receipt.json": "ef6397a8a90ea9713e5bae8c776da68916446046e7583b937f45b26360479b5d",
    "validation-spec.json": "a496ca5a94833b78aa7643b93fd020d16a2f2d9ea9d0e9d3ee2e09849e01ea68",
    "validation-blocker.json": "dbcb6b52ce6e1cc47f30b6f1b7e81753acfc4d41081c43e8fd1948436190f4af",
    "source-statement-crosswalk.md": "5bbb714424a41fe2fb565557b48c6d1eac40390c4689ffd28b03c14df05595f4",
    "proof-validation.md": "70af7167ae544e05be46347eb69d49cf04472c2c37eaa5286eafe633b7862e34",
    "validation-phase.md": "900ce2e01f65bd4ebafc7acfbe1dc94e61f0e6c590b99cee543771e50480a77e",
    "check_proof.sh": "48d9c087684e32aed49a51d9da25f8aad4103bee478d6db3d9eb6fe2518e1a0b",
    "check_validation.py": "2f90ed1b130e23c3c2105aeca1a22e81c0fbdb12b0d219ae34252e4dcfbf8d40",
}
EXPECTED_AUTHORITY_INPUTS = {
    "Docs/Stage1_Blueprint_rev-5.6.md": "e204dde7031f713a5c9cca94577b8ded0a13b1afdaf9ffe8bb5e8c5284aa9315",
    "Docs/Stage1_Targets_rev-5.6.json": "02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c",
    "Docs/Stage1_Execution_DAG_rev-5.6.json": "5b36f715a42bd87b5ec928b41b51186727c0215b8721481aa9d1a04779df341e",
    "Docs/Blueprint_Guidelines.md": "a06c07b5ca1b270b4935ad3dab893e9a0e078c29c8da2ef9dca1e71193310535",
    "skills/execute-stage1-rev56/SKILL.md": "26d47a66c6535feabb8bbf1051fd55d76a53fe761f4b3d953f86b97ec86152b8",
    "Formalizations/Lean/lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "Formalizations/Lean/lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
EXPECTED_RELEASE_OUTPUTS = {
    "release-spec.json": "ac9cf3452e7b63031a1cc2741a61ceaf4f9836c39eee7b5575ddba40243881a4",
    "release-decision.json": "d0fc1db6a8239d9f7cadda7511bdc344374b05372eec1fdd8cb5e706e83742d0",
    "release-validation.md": "62ddbc2c072d7ae84edbdff990a093f8d81fba972d3c1d8d3d243a4de968bb43",
}
RELEASE_FILES = (*EXPECTED_RELEASE_OUTPUTS, "release-receipt.json")
SUMMARY_LINES = [
    "PASS release reconciliation: target, DAG, receipts, registry, graphs, and hashes agree",
    "PASS narrow Lean replay: exact statement, conditional composition, and affine-integration body are sorry-free at trust zero",
    "BLOCKED S56-10.2-DEPENDENCY-ACCEPTANCE: validation is provisional and not master accepted",
    "BLOCKED exact Bernstein root M2: six required obligations remain open",
    "BLOCKED AUDIT-Z and THEOREM-Z: source/readability, trust, hermetic, and independent gates remain open",
    "verdict=blocked audit_complete=false theorem_complete=false accepted_receipts=0",
]
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/check_release.py",
    *(f"Stage1_Instances/{THEOREM}/{name}" for name in RELEASE_FILES),
}
STARTED = time.monotonic()
TIMEOUT_SECONDS = 900.0


if sys.flags.optimize:
    raise SystemExit("release check failed: Python optimization disables assertions")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


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


def run(argv: list[str], *, cwd: Path = ROOT, timeout: float | None = None) -> str:
    remaining = TIMEOUT_SECONDS - (time.monotonic() - STARTED)
    assert remaining > 0, "release recipe exceeded its wall-clock bound"
    result = subprocess.run(
        argv,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=min(remaining, timeout) if timeout is not None else remaining,
        check=False,
    )
    if result.returncode:
        raise RuntimeError(f"command failed ({result.returncode}): {argv!r}\n{result.stdout}")
    return result.stdout


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["/usr/bin/git", *args], cwd=cwd, timeout=60).strip()


def assert_text_hygiene(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())


def code_without_comments_and_strings(source: str) -> str:
    output: list[str] = []
    depth = 0
    index = 0
    in_string = False
    while index < len(source):
        if not in_string and source.startswith("/-", index):
            depth += 1
            output.extend("  ")
            index += 2
        elif depth and source.startswith("-/", index):
            depth -= 1
            output.extend("  ")
            index += 2
        elif depth:
            output.append("\n" if source[index] == "\n" else " ")
            index += 1
        elif not in_string and source.startswith("--", index):
            end = source.find("\n", index)
            end = len(source) if end < 0 else end
            output.extend(" " * (end - index))
            index = end
        elif source[index] == '"':
            in_string = not in_string
            output.append(" ")
            index += 1
        elif in_string:
            if source[index] == "\\" and index + 1 < len(source):
                output.extend("  ")
                index += 2
            else:
                output.append("\n" if source[index] == "\n" else " ")
                index += 1
        else:
            output.append(source[index])
            index += 1
    assert depth == 0 and not in_string, "unterminated Lean comment or string"
    return "".join(output)


def main() -> None:
    decision = load(HERE / "release-decision.json")
    receipt = load(HERE / "release-receipt.json")
    spec = load(HERE / "release-spec.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")
    instance = load(HERE / "instance.json")
    statement = load(HERE / "statement.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    local_tasks = load(HERE / "task-dag.json")
    proof = load(HERE / "proof-receipt.json")
    validation = load(HERE / "validation-receipt.json")
    targets = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 665 and target["baseline"] == "L0"
    assert target["lifecycle_mode"] == instance["lifecycle"] == "planned"
    assert target["rework_required"] is True and target["theorem_complete"] is False
    assert instance["theorem_complete"] is False and instance["accepted_proof_state"] == []

    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 665,
        "phase": "release",
        "layer": 6,
        "state": "[ ]",
        "depends_on": ["S56-M-0168-VALIDATION"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Reconcile evidence and decide the exact theorem-completion verdict.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    predecessor = next(
        row for row in execution["items"] if row["id"] == "S56-M-0168-VALIDATION"
    )
    assert predecessor["state"] == "[_]" and predecessor["attempts"] >= 1
    assert local_tasks["accepted_states"] == []
    assert any(row["id"] == ITEM and row["state"] == "open" for row in local_tasks["tasks"])

    for name, digest in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == digest, f"reconciled input drifted: {name}"
    for relative, digest in EXPECTED_AUTHORITY_INPUTS.items():
        assert sha256(ROOT / relative) == digest, f"authority input drifted: {relative}"
    for name, digest in EXPECTED_RELEASE_OUTPUTS.items():
        assert sha256(HERE / name) == digest, f"release output drifted: {name}"
    assert receipt["input_bindings"] == {
        **{f"Stage1_Instances/{THEOREM}/{name}": digest for name, digest in EXPECTED_INPUTS.items()},
        **EXPECTED_AUTHORITY_INPUTS,
    }
    assert receipt["release_output_bindings"] == {
        f"Stage1_Instances/{THEOREM}/{name}": digest
        for name, digest in EXPECTED_RELEASE_OUTPUTS.items()
    } | {f"Stage1_Instances/{THEOREM}/check_release.py": sha256(Path(__file__).resolve())}

    formal = statement["canonical_formal_target"]
    assert formal["declaration_or_expression"] == "Stage1Instances.THM_M_0168.BernsteinMinimalGraphTarget"
    assert formal["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert instance["root_vector"] == {"H": "H1", "M": "M4", "R": "R4"}
    assert instance["audit_complete"] is instance["theorem_complete"] is False
    obligations = {row["obligation_id"]: row for row in registry["obligations"]}
    assert list(obligations) == INVENTORY_IDS
    assert registry["canonical_root_expression_sha256"] == EXPRESSION_SHA256
    denominator = hashlib.sha256(json.dumps(
        graphs["coverage_denominators"], sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    assert denominator == DENOMINATOR_SHA256
    assert graphs["coverage_denominators"]["canonical_obligations"] == INVENTORY_IDS
    assert graphs["root_cut_set"] == FROZEN_CUT and graphs["closure_metrics_observed"] is False
    assert obligations["M0168-ROOT"]["machine_debt"] == "M2"
    assert obligations["M0168-T-INTEGRATE"]["machine_debt"] == "M4"
    assert all(row["evidence_ids"] == [] for row in obligations.values())

    assert proof["accepted"] is False and proof["support_state"] == "provisional_worker_selftest"
    assert proof["provisionally_closed_obligation_ids"] == ["M0168-T-INTEGRATE"]
    assert proof["accepted_closed_obligation_ids"] == []
    assert proof["result"]["root_kernel_closed"] is False
    assert proof["remaining_root_cut_set"] == OPEN_ROOT_CUT
    assert set(proof["result"]["axioms"]) == EXPECTED_AXIOMS

    assert validation["base_revision"] == VALIDATION_BASE
    assert validation["accepted"] is validation["release_grade"] is False
    assert validation["support_state"] == "provisional_worker_selftest"
    assert validation["result"]["root_kernel_closed"] is False
    assert validation["result"]["validation_complete"] is False
    assert validation["result"]["audit_complete"] is validation["result"]["theorem_complete"] is False
    assert validation["accepted_closed_obligation_ids"] == []
    assert validation["remaining_root_cut_set"] == OPEN_ROOT_CUT
    assert sha256(HERE / "validation-receipt.json") == decision["dependency"]["receipt_sha256"]
    assert decision["dependency"]["accepted"] is decision["dependency"]["release_grade"] is False
    assert decision["dependency"]["master_accepted"] is False

    result = decision["decision"]
    assert decision["item_id"] == ITEM and decision["theorem_id"] == THEOREM
    assert decision["base_revision"] == BASE_REVISION and decision["base_tree"] == BASE_TREE
    assert decision["proposed_state"] == "[_]" and decision["release_grade"] is False
    assert decision["accepted_receipt_ids"] == []
    assert result["verdict"] == "blocked"
    assert result["lifecycle_before"] == result["lifecycle_after"] == "planned"
    assert result["root_vector_before"] == result["root_vector_after"] == ["H1", "M4", "R4"]
    assert result["audit_complete"] is result["theorem_complete"] is False
    assert result["audit_z"] == result["theorem_z"] == "blocked"
    assert result["release_accepted"] is False
    assert result["first_failed_gate"]["gate_id"] == "S56-10.2-DEPENDENCY-ACCEPTANCE"
    assert result["first_failed_audit_gate"]["gate_id"] == (
        "S56-AUDIT-FROZEN-INVENTORY-SOURCE-BOUNDARY-RECONCILIATION"
    )
    assert result["first_failed_theorem_gate"]["gate_id"] == "M0168-C-GRAPH"
    assert result["first_failed_release_specific_gate"]["gate_id"] == (
        "S56-RELEASE-IMMUTABLE-CLEAN-INPUT"
    )
    assert result["next_failed_release_gate"]["gate_id"] == (
        "S56-10.6-HERMETIC-COLD-EMPTY-CACHE-REPLAY"
    )
    assert result["remaining_root_cut_set"] == FROZEN_CUT
    assert result["provisional_remaining_root_cut_set"] == OPEN_ROOT_CUT
    for key in (
        "exact_root_kernel_closed",
        "authoritative_graph_reconciled",
        "pinpoint_h0_review",
        "independent_r0_review",
        "audit_z_accepted",
        "complete_provenance_foundation_tcb_closure",
        "immutable_clean_release_input",
        "hermetic_cold_offline_replay",
        "sbom_license_archive_closure",
        "independent_clean_runner_attestations",
        "independently_implemented_minimal_verifier",
        "protected_ci_and_adversarial_gates",
        "deterministic_content_addressed_release_bundle",
        "theorem_z_accepted",
        "master_acceptance",
    ):
        assert decision["evidence_reconciliation"][key] is False, key

    assert spec["item_id"] == ITEM and spec["theorem_id"] == THEOREM
    assert spec["argv"] == [
        "/usr/bin/python3", "-I", "-B", f"Stage1_Instances/{THEOREM}/check_release.py"
    ]
    assert spec["network_policy"] == "denied" and spec["expected_exit"] == 0
    assert spec["covered_obligation_ids"] == INVENTORY_IDS
    assert spec["covered_decisions"] == ["AUDIT-Z", "THEOREM-Z"]
    for key in (
        "recipe_id", "cwd", "argv", "env_allowlist", "timeout_seconds",
        "network_policy", "network_enforcement", "expected_exit",
    ):
        assert receipt["recipe"][key] == spec[key], key

    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["phase"] == receipt["intent"] == "release"
    assert receipt["depends_on"] == ["S56-M-0168-VALIDATION"]
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]"
    assert receipt["accepted"] is receipt["release_grade"] is False
    assert receipt["content_addressed_release_evidence"] is receipt["master_accepted"] is False
    assert receipt["accepted_receipt_ids"] == []
    assert receipt["canonical_obligation_ids"] == INVENTORY_IDS
    assert receipt["result"]["verdict"] == "blocked"
    assert receipt["result"]["accepted_root_closed"] is False
    assert receipt["result"]["accepted_closed_obligations"] == []
    assert receipt["result"]["remaining_root_cut_set"] == FROZEN_CUT
    assert receipt["result"]["provisional_remaining_root_cut_set"] == OPEN_ROOT_CUT
    assert receipt["result"]["audit_complete"] is receipt["result"]["theorem_complete"] is False
    assert receipt["result"]["root_vector_before"] == receipt["result"]["root_vector_after"] == [
        "H1", "M4", "R4"
    ]

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|implemented_by|native_decide|run_tac|oracle)\b|"
        r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
        r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
        r"(?:axiom|constant|opaque|unsafe|extern)\b",
        re.MULTILINE,
    )
    for name in ("Statement.lean", "ObligationTree.lean", "AnchorAudit.lean", "Proof.lean", "Validation.lean"):
        clean = code_without_comments_and_strings((HERE / name).read_text(encoding="utf-8"))
        assert prohibited.search(clean) is None, f"prohibited proof device: {name}"

    assert (LEAN_ROOT / ".lake").is_symlink()
    assert git("rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert git("remote", "get-url", "origin", cwd=MATHLIB) == MATHLIB_ORIGIN
    assert git("status", "--porcelain=v1", "--untracked-files=all", cwd=MATHLIB) == ""
    assert sha256(MATHLIB / "LICENSE") == MATHLIB_LICENSE_SHA256

    proof_output = run(["/usr/bin/bash", str(HERE / "check_proof.sh")])
    assert "PASS THM-M-0168 isolated proof replay" in proof_output
    assert "closed child: M0168-T-INTEGRATE; root remains open M2" in proof_output

    assert set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert packet["item_id"] == ITEM and packet["base_revision"] == BASE_REVISION
    assert packet["state"] == "[_]"
    assert set(packet["changed_paths"]) == set(receipt["changed_paths"]) == CHANGED_PATHS
    assert packet["commands"] == receipt["commands_and_results"]
    assert packet["output_summary"] == receipt["output_summary"] == SUMMARY_LINES
    assert packet["known_failures"] == decision["known_failures"] == receipt["known_failures"]

    status = git("status", "--short", "--untracked-files=all")
    actual_changes = {
        line[3:] for line in status.splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual_changes == CHANGED_PATHS, (actual_changes, CHANGED_PATHS)
    for relative in CHANGED_PATHS:
        assert_text_hygiene(ROOT / relative)
    for name in RELEASE_FILES:
        text = (HERE / name).read_text(encoding="utf-8")
        assert "/home/" not in text and ".cron/" not in text
        assert "theorem_complete=true" not in text

    print("\n".join(SUMMARY_LINES))


if __name__ == "__main__":
    main()
