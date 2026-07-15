#!/usr/bin/env python3
"""Fail-closed release reconciliation for S56-M-1023-RELEASE."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-1023"
ITEM = "S56-M-1023-RELEASE"
THEOREM = "THM-M-1023"
BASE_REVISION = "f94e9d38903a8428e13b050f044d57ef76fc65ed"
BASE_TREE = "3aa6f6cbea0f08da6762c671d71e89e864f21cd1"
TARGET_EXPRESSION = "f84253c83a8c31d9b77246bc0b3eef7715b0d0a04b707bb91cd5c329fdde1a2f"
DENOMINATOR = "d4c7d2a1d47477fc812ed85f49f768034a99424755d90cb4de202a112a80c825"
VALIDATION_RECEIPT_SHA256 = (
    "3fc4a8c6b43ce0d4d49f05aea5f1a57762d77a126a00bd34041bf935dd729faa"
)
VALIDATION_RECEIPT_ID = (
    "S56-M-1023-VALIDATION-network-isolated-20260715T083400+0800"
)
EXPECTED_AXIOMS = ["propext", "Classical.choice", "Quot.sound"]
ALL_OBLIGATIONS = [
    "M1023-ROOT",
    "M1023-S-DEFINITIONS",
    "M1023-S-BOUNDARY",
    "M1023-S-FOUNDATION",
    "M1023-N-CONVENTION",
    "M1023-F-COHERENT-ROOTS",
    "M1023-F-TRIPLET-EXISTS",
    "M1023-F-REPRESENTS",
    "M1023-F-UNIQUE",
    "M1023-T-FORWARD",
    "M1023-R-SCALE-DATA",
    "M1023-R-ROOT-MEASURE",
    "M1023-R-CONVOLUTION-POWER",
    "M1023-T-REVERSE",
    "M1023-T-ASSEMBLE",
    "M1023-X-SOURCE",
    "M1023-X-PROVENANCE",
]
ROOT_CUT = ["M1023-T-FORWARD", "M1023-T-REVERSE"]
EXPECTED_INPUTS = {
    "README.md": "917a19a1ef40f3dd563638fe9bd5dd97d5db52fc7190b9bfb023ad9c41aa4534",
    "instance.json": "b09fae7437e8524f4ceaa8ab2a9d9bdec9b41f49f25171ec235c9048067d03a5",
    "Statement.lean": "ebb29fb83091cddccb5eeeeddd8924b2b7960cff12bbdf492070780d4222e296",
    "source_statement_crosswalk.md": "367fb86d80c0b9a4a62eb1ddaaab60c6bfb2404d26cf89e23c9d4888e3dd2579",
    "AnchorAudit.lean": "b7ffe1699eb543b46525e6ff30eddbfc6bfbf490d8d17000399a05aa33ee7c37",
    "anchor-audit.json": "f58cb74240f545238d26d41a0d3f34590ec888b0532db8cd57121ea8a3deaec9",
    "obligation-registry.json": "bd0fba6bed549ab3a196f0ab5fe02f3434093226effd922b10000ab33248d6ac",
    "typed-graphs.json": "4b67e6ef2f2d04cdd4e23758fe00b7125f1b8f5e7b495657db0b9199ee51b698",
    "ObligationTree.lean": "08cbbbaad4f6ea735dcc9da0ce6f26d5782313670295c54c87b0b7115cd10985",
    "Proof.lean": "391a7e04692c213b000229339d6ed734141fc62466c06552d5fa0cd4d50579b8",
    "proof-receipt.json": "2accc37546accb0efd1c5c87c6a5324fb7d90da588335435224bb0106f10fda3",
    "Validation.lean": "4e15c9af20cfc331f7b328eaedfb6044b1ae096aeb07bca7d9eaf982244b45cc",
    "validation-spec.json": "a626b118bcaaf963ce307b9cc786f8737ca4cd4753d60e46f4956c8a4e83363d",
    "validation-receipt.json": VALIDATION_RECEIPT_SHA256,
    "validation-phase.md": "45df7553f51761735dc1eeb4f12086531995ed16e8d837daada215fae7135bc8",
    "check_validation.py": "dc277fbbc92c14fcb0281db9afd49c806c76f79ff2f515c21a03f8253326a09d",
    "check_validation.sh": "96c26d44db76d88ea56d1ac6892e59d2dae7c899f59c882bde9dd725bd3b896e",
    "vendor-manifest.json": "0e1ca71947378058abc2580f632f7f2dc656f66aec6a1c6f6478afc96610daa5",
    "VENDOR_PROVENANCE.md": "e69c50cd0bc8b99b6f73882d06072f417b5e0c37a0b40b6f6271b55fb4be5035",
    "Vendor/LICENSE": "9ccb61ce372d47010507d876144053d40f49203851663956ae8c46e469dbfe79",
}
AUTHORITY_INPUTS = {
    "Docs/Stage1_Targets_rev-5.6.json": "02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c",
    "Docs/Stage1_Execution_DAG_rev-5.6.json": "5daaf58f1a0f3d9b03a05dd2b96082d4b2ac33d113c17f731cecf3f40dcd58d9",
    "Docs/Stage1_Blueprint_rev-5.6.md": "a6401f8597fc4419e1054cab042eb5b46f06c219f614e153555cd08d8188d220",
    "Docs/Blueprint_Guidelines.md": "a06c07b5ca1b270b4935ad3dab893e9a0e078c29c8da2ef9dca1e71193310535",
    "skills/execute-stage1-rev56/SKILL.md": "26d47a66c6535feabb8bbf1051fd55d76a53fe761f4b3d953f86b97ec86152b8",
    "Formalizations/Lean/lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "Formalizations/Lean/lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/check_release.py",
    f"Stage1_Instances/{THEOREM}/release-decision.json",
    f"Stage1_Instances/{THEOREM}/release-receipt.json",
    f"Stage1_Instances/{THEOREM}/release-spec.json",
    f"Stage1_Instances/{THEOREM}/release-validation.md",
}
SUMMARY = (
    "PASS release inputs: authority, dependency receipts, registry, graph, and hashes agree\n"
    "PASS exact-root replay: network-isolated trust-zero Lean validation passed\n"
    "PASS fail-closed state: lifecycle planned; accepted vector H1/M3/R4; receipts 0\n"
    "BLOCKED S56-10.2-DEPENDENCY-ACCEPTANCE: validation is provisional and unaccepted\n"
    "BLOCKED audit/root reconciliation: late external route is absent from accepted authority\n"
    "BLOCKED release trust, cold/offline, independent-verifier, and bundle gates\n"
    "verdict=blocked audit_complete=false theorem_complete=false\n"
)
START = time.monotonic()
TIMEOUT = 3600.0


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


def run(argv: list[str], *, cwd: Path = ROOT, timeout: float | None = None) -> str:
    remaining = TIMEOUT - (time.monotonic() - START)
    require(remaining > 0, "release recipe exceeded its wall-clock bound")
    completed = subprocess.run(
        argv,
        cwd=cwd,
        env=os.environ.copy(),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=min(remaining, timeout) if timeout else remaining,
        check=False,
    )
    require(
        completed.returncode == 0,
        f"command failed ({completed.returncode}): {argv!r}\n{completed.stdout}",
    )
    return completed.stdout


def git(*args: str) -> str:
    return run(["git", *args], timeout=60).strip()


def strip_lean_comments_and_strings(source: str) -> str:
    out: list[str] = []
    i = 0
    block_depth = 0
    line_comment = False
    quoted: str | None = None
    escaped = False
    while i < len(source):
        pair = source[i:i + 2]
        char = source[i]
        if line_comment:
            out.append("\n" if char == "\n" else " ")
            line_comment = char != "\n"
            i += 1
        elif block_depth:
            if pair == "/-":
                block_depth += 1
                out.extend("  ")
                i += 2
            elif pair == "-/":
                block_depth -= 1
                out.extend("  ")
                i += 2
            else:
                out.append("\n" if char == "\n" else " ")
                i += 1
        elif quoted:
            out.append("\n" if char == "\n" else " ")
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == quoted:
                quoted = None
            i += 1
        elif pair == "/-":
            block_depth = 1
            out.extend("  ")
            i += 2
        elif pair == "--":
            line_comment = True
            out.extend("  ")
            i += 2
        elif char == '"':
            quoted = char
            out.append(" ")
            i += 1
        else:
            out.append(char)
            i += 1
    require(block_depth == 0 and quoted is None, "unterminated Lean comment/string")
    return "".join(out)


def main() -> None:
    require(not sys.flags.optimize, "optimized Python disables fail-closed checking")
    os.umask(0o022)
    os.environ.update({
        "LANG": "C.UTF-8",
        "LC_ALL": "C.UTF-8",
        "TZ": "UTC",
        "LEAN_NUM_THREADS": "1",
    })
    decision = load(HERE / "release-decision.json")
    receipt = load(HERE / "release-receipt.json")
    spec = load(HERE / "release-spec.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")
    targets = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    instance = load(HERE / "instance.json")
    anchor = load(HERE / "anchor-audit.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    proof = load(HERE / "proof-receipt.json")
    validation = load(HERE / "validation-receipt.json")
    vendor = load(HERE / "vendor-manifest.json")

    require(git("rev-parse", "HEAD") == BASE_REVISION, "base revision drifted")
    require(git("rev-parse", "HEAD^{tree}") == BASE_TREE, "base tree drifted")
    for relative, expected in EXPECTED_INPUTS.items():
        require(digest(HERE / relative) == expected, f"reconciled input drifted: {relative}")
    require(decision["reconciled_inputs"] == EXPECTED_INPUTS, "decision input map drifted")
    for relative, expected in AUTHORITY_INPUTS.items():
        require(digest(ROOT / relative) == expected, f"authority input drifted: {relative}")
    require(decision["authority_inputs"] == AUTHORITY_INPUTS, "authority map drifted")

    target = next(
        (row for row in targets["targets"] if row["theorem_id"] == THEOREM), None
    )
    require(target is not None, "target absent from manifest")
    require(target["execution_rank"] == 499, "execution rank drifted")
    require(target["baseline"] == "L0" and target["rework_required"] is True,
            "uniform L0 baseline drifted")
    require(target["legacy_artifacts_accepted"] is False, "legacy artifacts became accepted")
    require(target["lifecycle_mode"] == "planned", "target lifecycle drifted")
    require(target["theorem_complete"] is False, "manifest claims theorem completion")

    release_item = next((row for row in execution["items"] if row["id"] == ITEM), None)
    validation_item = next(
        (row for row in execution["items"] if row["id"] == "S56-M-1023-VALIDATION"),
        None,
    )
    require(release_item == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 499,
        "phase": "release",
        "layer": 6,
        "state": "[ ]",
        "depends_on": ["S56-M-1023-VALIDATION"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Reconcile evidence and decide the exact theorem-completion verdict.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }, "release execution item drifted")
    require(validation_item is not None and validation_item["state"] == "[_]",
            "validation dependency is not provisional [_]")
    require(validation_item["attempts"] == 1, "validation attempt count drifted")

    accepted_vector = {"human": "H1", "machine": "M3", "readability": "R4"}
    require(instance["lifecycle_mode"] == "planned", "instance lifecycle drifted")
    require(instance["root_vector"] == accepted_vector, "accepted vector drifted")
    require(instance["accepted_proof_state"] == [], "instance acquired proof state")
    require(instance["audit_complete"] is instance["theorem_complete"] is False,
            "instance claims terminal completion")
    require(instance["canonical_formal_target"]["elaborated_expression_hash"] ==
            f"sha256:{TARGET_EXPRESSION}", "target expression drifted")

    require(anchor["root_machine_classification"] == "M3", "anchor class drifted")
    require(anchor["terminal_result"].startswith(
        "No exact or stronger terminal Lean 4 theorem"
    ), "late discovery was silently rewritten into anchor authority")
    require(registry["root_obligation_id"] == "M1023-ROOT", "root ID drifted")
    require(registry["denominator_sha256"] == DENOMINATOR, "denominator drifted")
    require([row["obligation_id"] for row in registry["obligations"]] == ALL_OBLIGATIONS,
            "obligation inventory drifted")
    require(graphs["registry_denominator_sha256"] == DENOMINATOR,
            "graph denominator drifted")
    require({row["obligation_id"] for row in graphs["nodes"]} == set(ALL_OBLIGATIONS),
            "typed graph inventory drifted")
    require(sum(len(graph["edges"]) for graph in graphs["graphs"].values()) == 46,
            "typed edge count drifted")
    boundary = graphs["closure_boundary"]
    require(boundary["root_closed"] is boundary["audit_complete"] is
            boundary["theorem_complete"] is False, "graph claims terminal completion")
    require(boundary["remaining_root_cut_set"] == ROOT_CUT, "root cut drifted")

    require(proof["support_state"] == "provisional_worker_selftest",
            "proof support state drifted")
    require(proof["accepted"] is False and proof["proposed_state"] == "[_]",
            "proof receipt became accepted")
    require(proof["accepted_receipt_ids"] == proof["accepted_closed_obligation_ids"] == [],
            "proof grants acceptance")
    require(proof["covered_obligation_ids"] == ["M1023-ROOT"],
            "proof coverage drifted")
    require(proof["result"]["root_kernel_inhabitant_observed"] is True,
            "proof lost exact-root observation")
    require(proof["result"]["accepted_root_closed"] is False and
            proof["result"]["theorem_complete"] is False,
            "proof receipt claims accepted completion")
    require(proof["canonical_target_expression_sha256"] == TARGET_EXPRESSION,
            "proof target drifted")

    require(digest(HERE / "validation-receipt.json") == VALIDATION_RECEIPT_SHA256,
            "validation receipt bytes drifted")
    require(validation["receipt_id"] == VALIDATION_RECEIPT_ID,
            "wrong validation receipt")
    require(validation["support_state"] == "provisional_worker_selftest",
            "validation support drifted")
    require(validation["accepted"] is validation["release_grade"] is False,
            "validation became accepted or release grade")
    require(validation["accepted_closed_obligation_ids"] == [],
            "validation grants accepted closure")
    require(validation["result"]["network_isolated_lean_replay"] == "pass",
            "validation lost isolated replay")
    require(validation["result"]["accepted_root_closed"] is False and
            validation["result"]["audit_complete"] is
            validation["result"]["theorem_complete"] is False,
            "validation claims terminal completion")
    require(validation["execution"]["observed_axioms"] == EXPECTED_AXIOMS,
            "validation axiom observation drifted")
    require(validation["first_failed_gate"] ==
            "dependency.S56-M-1023-PROOF.master_acceptance",
            "validation dependency boundary drifted")
    require(vendor["upstream"]["revision"] ==
            "93b635fba23398bfb1f0db8d220f88172f6900b6",
            "vendored upstream revision drifted")
    require(vendor["closure"]["module_count"] == len(vendor["files"]) == 20,
            "vendor closure drifted")

    require(decision["schema_version"] == "stage1-release-decision/1.0",
            "decision schema drifted")
    require(decision["item_id"] == ITEM and decision["theorem_id"] == THEOREM,
            "decision identity drifted")
    require(decision["phase"] == decision["intent"] == "release",
            "decision intent drifted")
    require(decision["verdict"] == "blocked" and
            decision["release_grade"] is decision["release_accepted"] is False,
            "decision claims release")
    require(decision["base_revision"] == BASE_REVISION and
            decision["base_tree"] == BASE_TREE, "decision base drifted")
    require(decision["lifecycle_before"] == decision["lifecycle_after"] == "planned",
            "blocked release advanced lifecycle")
    require(decision["accepted_receipt_ids"] == [], "worker accepted a receipt")
    release_vector = {"H": "H1", "M": "M3", "R": "R4"}
    require(decision["root_vector"]["accepted_before"] ==
            decision["root_vector"]["accepted_after"] == release_vector,
            "release changed accepted vector")
    require(decision["terminal_decisions"] == {
        "audit_complete": False,
        "theorem_complete": False,
        "audit_z": "blocked",
        "theorem_z": "blocked",
    }, "terminal decisions do not fail closed")
    require(decision["first_failed_gate"]["gate_id"] ==
            "S56-10.2-DEPENDENCY-ACCEPTANCE", "first gate drifted")
    require(decision["first_failed_audit_gate"]["gate_id"] ==
            "S56-7.1-DISCOVERY-AND-AUTHORITY-RECONCILIATION",
            "audit gate drifted")
    require(decision["first_failed_theorem_gate"]["gate_id"] ==
            "S56-6.7-ACCEPTED-ROOT-COMPOSITION", "theorem gate drifted")
    require(decision["first_failed_release_gate"]["gate_id"] ==
            "S56-7.3-7.4-TRANSITIVE-PROVENANCE-TCB-CLOSURE",
            "release gate drifted")
    require(decision["first_failed_reproduction_gate"]["gate_id"] ==
            "S56-10.6-HERMETIC-COLD-BUILD", "reproduction gate drifted")
    require(decision["authoritative_remaining_root_cut_set"] == ROOT_CUT,
            "decision root cut drifted")
    require(decision["dependency"] == receipt["dependency"],
            "decision/receipt dependency ledgers disagree")
    require(decision["dependency"] == {
        "item_id": "S56-M-1023-VALIDATION",
        "scheduler_projection": "[_]",
        "receipt_id": VALIDATION_RECEIPT_ID,
        "receipt_sha256": VALIDATION_RECEIPT_SHA256,
        "support_state": "provisional_worker_selftest",
        "accepted": False,
        "release_grade": False,
        "master_accepted": False,
    }, "dependency ledger drifted")
    for key in (
        "validation_dependency_master_accepted",
        "frozen_route_and_composition_reconciled",
        "late_external_discovery_reconciled",
        "authoritative_public_projection_reconciled",
        "audit_inventory_and_source_boundaries_accepted",
        "pinpoint_h0_and_independent_source_review",
        "independent_r0_review",
        "accepted_foundation_profile",
        "complete_transitive_declaration_provenance_tcb",
        "immutable_clean_release_input",
        "cold_empty_cache_offline_replay",
        "complete_sbom_license_and_offline_archive",
        "deterministic_content_addressed_release_bundle",
        "two_distinct_signed_runner_attestations",
        "independently_implemented_minimal_verifier",
        "protected_ci_and_required_adversarial_gates",
        "master_acceptance",
    ):
        require(decision["evidence_reconciliation"][key] is False,
                f"release silently cleared {key}")

    require(spec["schema_version"] == "stage1-validation-recipe/1.0",
            "release recipe schema drifted")
    require(spec["item_id"] == receipt["item_id"] == ITEM and
            spec["theorem_id"] == receipt["theorem_id"] == THEOREM,
            "recipe/receipt identity drifted")
    require(spec["argv"] == [
        "python3", "-I", "-B", f"Stage1_Instances/{THEOREM}/check_release.py"
    ], "release argv drifted")
    require(spec["cwd"] == "." and spec["timeout_seconds"] == 3600,
            "release resource contract drifted")
    require(spec["network_policy"] == "denied_for_lean_subprocesses",
            "network policy drifted")
    require(spec["expected_exit"] == 0, "expected exit drifted")
    require(spec["covered_obligation_ids"] == ALL_OBLIGATIONS,
            "recipe misses frozen obligations")
    require(spec["covered_decisions"] == ["AUDIT-Z", "THEOREM-Z"],
            "recipe misses terminal decisions")

    require(receipt["schema_version"] == "stage1-node-receipt/1.0",
            "receipt schema drifted")
    require(receipt["base_revision"] == BASE_REVISION and
            receipt["base_tree"] == BASE_TREE, "receipt base drifted")
    require(receipt["verdict"] == "blocked" and
            receipt["support_state"] == "provisional_worker_selftest",
            "receipt support drifted")
    require(receipt["accepted"] is receipt["master_accepted"] is
            receipt["release_grade"] is receipt["release_accepted"] is False,
            "receipt claims acceptance")
    require(receipt["accepted_receipt_ids"] ==
            receipt["accepted_closed_obligation_ids"] == [],
            "receipt grants acceptance")
    require(receipt["decision_id"] == decision["decision_id"],
            "receipt names wrong decision")
    require(receipt["decision_sha256"] == digest(HERE / "release-decision.json"),
            "decision hash drifted")
    require(receipt["release_spec_sha256"] == digest(HERE / "release-spec.json"),
            "recipe hash drifted")
    require(receipt["checker_sha256"] == digest(Path(__file__).resolve()),
            "checker hash drifted")
    require(receipt["public_projection_sha256"] ==
            digest(HERE / "release-validation.md"), "projection hash drifted")
    require(receipt["known_failures"] == decision["known_failures"],
            "failure ledgers disagree")
    require(set(receipt["changed_paths"]) == CHANGED_PATHS,
            "receipt changed paths drifted")
    require(receipt["canonical_target"] == decision["canonical_target"],
            "canonical target ledgers disagree")
    require(receipt["result"] == {
        "exit_code": 0,
        "verdict": "blocked",
        "lifecycle_before": "planned",
        "lifecycle_after": "planned",
        "root_vector_before": release_vector,
        "root_vector_after": release_vector,
        "accepted_receipt_ids": [],
        "accepted_closed_obligation_ids": [],
        "provisionally_observed_root_kernel_inhabitant": True,
        "remaining_root_cut_set": ROOT_CUT,
        "audit_complete": False,
        "theorem_complete": False,
        "release_accepted": False,
        "first_failed_gate": "S56-10.2-DEPENDENCY-ACCEPTANCE",
        "first_failed_audit_gate": "S56-7.1-DISCOVERY-AND-AUTHORITY-RECONCILIATION",
        "first_failed_theorem_gate": "S56-6.7-ACCEPTED-ROOT-COMPOSITION",
        "first_failed_release_gate": "S56-7.3-7.4-TRANSITIVE-PROVENANCE-TCB-CLOSURE",
        "first_failed_reproduction_gate": "S56-10.6-HERMETIC-COLD-BUILD",
    }, "receipt result drifted")
    for key in (
        "recipe_id", "cwd", "argv", "env_allowlist", "timeout_seconds",
        "network_policy", "network_enforcement", "expected_exit",
        "expected_outputs", "covered_obligation_ids", "covered_declarations",
        "covered_decisions", "coverage_kind", "scope_boundary",
    ):
        require(receipt["recipe"][key] == spec[key], f"receipt/spec mismatch: {key}")

    require(set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }, "worker packet schema drifted")
    require(packet["item_id"] == ITEM and packet["state"] == "[_]",
            "worker packet identity drifted")
    require(packet["base_revision"] == BASE_REVISION, "worker base drifted")
    require(set(packet["changed_paths"]) == CHANGED_PATHS,
            "worker changed paths drifted")
    require(packet["known_failures"] == decision["known_failures"],
            "worker failure ledger drifted")
    require(packet["commands"] == [row["command"] for row in receipt["commands"]],
            "worker command ledger drifted")
    require(packet["output_summary"] == SUMMARY.rstrip("\n"),
            "worker output summary drifted")
    require({row["exit_code"] for row in receipt["commands"]} == {0},
            "recorded command failure")

    status = git("status", "--short", "--untracked-files=all")
    actual_changes = {
        line[3:] for line in status.splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    }
    require(actual_changes == CHANGED_PATHS, f"unexpected changed paths: {actual_changes}")
    public = (HERE / "release-validation.md").read_text(encoding="utf-8")
    for fragment in (
        "`blocked`", "`[H1, M3, R4]`", "`AUDIT-Z`", "`THEOREM-Z`",
        "release_grade=false", "accepts no", "M1023-T-FORWARD",
    ):
        require(fragment in public, f"public projection omits {fragment!r}")
    require("/home/" not in public and ".cron/" not in public,
            "public projection exposes worker path")
    for relative in CHANGED_PATHS:
        data = (ROOT / relative).read_bytes()
        require(data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data,
                f"invalid text bytes: {relative}")
        require(all(not line.endswith((b" ", b"\t")) for line in data.splitlines()),
                f"trailing whitespace: {relative}")

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|implemented_by|native_decide|run_tac)\b|"
        r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
        r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
        r"(?:axiom|constant|opaque|unsafe|extern)\b",
        re.MULTILINE,
    )
    lean_sources = sorted(HERE.rglob("*.lean"))
    require(len(lean_sources) == 25, "owned Lean source count drifted")
    for path in lean_sources:
        source = strip_lean_comments_and_strings(path.read_text(encoding="utf-8"))
        require(prohibited.search(source) is None,
                f"prohibited proof construct: {path.relative_to(HERE)}")

    replay = run(["bash", str(HERE / "check_validation.sh")])
    expected_replay = (
        "PASS network-isolated trust-zero replay: 20 vendored modules, exact statement, frozen composition, proof root, and differential root elaborated\n"
        "PASS trust observation: proof/differential declarations are sorry-free; six reports use exactly propext, Classical.choice, and Quot.sound\n"
        "PASS differential scope: Validation.lean reconstructs the exact root without importing Proof or ObligationTree\n"
    )
    require(replay == expected_replay, "exact-root replay output drifted")
    require(receipt["execution"]["runner_stdout_sha256"] ==
            hashlib.sha256(replay.encode()).hexdigest(), "runner output hash drifted")
    require(receipt["execution"]["runner_stdout_bytes"] == len(replay.encode()),
            "runner output size drifted")
    require(receipt["execution"]["summary_sha256"] ==
            hashlib.sha256(SUMMARY.encode()).hexdigest(), "summary hash drifted")
    require(receipt["execution"]["summary_bytes"] == len(SUMMARY.encode()),
            "summary size drifted")

    print(SUMMARY, end="")


if __name__ == "__main__":
    main()
