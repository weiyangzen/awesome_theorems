#!/usr/bin/env python3
"""Fail-closed release reconciliation for S56-M-1024-RELEASE."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-1024"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
ITEM = "S56-M-1024-RELEASE"
THEOREM = "THM-M-1024"
BASE_REVISION = "557b928b377b386864527c9fb4831d45857837aa"
BASE_TREE = "e677879a6eb4cb9d6795ba1bd78726af06ab9465"
VALIDATION_BASE_REVISION = "400502797d73f88ee509ece5b25ced4e9b673e60"
VALIDATION_RECEIPT_SHA256 = (
    "cf013cbfc7c2acb35d0679909b5d6221e3ec233e6c6b14ff63d86d44d22d2c03"
)
STATEMENT_SHA256 = "197a7197043d6645b3a2e0a190c57571f93521686da2a84a264faef959481a87"
DENOMINATOR_SHA256 = "09ae507f5852e0e927272c16a31701c7b4e7a9f69359716285d2a915bdb44921"
ALL_OBLIGATIONS = [
    "M1024-ROOT",
    "M1024-S-DEFINITIONS",
    "M1024-S-CONVENTIONS",
    "M1024-S-BOUNDARY",
    "M1024-S-FOUNDATION",
    "M1024-N-EXPONENT",
    "M1024-B-FORWARD",
    "M1024-C-ARRAY",
    "M1024-L-TIGHTNESS",
    "M1024-L-FORWARD-IDENTITY",
    "M1024-B-CONVERSE",
    "M1024-C-REALIZATION",
    "M1024-L-CONVOLUTION-ROOTS",
    "M1024-B-UNIQUENESS",
    "M1024-L-JUMP-UNIQUENESS",
    "M1024-L-GAUSSIAN-UNIQUENESS",
    "M1024-L-DRIFT-UNIQUENESS",
    "M1024-T-FORWARD",
    "M1024-T-CONVERSE",
    "M1024-T-UNIQUENESS",
    "M1024-T-ASSEMBLE",
    "M1024-X-SOURCE",
    "M1024-X-EXTERNAL",
    "M1024-X-PROVENANCE",
]
ROOT_CUT = ["M1024-T-FORWARD", "M1024-T-CONVERSE", "M1024-T-UNIQUENESS"]
EXPECTED_INPUTS = {
    "README.md": "10bd054e582248eeedfe448d19fa434f875a72ccdd6d0c5dd95fb2e6e14472d1",
    "intake.json": "d4a6bd03e79c81a47117bc97331c7cce463defdf9040d170a02f1b0e73a69dea",
    "Statement.lean": STATEMENT_SHA256,
    "statement.json": "9179bc579f5dbbb9d8a9744ecc5114d0a4a2a93db08b100e684672370acef084",
    "source_statement_crosswalk.md": "4a02885ac05a8d5738b2286243e68d2c82493d629cc3403a9c30a436bffdc9bc",
    "AnchorAudit.lean": "3f08c7bf2d3058b5cb035cb7f5b7a13d8a2b94ef97c8ec44b10b38a8bfe83326",
    "anchor-audit.json": "26013142d8d916de7a8f6662e23e8833efdcd5032d11cf039f4e0e733a396199",
    "obligation-registry.json": "805d027545115d1078b522f0499a6bf69e11825657af01e9723165e961c78ee5",
    "typed-graphs.json": "8180ffacb09d1dddabf82cc56dc8c7d573186595b7072e9207a611d13f1dc8f0",
    "ObligationTree.lean": "a731c59b39859c7e13677bf69e2e37cd4a719e5bab5905dfa03206abba087977",
    "Proof.lean": "86057da583c3dbcd6c5b1d9b67e538e6c02bcf46124222bc57b8f143f49bcaaa",
    "proof-blocker.json": "7ebddf83eeea4085f14a2ed7b220a17d13b3ccc47d214d1076f94631dd679c64",
    "proof-receipt.json": "f70c580ffd4e83a308193fa790af022a2c93779ee1c2927633e8a5f79ecfe599",
    "Validation.lean": "72791eff66e79e8d5ae960ff4b46b1186f64e51c1b06a87e1c8741e20a230bbc",
    "validation-spec.json": "ceeeb730ab70b95a33cbb91c98189d1a893c654bb6c290e75a5cf9aa46b835a0",
    "validation-receipt.json": VALIDATION_RECEIPT_SHA256,
    "validation-phase.md": "e78d97b465fdd2a1b751cb4dd51502f813ee0264e2464d74110b3a94758c64ae",
    "check_validation.py": "ed2fda4761bc4b913cccfd631cbb6d76f3e8f8b5ac204b080e3155cfdefc3832",
    "check_obligation_tree.py": "dbb7196f7971728398512ab6f2256a327685b5b1efaec3845bdc7d62d890abed",
}
AUTHORITY_INPUTS = {
    "Docs/Stage1_Targets_rev-5.6.json": "02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c",
    "Docs/Stage1_Execution_DAG_rev-5.6.json": "ab3bfabcf3ccff2b4e684273f9eaf7db9376bab69c4455f808196a6af05b3973",
    "Docs/Stage1_Blueprint_rev-5.6.md": "8830573c4a74ff560daebbfcde9278136a30d9841a81816cee8a7ce9c0f5eee4",
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


def load(path: Path) -> dict:
    def reject_duplicates(pairs: list[tuple[str, object]]) -> dict:
        result: dict[str, object] = {}
        for key, value in pairs:
            require(key not in result, f"duplicate JSON key in {path}: {key}")
            result[key] = value
        return result

    value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates)
    require(isinstance(value, dict), f"expected JSON object: {path}")
    return value


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"release failed: {message}")


def run(argv: list[str], *, cwd: Path = ROOT, timeout: int = 300) -> str:
    result = subprocess.run(
        argv,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=timeout,
        check=False,
    )
    require(result.returncode == 0, f"command failed ({result.returncode}): {argv!r}\n{result.stdout}")
    return result.stdout


def git(*args: str) -> str:
    return run(["git", *args], timeout=60).strip()


def strip_lean_comments(source: str) -> str:
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
    require(depth == 0, "unterminated Lean block comment")
    return "".join(output)


def statement_replay() -> str:
    with tempfile.TemporaryDirectory(prefix="m1024-release-", dir="/tmp") as tmp_name:
        output = run(
            [
                "lake",
                "env",
                "lean",
                "--trust=0",
                "-t0",
                "--root",
                str(HERE),
                "-o",
                str(Path(tmp_name) / "Statement.olean"),
                str(HERE / "Statement.lean"),
            ],
            cwd=LEAN_ROOT,
            timeout=360,
        )
    require("LevyKhintchineTarget" in output, "statement print output omitted the canonical target")
    require("error:" not in output and "sorryAx" not in output, "statement replay reported an error")
    return output


def main() -> None:
    require(not sys.flags.optimize, "optimized Python disables fail-closed checks")
    os.environ.update({"LANG": "C.UTF-8", "LC_ALL": "C.UTF-8", "TZ": "UTC", "LEAN_NUM_THREADS": "1"})

    decision = load(HERE / "release-decision.json")
    receipt = load(HERE / "release-receipt.json")
    spec = load(HERE / "release-spec.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")
    intake = load(HERE / "intake.json")
    statement = load(HERE / "statement.json")
    anchor = load(HERE / "anchor-audit.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    proof = load(HERE / "proof-receipt.json")
    blocker = load(HERE / "proof-blocker.json")
    validation = load(HERE / "validation-receipt.json")
    targets = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")

    require(git("rev-parse", "HEAD") == BASE_REVISION, "base revision drifted")
    require(git("rev-parse", "HEAD^{tree}") == BASE_TREE, "base tree drifted")
    run(["git", "merge-base", "--is-ancestor", VALIDATION_BASE_REVISION, BASE_REVISION])
    for name, expected in EXPECTED_INPUTS.items():
        require(digest(HERE / name) == expected, f"reconciled input drifted: {name}")
    require(decision["reconciled_inputs"] == EXPECTED_INPUTS, "decision input map drifted")
    for name, expected in AUTHORITY_INPUTS.items():
        require(digest(ROOT / name) == expected, f"authority input drifted: {name}")
    require(decision["authority_inputs"] == AUTHORITY_INPUTS, "decision authority map drifted")

    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    require(target["execution_rank"] == 500, "execution rank drifted")
    require(target["target_lane"] == "hard_mathlib_anchor_and_wrapper", "target lane drifted")
    require(target["baseline"] == "L0" and target["rework_required"] is True, "L0 baseline drifted")
    require(target["lifecycle_mode"] == "planned" and target["theorem_complete"] is False,
            "target authority no longer records a planned open theorem")
    items = {row["id"]: row for row in execution["items"]}
    require(items[ITEM] == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 500,
        "phase": "release",
        "layer": 6,
        "state": "[ ]",
        "depends_on": ["S56-M-1024-VALIDATION"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Reconcile evidence and decide the exact theorem-completion verdict.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }, "release DAG item drifted")
    require(items["S56-M-1024-VALIDATION"]["state"] == "[_]", "validation is no longer provisional")

    require(intake["lifecycle_mode"] == "planned" and intake["theorem_complete"] is False,
            "intake authority claims completion")
    require(intake["root_vector"] == {"human": "H1", "machine": "M4", "readability": "R3"},
            "intake scope vector drifted")
    formal = statement["canonical_formal_target"]
    require(formal["declaration_or_expression"] ==
            "Stage1Instances.THM_M_1024.LevyKhintchineTarget", "target declaration drifted")
    require(formal["statement_file_sha256"] == STATEMENT_SHA256, "statement hash drifted")
    require("elaborated_expression_sha256" not in formal and
            "elaborated_expression_hash" not in formal, "release record must be updated for a new expression hash")
    require(statement["statement_elaborated"] is True and statement["theorem_proved"] is False,
            "statement proof boundary drifted")
    require(anchor["root_machine_classification"] == "M3" and
            anchor["mathlib"]["exact_candidate_found"] is False, "anchor boundary drifted")

    require(registry["denominator_sha256"] == DENOMINATOR_SHA256, "registry denominator drifted")
    require([row["obligation_id"] for row in registry["obligations"]] == ALL_OBLIGATIONS,
            "obligation inventory drifted")
    require(graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256, "graph denominator drifted")
    require({row["obligation_id"] for row in graphs["nodes"]} == set(ALL_OBLIGATIONS),
            "typed graph inventory drifted")
    require(sum(len(graph["edges"]) for graph in graphs["graphs"].values()) == 66,
            "typed edge count drifted")
    root = next(row for row in graphs["nodes"] if row["obligation_id"] == "M1024-ROOT")
    require((root["human_debt"], root["machine_debt"], root["readability_debt"]) ==
            ("H1", "M3", "R3"), "provisional graph vector drifted")
    boundary = graphs["closure_boundary"]
    require(boundary["root_closed"] is boundary["audit_complete"] is
            boundary["theorem_complete"] is False, "graph claims terminal completion")
    require(boundary["remaining_root_cut_set"] == ROOT_CUT, "root cut drifted")

    require(proof["support_state"] == "provisional_worker_selftest" and proof["accepted"] is False,
            "proof receipt became accepted")
    require(proof["supported_obligation_ids"] == proof["provisionally_closed_obligation_ids"] ==
            proof["accepted_closed_obligation_ids"] == [], "proof receipt claims frozen closure")
    require(proof["partial_progress_toward_obligation_ids"] == ["M1024-N-EXPONENT"],
            "proof progress boundary drifted")
    require(proof["result"]["root_kernel_closed"] is False and
            proof["result"]["theorem_complete"] is False, "proof receipt claims completion")
    require(blocker["remaining_root_cut_set"] == ROOT_CUT and blocker["theorem_complete"] is False,
            "proof blocker drifted")
    require(digest(HERE / "validation-receipt.json") == VALIDATION_RECEIPT_SHA256,
            "validation receipt bytes drifted")
    require(validation["base_revision"] == VALIDATION_BASE_REVISION, "validation base drifted")
    require(validation["support_state"] == "provisional_worker_selftest" and
            validation["accepted"] is validation["release_grade"] is False,
            "validation became accepted or release-grade")
    require(validation["result"]["root_kernel_closed"] is False and
            validation["result"]["audit_complete"] is validation["result"]["theorem_complete"] is False,
            "validation claims terminal completion")
    require(validation["remaining_root_cut_set"] == ROOT_CUT, "validation root cut drifted")

    require(decision["schema_version"] == "stage1-release-decision/1.0", "decision schema drifted")
    require(decision["item_id"] == ITEM and decision["theorem_id"] == THEOREM, "decision identity drifted")
    require(decision["intent"] == "release" and decision["verdict"] == "blocked", "verdict drifted")
    require(decision["release_grade"] is decision["release_accepted"] is False,
            "decision claims release")
    require(decision["base_revision"] == BASE_REVISION and decision["base_tree"] == BASE_TREE,
            "decision base drifted")
    require(decision["lifecycle_before"] == decision["lifecycle_after"] == "planned",
            "blocked release advanced lifecycle")
    require(decision["accepted_receipt_ids"] == [], "worker accepted a receipt")
    expected_scope = {"H": "H1", "M": "M4", "R": "R3"}
    require(decision["root_vector"]["scope_authority_before"] ==
            decision["root_vector"]["scope_authority_after"] == expected_scope,
            "decision changed planned scope vector")
    require(decision["root_vector"]["provisional_graph_observation"] ==
            {"H": "H1", "M": "M3", "R": "R3"}, "provisional vector drifted")
    require(decision["terminal_decisions"] == {
        "audit_complete": False,
        "theorem_complete": False,
        "audit_z": "blocked",
        "theorem_z": "blocked",
    }, "terminal decisions do not fail closed")
    require(decision["first_failed_gate"]["gate_id"] == "S56-10.2-DEPENDENCY-ACCEPTANCE",
            "first node gate drifted")
    require(decision["first_failed_statement_gate"]["gate_id"] ==
            "S56-5.1-CANONICAL-EXPRESSION-FINGERPRINT", "statement gate drifted")
    require(decision["first_failed_theorem_gate"]["gate_id"] ==
            "proof.M1024-N-EXPONENT.kernel_closure", "theorem gate drifted")
    require(decision["first_failed_release_gate"]["gate_id"] ==
            "S56-7.3-7.4-TRANSITIVE-PROVENANCE-TCB-CLOSURE", "release gate drifted")
    require(decision["first_failed_reproduction_gate"]["gate_id"] ==
            "S56-10.6-HERMETIC-COLD-BUILD", "reproduction gate drifted")
    require(decision["authoritative_remaining_root_cut_set"] == ROOT_CUT, "decision root cut drifted")
    require(decision["dependency"]["receipt_sha256"] == VALIDATION_RECEIPT_SHA256 and
            decision["dependency"]["master_accepted"] is False, "dependency ledger drifted")
    require(decision["dependency"]["receipt_id"] == validation["receipt_id"], "wrong dependency receipt")
    false_gates = (
        "normalized_elaborated_expression_identity",
        "validation_dependency_master_accepted",
        "exact_root_kernel_closed",
        "accepted_foundation_profile",
        "complete_transitive_provenance_and_tcb",
        "pinpoint_h0_and_independent_source_review",
        "independent_r0_review",
        "audit_z_accepted",
        "immutable_clean_release_input",
        "hermetic_empty_cache_cold_offline_replay",
        "complete_sbom_license_archive_closure",
        "two_independent_signed_runner_attestations",
        "independently_implemented_minimal_verifier",
        "protected_ci_and_adversarial_gates",
        "deterministic_content_addressed_release_bundle",
        "master_acceptance",
    )
    for key in false_gates:
        require(decision["evidence_reconciliation"][key] is False,
                f"release silently cleared {key}")
    require(decision["evidence_reconciliation"]["predecessor_recipe_freshness"] ==
            "fail_closed_phase_bound_to_historical_head_old_DAG_and_validation_worker_packet",
            "stale predecessor recipe was hidden")

    require(spec["schema_version"] == "stage1-validation-recipe/1.0", "release spec schema drifted")
    require(spec["item_id"] == receipt["item_id"] == ITEM and
            spec["theorem_id"] == receipt["theorem_id"] == THEOREM, "spec identity drifted")
    require(spec["argv"] == ["python3", "-B", f"Stage1_Instances/{THEOREM}/check_release.py"],
            "release argv drifted")
    require(spec["cwd"] == "." and spec["network_policy"] == "denied", "recipe policy drifted")
    require(spec["timeout_seconds"] == 900 and spec["expected_exit"] == 0, "resource contract drifted")
    require(spec["covered_obligation_ids"] == ALL_OBLIGATIONS, "spec misses frozen obligations")

    require(receipt["schema_version"] == "stage1-node-receipt/1.0", "receipt schema drifted")
    require(receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE,
            "receipt base drifted")
    require(receipt["verdict"] == "blocked" and receipt["support_state"] ==
            "provisional_worker_selftest", "receipt support drifted")
    require(receipt["accepted"] is receipt["master_accepted"] is receipt["release_grade"] is
            receipt["release_accepted"] is False, "receipt claims acceptance")
    require(receipt["decision_id"] == decision["decision_id"], "receipt names wrong decision")
    require(receipt["decision_sha256"] == digest(HERE / "release-decision.json"), "decision hash drifted")
    require(receipt["release_spec_sha256"] == digest(HERE / "release-spec.json"), "spec hash drifted")
    require(receipt["checker_sha256"] == digest(Path(__file__).resolve()), "checker hash drifted")
    require(receipt["public_projection_sha256"] == digest(HERE / "release-validation.md"),
            "projection hash drifted")
    require(receipt["dependency"] == decision["dependency"], "dependency ledgers disagree")
    for key in (
        "recipe_id", "cwd", "argv", "env_allowlist", "timeout_seconds", "network_policy",
        "network_enforcement", "expected_exit", "expected_outputs", "covered_obligation_ids",
        "covered_declarations", "scope_boundary",
    ):
        require(receipt["recipe"][key] == spec[key], f"receipt/spec mismatch: {key}")
    require(receipt["known_failures"] == decision["known_failures"], "failure ledgers disagree")
    require(set(receipt["changed_paths"]) == CHANGED_PATHS, "receipt changed paths drifted")
    result = receipt["result"]
    require(result["verdict"] == "blocked" and result["audit_complete"] is
            result["theorem_complete"] is result["release_accepted"] is False,
            "receipt result claims completion")
    require(result["root_vector_before"] == result["root_vector_after"] == expected_scope,
            "receipt changed planned vector")
    require(result["accepted_receipt_ids"] == result["accepted_closed_obligation_ids"] == [],
            "receipt grants acceptance")
    require(result["remaining_root_cut_set"] == ROOT_CUT, "receipt cut set drifted")

    require(set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary", "base_revision",
        "known_failures", "state",
    }, "worker packet schema drifted")
    require(packet["item_id"] == ITEM and packet["state"] == "[_]", "worker packet identity drifted")
    require(packet["base_revision"] == BASE_REVISION, "worker packet base drifted")
    require(set(packet["changed_paths"]) == CHANGED_PATHS, "worker packet changed paths drifted")
    require(packet["known_failures"] == decision["known_failures"], "worker failure ledger drifted")
    require(packet["commands"] == [row["command"] for row in receipt["commands"]],
            "worker command ledger drifted")
    require({row["exit_code"] for row in receipt["commands"]} == {0}, "recorded command failure")

    status = git("status", "--short", "--untracked-files=all")
    actual_changes = {
        line[3:] for line in status.splitlines() if line[3:] != "Formalizations/Lean/.lake"
    }
    require(actual_changes == CHANGED_PATHS, f"unexpected changed paths: {actual_changes}")
    public = (HERE / "release-validation.md").read_text(encoding="utf-8")
    for fragment in (
        "`blocked`", "`[H1, M4, R3]`", "`AUDIT-Z`", "`THEOREM-Z`",
        "release_grade=false", "accepts no", "M1024-T-FORWARD",
    ):
        require(fragment in public, f"public release projection omits {fragment!r}")
    require("/home/" not in public and ".cron/" not in public, "public projection exposes worker path")
    for relative in CHANGED_PATHS:
        data = (ROOT / relative).read_bytes()
        require(data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data,
                f"invalid text bytes: {relative}")
        require(all(not line.endswith((b" ", b"\t")) for line in data.splitlines()),
                f"trailing whitespace: {relative}")

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|implemented_by|native_decide|run_tac)\b|"
        r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
        r"(?:axiom|constant|opaque|unsafe)\b|\bextern[ \t]+",
        flags=re.MULTILINE,
    )
    for path in HERE.glob("*.lean"):
        require(prohibited.search(strip_lean_comments(path.read_text(encoding="utf-8"))) is None,
                f"prohibited proof construct: {path.name}")

    output = statement_replay()
    require(receipt["current_statement_replay"]["stdout_sha256"] ==
            hashlib.sha256(output.encode()).hexdigest(), "current replay output hash drifted")
    require(receipt["current_statement_replay"]["stdout_bytes"] == len(output.encode()),
            "current replay byte count drifted")

    print("PASS release inputs: authority, dependency receipts, registry, graph, and hashes agree")
    print("PASS current pinned Lean statement elaboration; no root proof is inferred")
    print("PASS fail-closed state: lifecycle planned; planned scope H1/M4/R3; receipts 0")
    print("BLOCKED S56-10.2-DEPENDENCY-ACCEPTANCE: validation is provisional and unaccepted")
    print("BLOCKED proof root: forward, converse, and uniqueness terminal packages are open")
    print("BLOCKED release trust, cold/offline, independent-verifier, and bundle gates")
    print("verdict=blocked audit_complete=false theorem_complete=false")


if __name__ == "__main__":
    main()
