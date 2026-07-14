#!/usr/bin/env python3
"""Fail-closed release reconciliation for S56-M-1246-RELEASE."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import time


if not __debug__:
    raise SystemExit("check_release.py must run without Python optimization")


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-1246"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM = "S56-M-1246-RELEASE"
THEOREM = "THM-M-1246"
BASE_REVISION = "f2f2e5f8994202b6e632a4270a1ce1f4a2c49434"
BASE_TREE = "15f8a42d4745fe3c7d55dd91e8aa269b557eac32"
EXPRESSION_SHA256 = "07f1c030325dfe8d02e99a0af1a00c5241a312e6195aa4a9e2967822960048f1"
DENOMINATOR_SHA256 = "dd6e6ca1fc734ea8f477095e77a99601a3387cd914de7e599c9343b874ae2d6d"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
EXPECTED_INPUTS = {
    "intake.json": "1560bd2fd7b228380bd7683a1cd535136aff52494a4919b1ec813437e2121a81",
    "statement.json": "48ca0afb1db7651526500b03e47c73e25ceae54bc6f2b0a288c454ee6829d237",
    "source_statement_crosswalk.md": "ebfc9069828220031f841ac2f979955ef2cb623dbd9b21273516a9448962927f",
    "anchor-audit.json": "5688f27403172094e3ba47a076310f73f1677bc09d7cfb504a032bc7c79f035f",
    "obligation-registry.json": "55abd985d8dae0c29fa16cde7df11f83979cda152bea30bc9df5a1143ab2fd2e",
    "typed-graphs.json": "3af40d84c9b5a91b33b2de6b12a11d65e2b5dab1f98d9a563b770d56ad1e4920",
    "Statement.lean": "0388e86c4661e59d1cebd5d54c854bad1184b6b7d2ae2a83e12fc3c3dabddf41",
    "ObligationTree.lean": "794d7584a46ae138d071b1958bd1fa82da1fa11db763f696e16f6b4a14e1aac6",
    "RegularizedIBP.lean": "7af35645a8afbc1e61f3bf44b8cdabb7ad244097cd6a7c27829e9876adf84936",
    "SharpEstimate.lean": "6f839807e9c76117edccc734fa79f99f68b3edb86211be78222a1ec1e48a9093",
    "HardyLimit.lean": "2cb9fea444cc720976838b285c06026b8a6a60ba5c9e9e9c413a46771bb59b53",
    "Proof.lean": "fa5b3bf6cb5dbd63f597f0428d9d490baccb5c41005cb6d2145c0a6ebc39388b",
    "ProofAudit.lean": "253e11a86327d30feee6402d37b47e40e41574596301da1d08964f7a1ab01f5b",
    "Validation.lean": "488e771788870293aed54f5a9bd6c6b847856f9470d903400b93cd2f3b49af64",
    "proof-blocker.json": "25a5a1f3dcb4e5c2f48d0f49dca089a3db6a20bc246732c7a3bc74d38623867a",
    "proof-receipt.json": "34b95ea1376a363cee1dc6d1a4e6a28f14332fda3c93abe261238beba30e3d87",
    "validation-spec.json": "65751e8dd3fb838345597f80e66eee359cbdc53124d25d797ff76af1201d148f",
    "validation-receipt.json": "1644eb49e8b311bb2983374cce8a3610563b91f83b9690ef1afcea77df219734",
    "check_validation.sh": "8daeb99f8a64d8cbb650b29b2a59f9cfd861d1449c5a179b7acfbe96daeb5edd",
}
EXPECTED_AUTHORITY = {
    "Docs/Stage1_Targets_rev-5.6.json": "02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c",
    "Docs/Stage1_Execution_DAG_rev-5.6.json": "6ab95e85fbea9b9336c11585921ffd5dea180070521d843c2740f5e507417579",
}
EXPECTED_TOOL_INPUTS = {
    "lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
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
    "PASS THM-M-1246 release reconciliation",
    "BLOCKED dependency: S56-M-1246-VALIDATION is provisional and not master accepted",
    "AUDIT-Z=false; THEOREM-Z=false; theorem_complete=false",
    "accepted_receipt_ids=[]; lifecycle=planned; root_vector=H2/M3/R4",
)
STARTED = time.monotonic()
TIMEOUT_SECONDS = 180.0


def fail(message: str) -> None:
    raise SystemExit(f"release-decision: FAIL: {message}")


def load(path: Path) -> dict:
    def reject_duplicates(pairs: list[tuple[str, object]]) -> dict:
        value: dict[str, object] = {}
        for key, item in pairs:
            if key in value:
                fail(f"duplicate JSON key in {path}: {key}")
            value[key] = item
        return value

    value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates)
    if not isinstance(value, dict):
        fail(f"expected JSON object: {path}")
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(argv: list[str], *, cwd: Path = ROOT) -> str:
    remaining = TIMEOUT_SECONDS - (time.monotonic() - STARTED)
    if remaining <= 0:
        fail("release recipe exceeded its 180-second wall-clock bound")
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
        fail(f"command failed ({result.returncode}): {argv!r}\n{result.stdout}")
    return result.stdout


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["git", *args], cwd=cwd).strip()


def assert_text_hygiene(path: Path) -> None:
    data = path.read_bytes()
    if not data.endswith(b"\n") or b"\r" in data or b"\x00" in data:
        fail(f"invalid text encoding or final newline: {path}")
    if any(line.endswith((b" ", b"\t")) for line in data.splitlines()):
        fail(f"trailing whitespace: {path}")


def code_without_comments(source: str) -> str:
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
    if depth:
        fail("unterminated Lean block comment")
    return "".join(output)


def main() -> None:
    spec = load(HERE / "release-spec.json")
    decision = load(HERE / "release-decision.json")
    receipt = load(HERE / "release-receipt.json")
    selftest = load(ROOT / ".stage1-worker-selftest.json")
    targets = load(ROOT / "Docs" / "Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")
    statement = load(HERE / "statement.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    proof = load(HERE / "proof-receipt.json")
    validation = load(HERE / "validation-receipt.json")

    if git("rev-parse", "HEAD") != BASE_REVISION or git("rev-parse", "HEAD^{tree}") != BASE_TREE:
        fail("base repository identity drifted")
    for relative, expected in EXPECTED_AUTHORITY.items():
        if sha256(ROOT / relative) != expected:
            fail(f"authority input drifted: {relative}")
    for name, expected in EXPECTED_INPUTS.items():
        if sha256(HERE / name) != expected:
            fail(f"reconciled input drifted: {name}")
    for name, expected in EXPECTED_TOOL_INPUTS.items():
        if sha256(LEAN_ROOT / name) != expected:
            fail(f"toolchain input drifted: {name}")

    target = next((row for row in targets["targets"] if row["theorem_id"] == THEOREM), None)
    if target is None or target["execution_rank"] != 426:
        fail("target membership or execution rank drifted")
    if target["baseline"] != "L0" or target["rework_required"] is not True:
        fail("target no longer has the uniform L0/rework baseline")
    if target["lifecycle_mode"] != "planned" or target["theorem_complete"] is not False:
        fail("target authority no longer supports a blocked release")

    item = next((row for row in execution["items"] if row["id"] == ITEM), None)
    expected_item = {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 426,
        "phase": "release",
        "layer": 6,
        "state": "[ ]",
        "depends_on": ["S56-M-1246-VALIDATION"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Reconcile evidence and decide the exact theorem-completion verdict.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    if item != expected_item:
        fail("release execution item drifted")
    predecessor = next(
        (row for row in execution["items"] if row["id"] == "S56-M-1246-VALIDATION"), None
    )
    if predecessor is None or predecessor["state"] != "[_]" or predecessor["attempts"] != 1:
        fail("validation dependency is not the reconciled provisional predecessor")

    if statement["canonical_formal_target"]["elaborated_expression_sha256"] != EXPRESSION_SHA256:
        fail("canonical target expression drifted")
    if registry["denominator_sha256"] != DENOMINATOR_SHA256:
        fail("frozen obligation denominator drifted")
    if graphs["registry_denominator_sha256"] != DENOMINATOR_SHA256:
        fail("typed graph denominator drifted")
    obligation_ids = [row["obligation_id"] for row in registry["obligations"]]
    if len(obligation_ids) != len(set(obligation_ids)) or len(obligation_ids) != 15:
        fail("frozen obligation inventory drifted")
    boundary = graphs["closure_boundary"]
    if boundary != {
        "closed_obligations": ["M1246-S-DEFINITIONS", "M1246-T-ROOT-TRANSPORT"],
        "root_closed": False,
        "theorem_complete": False,
        "remaining_root_cut_set": ["M1246-T-ANALYTIC"],
        "root_machine_debt": "M3",
    }:
        fail("authoritative graph no longer supports the blocked decision")

    if proof["support_state"] != "provisional_worker_selftest" or proof["accepted"] is not False:
        fail("proof receipt support boundary drifted")
    if proof["accepted_closed_obligation_ids"] or proof["result"]["accepted_root_closed"] is not False:
        fail("proof receipt unexpectedly contains accepted closure")
    if proof["result"]["root_kernel_closed"] is not True or proof["result"]["theorem_complete"] is not False:
        fail("proof receipt kernel/completion boundary drifted")
    if proof["proof_body"]["classification"].startswith("repo_local_") is not True:
        fail("proof body is no longer classified as repo-local")

    if validation["item_id"] != "S56-M-1246-VALIDATION":
        fail("wrong validation predecessor")
    if validation["support_state"] != "provisional_worker_selftest":
        fail("validation support state drifted")
    if validation["accepted"] is not False or validation["release_grade"] is not False:
        fail("validation was falsely represented as accepted or release-grade")
    if validation["content_addressed"] is not False or validation["accepted_receipt_ids"]:
        fail("validation was falsely represented as content-addressed or accepted")
    if validation["result"]["exact_root_kernel_replay"] != "provisional_pass":
        fail("validation lost the provisional exact-root evidence")
    if validation["result"]["audit_complete"] is not False:
        fail("validation unexpectedly claims AUDIT-Z")
    if validation["result"]["theorem_complete"] is not False:
        fail("validation unexpectedly claims theorem completion")

    if spec["schema_version"] != "stage1-validation-recipe/1.0":
        fail("release recipe schema drifted")
    if spec["item_id"] != decision["item_id"] or decision["item_id"] != receipt["item_id"]:
        fail("release item identity mismatch")
    if spec["theorem_id"] != decision["theorem_id"] or decision["theorem_id"] != THEOREM:
        fail("release theorem identity mismatch")
    if spec["argv"] != ["python3", "-B", f"Stage1_Instances/{THEOREM}/check_release.py"]:
        fail("release recipe argv drifted")
    if spec["cwd"] != "." or spec["env_allowlist"] != {}:
        fail("release recipe cwd or environment drifted")
    if spec["timeout_seconds"] != 180 or spec["network_policy"] != "denied":
        fail("release recipe execution bound drifted")
    if spec["expected_exit"] != 0 or spec["expected_outputs"] != [{
        "path_or_stream": "stdout",
        "semantic_hash_policy": "exact four-line blocked release summary from the hash-bound checker",
        "semantic_sha256": "bff0b7539b2d5eb3816442779f31272ceab07c83d5d8cf73cbea2232c7bcea9c",
        "bytes": 240,
    }]:
        fail("release recipe output contract drifted")
    if spec["covered_obligation_ids"] != obligation_ids:
        fail("release recipe does not cover the frozen obligation inventory")
    for field in (
        "recipe_id", "cwd", "argv", "env_allowlist", "timeout_seconds",
        "network_policy", "network_enforcement", "expected_exit", "expected_outputs",
        "covered_obligation_ids", "covered_declarations", "scope_boundary",
    ):
        if receipt["recipe"][field] != spec[field]:
            fail(f"release receipt recipe drifted at {field}")

    if decision["base_revision"] != receipt["base_revision"] or decision["base_revision"] != BASE_REVISION:
        fail("release base revision mismatch")
    if decision["base_tree"] != receipt["base_tree"] or decision["base_tree"] != BASE_TREE:
        fail("release base tree mismatch")
    if decision["decision_id"] != receipt["decision_id"]:
        fail("release decision/receipt identity mismatch")
    if decision["verdict"] != "blocked" or receipt["result"]["verdict"] != "blocked":
        fail("open gates require a blocked release verdict")
    if decision["lifecycle_before"] != "planned" or decision["lifecycle_after"] != "planned":
        fail("blocked worker release must not advance lifecycle")
    if decision["accepted_receipt_ids"] or receipt["accepted_receipt_ids"]:
        fail("provisional evidence was represented as accepted")
    if receipt["accepted"] is not False or receipt["release_grade"] is not False:
        fail("release receipt was represented as accepted or release-grade")
    if receipt["content_addressed"] is not False or receipt["accepted_closed_obligation_ids"]:
        fail("release receipt was represented as content-addressed or closing obligations")
    if decision["terminal_decisions"] != {
        "audit_complete": False,
        "theorem_complete": False,
        "audit_z": "blocked",
        "theorem_z": "blocked",
    }:
        fail("release terminal decisions drifted")
    if decision["root_vector"]["accepted_before"] != ["H2", "M3", "R4"]:
        fail("accepted root vector before release drifted")
    if decision["root_vector"]["accepted_after"] != ["H2", "M3", "R4"]:
        fail("release silently changed the accepted root vector")
    if decision["root_vector"]["best_provisional_evidence"] != ["H2", "M0-L", "R4"]:
        fail("repo-local proof-body classification drifted")

    dependency = decision["dependency"]
    if dependency["item_id"] != validation["item_id"]:
        fail("release dependency item mismatch")
    if dependency["receipt_id"] != validation["receipt_id"]:
        fail("release dependency receipt mismatch")
    if dependency["receipt_sha256"] != sha256(HERE / "validation-receipt.json"):
        fail("release dependency receipt hash mismatch")
    if dependency["worker_projection"] != "[_]" or dependency["master_accepted"] is not False:
        fail("release dependency acceptance boundary drifted")
    if dependency["receipt_release_grade"] is not False:
        fail("release dependency was represented as release-grade")
    if dependency["receipt_content_addressed"] is not False:
        fail("release dependency was represented as content-addressed")

    if decision["first_failed_gate"]["gate_id"] != "dependency.S56-M-1246-VALIDATION.master_acceptance":
        fail("first failed node gate drifted")
    if decision["first_failed_release_gate"] != "S56-10.6-HERMETIC-COLD-BUILD":
        fail("first failed release gate drifted")
    if receipt["first_failed_gate"] != decision["first_failed_gate"]["gate_id"]:
        fail("receipt and decision first failed gates disagree")
    if receipt["first_failed_release_gate"] != decision["first_failed_release_gate"]:
        fail("receipt and decision release gates disagree")
    required_false = (
        "authoritative_graph_reconciled", "accepted_root_m0_l", "audit_z_accepted",
        "pinpoint_h0_review", "independent_r0_review",
        "accepted_provenance_foundation_tcb_closure", "immutable_clean_release_input",
        "hermetic_cold_offline_replay", "sbom_license_offline_archive_closure",
        "two_independent_signed_runner_attestations",
        "independently_implemented_minimal_release_verifier",
        "protected_ci_and_adversarial_gates",
        "deterministic_content_addressed_release_bundle", "master_acceptance",
    )
    for gate in required_false:
        if decision["evidence_reconciliation"][gate] is not False:
            fail(f"release gate was silently cleared: {gate}")
    cut = "\n".join(decision["remaining_root_cut_set"])
    for fragment in (
        "master acceptance", "typed-graph reconciliation", "AUDIT-Z", "H0 primary-source",
        "R0 node-by-node", "transitive declaration", "empty-cache network-denied cold build",
        "SBOM", "two signed attestations", "minimal release verifier",
        "adversarial fixtures", "deterministic content-addressed release bundle",
    ):
        if fragment not in cut:
            fail(f"release cut set omits {fragment!r}")

    if decision["reconciled_inputs"] != receipt["inputs"]:
        fail("decision and receipt input ledgers disagree")
    if decision["authority_inputs"] != receipt["authority_inputs"]:
        fail("decision and receipt authority ledgers disagree")
    if receipt["canonical_target"]["elaborated_expression_sha256"] != EXPRESSION_SHA256:
        fail("release receipt target fingerprint drifted")
    if receipt["canonical_target"]["registry_denominator_sha256"] != DENOMINATOR_SHA256:
        fail("release receipt denominator drifted")
    if receipt["environment"]["mathlib_revision"] != MATHLIB_REVISION:
        fail("release receipt mathlib revision drifted")
    if receipt["environment"]["mathlib_tree"] != MATHLIB_TREE:
        fail("release receipt mathlib tree drifted")
    if git("rev-parse", "HEAD", cwd=MATHLIB) != MATHLIB_REVISION:
        fail("pinned mathlib revision drifted")
    if git("rev-parse", "HEAD^{tree}", cwd=MATHLIB) != MATHLIB_TREE:
        fail("pinned mathlib tree drifted")
    if git("status", "--porcelain=v1", "--untracked-files=all", cwd=MATHLIB) != "":
        fail("pinned mathlib worktree is dirty")

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by|oracle)\b|"
        r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
        r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
        r"(?:axiom|constant|opaque|unsafe|extern)\b",
        re.MULTILINE,
    )
    for name in (
        "Statement.lean", "ObligationTree.lean", "RegularizedIBP.lean",
        "SharpEstimate.lean", "HardyLimit.lean", "Proof.lean", "ProofAudit.lean",
        "Validation.lean",
    ):
        if prohibited.search(code_without_comments((HERE / name).read_text(encoding="utf-8"))):
            fail(f"prohibited source construct in {name}")

    replay_evidence = receipt["external_lean_replay"]
    if replay_evidence != {
        "argv": ["bash", f"Stage1_Instances/{THEOREM}/check_validation.sh"],
        "exit_code": 0,
        "output_sha256": "cd4a55ba5142c53c517d1e88afde1f45804bfc067441c57aef79b369e627d4d3",
        "output_bytes": 30446,
        "recursive_sorry_reports": 6,
        "observed_axioms": ["Classical.choice", "Quot.sound", "propext"],
        "validated_on": "2026-07-15",
        "scope": "independent worker rerun plus release-worker rerun before checker finalization",
    }:
        fail("recorded Lean replay evidence drifted")
    if validation["result"]["kernel_output_sha256"] != replay_evidence["output_sha256"]:
        fail("release and validation replay digests disagree")
    if validation["result"]["kernel_output_bytes"] != replay_evidence["output_bytes"]:
        fail("release and validation replay lengths disagree")
    if validation["result"]["axiom_report_count"] != replay_evidence["recursive_sorry_reports"]:
        fail("release and validation recursive checks disagree")
    if validation["result"]["observed_axioms"] != replay_evidence["observed_axioms"]:
        fail("release and validation axiom reports disagree")
    if git("status", "--porcelain=v1", "--untracked-files=all", cwd=MATHLIB) != "":
        fail("pinned mathlib checkout is dirty after release reconciliation")

    expected_selftest_keys = {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    if set(selftest) != expected_selftest_keys:
        fail("worker self-test schema drifted")
    if selftest["item_id"] != ITEM or selftest["state"] != "[_]":
        fail("wrong worker self-test item or state")
    if selftest["base_revision"] != BASE_REVISION:
        fail("worker self-test base revision drifted")
    if set(selftest["changed_paths"]) != CHANGED_PATHS:
        fail("worker self-test changed paths drifted")
    if selftest["commands"] != receipt["commands_and_exit_codes"]:
        fail("worker self-test command ledger drifted")
    if selftest["output_summary"] != list(SUMMARY_LINES):
        fail("worker self-test output summary drifted")
    if selftest["known_failures"] != receipt["known_failures"]:
        fail("worker self-test failure ledger drifted")
    if receipt["changed_paths"] != sorted(CHANGED_PATHS):
        fail("release receipt changed paths drifted")

    public_text = "\n".join(
        (HERE / name).read_text(encoding="utf-8")
        for name in ("release-decision.json", "release-receipt.json", "release-validation.md")
    )
    if "/home/" in public_text or ".cron/" in public_text:
        fail("release artifact exposes an absolute/private automation path")
    if '"theorem_complete": true' in public_text or '"accepted": true' in public_text:
        fail("release artifact overstates acceptance or theorem completion")

    status = set(
        git(
            "status", "--porcelain=v1", "-uall", "--",
            f"Stage1_Instances/{THEOREM}", ".stage1-worker-selftest.json",
            "Formalizations/Lean/.lake",
        ).splitlines()
    )
    expected_status = {f"?? {path}" for path in CHANGED_PATHS}
    expected_status.add("?? Formalizations/Lean/.lake")
    if status != expected_status:
        fail(f"scoped worktree change set drifted: {status!r}")
    for relative in CHANGED_PATHS:
        assert_text_hygiene(ROOT / relative)

    for line in SUMMARY_LINES:
        print(line)


if __name__ == "__main__":
    main()
