#!/usr/bin/env python3
"""Fail-closed release reconciliation for S56-M-1007-RELEASE."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-1007"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM = "S56-M-1007-RELEASE"
THEOREM = "THM-M-1007"
BASE_REVISION = "a9274bb02f984e5c74d2c97339044c6db8eb14f9"
BASE_TREE = "c72a5af07dd4ab3f7088c516c74235e794a6de09"
EXPRESSION_SHA256 = "3b1a82b3fc0ce70be489e8a49279e3f29cfe244f7a50c28f5c4e5de26894cf38"
DENOMINATOR_SHA256 = "0a29c34a938eeb9ddb91009316aabe1be97f16a7606fbc6da3c3aea7429e87cf"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
VALIDATION_RECEIPT_SHA256 = "04fb65eef8146482d4b121a8553c7b6b936c66861889f9d165d5210135170e26"
PROOF_RECEIPT_SHA256 = "35914be02b3722cfa95d8935f92122909e378974975aba2e2e532ecce0b8f525"
EXPECTED_INPUTS = {
    "intake.json": "a3815da91a73afbf9d5dcdc172db58d730a0e5fe82c6f86e278110537614e5f4",
    "README.md": "9ca8a6d839039ebbb6f7304dfe3cb30173b1e8dc630f0f0530d7d1e65a006fba",
    "source_statement_crosswalk.md": "181f6b23ec858a2799aedb0f42309147097185f6b9913eb2e3120d1e3f0b491d",
    "Statement.lean": "596d935026c6276c8a0e57a0e95915d18c568971094a02762bd1f88cdfc5daa9",
    "statement.json": "3590a105cf26828b45e7e70d966ea1764abde523338028e933aa47694085f137",
    "anchor_audit.json": "dddcefe41fae077838cf4b47f861be7731a7060bc7723ee7f1d069030b343b03",
    "obligation-registry.json": "49f4ca7878fea2342d4915a465c92dde637b1a288a7f3dd35429030e7d7e0cf4",
    "typed-graphs.json": "a054c4ef2b9e7b11e4966a549f17994cd57b2ad79c29502340fc29b0567d63b2",
    "ObligationTree.lean": "3f1b170706aaf5ed7c76e6f916e8398d25844fcb6471d8680ca6e194b564ed5f",
    "Proof.lean": "6a8f198527b1f8f915e979991a0e89a06b1728a1bf9e191910a6c63660ecb6c5",
    "proof-receipt.json": PROOF_RECEIPT_SHA256,
    "proof-blocker-2026-07-14.json": "990453f8c79e4873bcd6b0c4c4fec85300dcc800ed92ed9ed5d9a59256eaa9a3",
    "Validation.lean": "3f6780b21eedcf7c2d83571808e455a8defc1369e01372c251d18602245548f0",
    "validation-spec.json": "94c65c48a761caec5098b7f41fc4d90e5dcfc666a73669750a2a5af422645f8f",
    "validation-receipt.json": VALIDATION_RECEIPT_SHA256,
    "validation-phase.md": "32dd5c77ca2a1e23cd188b57d4a5b6a1d07ca39a354ed5339fc1fbe4f921b4ab",
    "check_validation.py": "9b3dedaf6833dbda9d6a23002d79b2669ac3ceac5b5107fa6c6aa76d8f2f767d",
    "run_validation.sh": "73406cc856fcc46500b9f6a395ca1894fd9ce6474e5901fbbed5ac68db357589",
}
AUTHORITY_INPUTS = {
    "Docs/Stage1_Targets_rev-5.6.json": "02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c",
    "Docs/Stage1_Execution_DAG_rev-5.6.json": "4f5335b6a1724a2856bb155e3147debd858e7fc1cf07d4b70c757e6515f5dd23",
    "Docs/Stage1_Blueprint_rev-5.6.md": "770174567b83623a839cf4f9a68c1a78524d516ecd1bc18e17c64130a48052e5",
    "skills/execute-stage1-rev56/SKILL.md": "26d47a66c6535feabb8bbf1051fd55d76a53fe761f4b3d953f86b97ec86152b8",
    "Formalizations/Lean/lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "Formalizations/Lean/lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
ALL_OBLIGATIONS = {
    "M1007-ROOT", "M1007-S-INTERFACE", "M1007-S-BOUNDARY",
    "M1007-S-FOUNDATION", "M1007-N-TRUNCATE", "M1007-C-TRUNC-PROPS",
    "M1007-C-EVENT-INDEP", "M1007-B-LARGE-JUMP-NEC",
    "M1007-B-LARGE-JUMP-SUFF", "M1007-T-EVENTUAL", "M1007-N-CENTER",
    "M1007-L-BOUNDED-NEC", "M1007-L-BOUNDED-SUFF", "M1007-T-NECESSITY",
    "M1007-T-SUFFICIENCY", "M1007-T-ASSEMBLE", "M1007-X-SOURCE",
    "M1007-X-PROVENANCE", "M1007-X-TCB",
}
FROZEN_CUT = [
    "M1007-C-TRUNC-PROPS", "M1007-C-EVENT-INDEP",
    "M1007-B-LARGE-JUMP-NEC", "M1007-B-LARGE-JUMP-SUFF",
    "M1007-T-EVENTUAL", "M1007-L-BOUNDED-NEC", "M1007-L-BOUNDED-SUFF",
]
MATHEMATICAL_CUT = ["M1007-L-BOUNDED-NEC"]
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/check_release.py",
    f"Stage1_Instances/{THEOREM}/release-decision.json",
    f"Stage1_Instances/{THEOREM}/release-receipt.json",
    f"Stage1_Instances/{THEOREM}/release-spec.json",
    f"Stage1_Instances/{THEOREM}/release-validation.md",
}
SUMMARY_LINES = [
    "PASS THM-M-1007 release reconciliation: current authority, target, registry, predecessor receipts, and input hashes agree",
    "PASS current narrow Lean evidence: the exact canonical statement elaborates at trust zero on the pinned Lean 4.29.0 toolchain",
    "PASS evidence boundary: historical proof and validation receipts support exact sufficiency only and remain hash-bound, provisional, unaccepted, and nonrelease",
    "BLOCKED dependency: S56-M-1007-VALIDATION lacks master acceptance and its recorded recipe is stale at current HEAD",
    "BLOCKED exact root: M1007-L-BOUNDED-NEC and necessity are absent; accepted obligations remain empty and root vector stays H1/M3/R3",
    "BLOCKED audit and assurance: H0/R0, accepted foundation, complete provenance/TCB/SBOM, cold offline replay, independent verification, CI, and deterministic bundle are absent",
    "verdict=blocked; lifecycle=planned; audit_complete=false; theorem_complete=false; accepted_receipt_ids=[]",
]


def fail(message: str) -> None:
    raise SystemExit(f"release-decision: FAIL: {message}")


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def load(path: Path) -> dict:
    def reject_duplicates(pairs: list[tuple[str, object]]) -> dict:
        result: dict[str, object] = {}
        for key, value in pairs:
            require(key not in result, f"duplicate JSON key in {path}: {key}")
            result[key] = value
        return result

    value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates)
    require(isinstance(value, dict), f"JSON object required: {path}")
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(argv: list[str], *, cwd: Path = ROOT) -> str:
    completed = subprocess.run(
        argv, cwd=cwd, text=True, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, timeout=60, check=False,
    )
    require(
        completed.returncode == 0,
        f"command failed ({completed.returncode}): {argv!r}\n{completed.stdout}",
    )
    return completed.stdout.rstrip()


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["git", *args], cwd=cwd)


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
    require(depth == 0, "unterminated Lean block comment")
    return "".join(output)


def assert_text_hygiene(path: Path) -> None:
    data = path.read_bytes()
    require(data.endswith(b"\n"), f"missing terminal newline: {path}")
    require(b"\r" not in data and b"\x00" not in data, f"bad bytes: {path}")
    require(
        all(not line.endswith((b" ", b"\t")) for line in data.splitlines()),
        f"trailing whitespace: {path}",
    )


def main() -> None:
    decision = load(HERE / "release-decision.json")
    receipt = load(HERE / "release-receipt.json")
    spec = load(HERE / "release-spec.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")
    intake = load(HERE / "intake.json")
    statement = load(HERE / "statement.json")
    anchor = load(HERE / "anchor_audit.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    proof = load(HERE / "proof-receipt.json")
    blocker = load(HERE / "proof-blocker-2026-07-14.json")
    validation = load(HERE / "validation-receipt.json")
    targets = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")

    require(git("rev-parse", "HEAD") == BASE_REVISION, "base revision drifted")
    require(git("rev-parse", "HEAD^{tree}") == BASE_TREE, "base tree drifted")
    for name, expected in EXPECTED_INPUTS.items():
        require(sha256(HERE / name) == expected, f"reconciled input drifted: {name}")
    for name, expected in AUTHORITY_INPUTS.items():
        require(sha256(ROOT / name) == expected, f"authority input drifted: {name}")
    require(receipt["inputs"] == EXPECTED_INPUTS, "receipt input ledger drifted")
    require(receipt["authority_inputs"] == AUTHORITY_INPUTS,
            "receipt authority ledger drifted")

    target = next((row for row in targets["targets"] if row["theorem_id"] == THEOREM), None)
    require(target is not None and target["execution_rank"] == 287, "target membership drifted")
    require(target["baseline"] == "L0" and target["rework_required"] is True,
            "uniform L0 baseline drifted")
    require(target["lifecycle_mode"] == "planned" and target["theorem_complete"] is False,
            "target authority no longer records an open planned theorem")
    release_item = next((row for row in execution["items"] if row["id"] == ITEM), None)
    validation_item = next(
        (row for row in execution["items"] if row["id"] == "S56-M-1007-VALIDATION"), None,
    )
    require(release_item == {
        "id": ITEM, "theorem_id": THEOREM, "execution_rank": 287,
        "phase": "release", "layer": 6, "state": "[ ]",
        "depends_on": ["S56-M-1007-VALIDATION"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Reconcile evidence and decide the exact theorem-completion verdict.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0, "children": [],
    }, "release DAG item drifted")
    require(validation_item is not None and validation_item["state"] == "[_]" and
            validation_item["attempts"] == 1,
            "validation dependency is not the recorded provisional state")

    require(intake["lifecycle_mode"] == "planned", "intake lifecycle drifted")
    require(intake["root_vector"] == {
        "human": "H1", "machine": "M3", "readability": "R3",
    }, "intake vector drifted")
    require(intake["theorem_complete"] is False, "intake claims completion")
    formal = statement["canonical_formal_target"]
    require(formal["declaration_or_expression"] == (
        "Stage1Instances.THM_M_1007.KolmogorovThreeSeriesTarget"
    ), "canonical declaration drifted")
    require(formal["elaborated_expression_sha256"] == EXPRESSION_SHA256,
            "canonical expression drifted")
    require(statement["statement_elaborated"] is True and statement["theorem_complete"] is False,
            "statement boundary drifted")
    require(anchor["canonical_expression_sha256"] == EXPRESSION_SHA256,
            "anchor target drifted")
    require(anchor["classification"]["human"] == "H1" and
            anchor["classification"]["machine"] == "M3" and
            anchor["classification"]["readability"] == "R3",
            "anchor classification drifted")
    require(anchor["theorem_complete"] is False, "anchor claims completion")
    require(registry["denominator_sha256"] == DENOMINATOR_SHA256,
            "registry denominator drifted")
    require({row["obligation_id"] for row in registry["obligations"]} == ALL_OBLIGATIONS,
            "registry obligation universe drifted")
    require(graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256,
            "graph denominator drifted")
    require({row["obligation_id"] for row in graphs["nodes"]} == ALL_OBLIGATIONS,
            "graph obligation universe drifted")
    closure = graphs["closure_boundary"]
    require(closure["closed_obligations"] == [], "graph contains accepted closure")
    require(closure["root_closed"] is False and closure["root_machine_debt"] == "M3",
            "graph root boundary drifted")
    require(closure["remaining_root_cut_set"] == FROZEN_CUT, "frozen cut drifted")
    require(closure["audit_complete"] is False and closure["theorem_complete"] is False,
            "graph claims terminal completion")

    require(sha256(HERE / "proof-receipt.json") == PROOF_RECEIPT_SHA256,
            "proof receipt digest drifted")
    require(proof["receipt_id"] == "S56-M-1007-PROOF-partial-20260714",
            "wrong proof receipt")
    require(proof["support_state"] == "provisional_worker_selftest" and proof["accepted"] is False,
            "proof receipt was promoted")
    require(proof["result"]["root_closed"] is False and proof["result"]["theorem_complete"] is False,
            "proof receipt claims root completion")
    require(proof["provisional_mathematical_remaining_cut"] == MATHEMATICAL_CUT,
            "proof mathematical cut drifted")
    require(blocker["root_closed"] is False and blocker["theorem_complete"] is False and
            blocker["provisional_mathematical_remaining_cut"] == MATHEMATICAL_CUT,
            "proof blocker boundary drifted")
    require(sha256(HERE / "validation-receipt.json") == VALIDATION_RECEIPT_SHA256,
            "validation receipt digest drifted")
    require(validation["receipt_id"] == "S56-M-1007-VALIDATION-local-20260715T064753+0800",
            "wrong validation receipt")
    require(validation["support_state"] == "provisional_worker_selftest" and
            validation["accepted"] is False and validation["release_grade"] is False,
            "validation receipt was promoted")
    require(validation["result"]["root_kernel_closed"] is False and
            validation["result"]["root_machine_debt"] == "M3",
            "validation root boundary drifted")
    require(validation["result"]["audit_complete"] is False and
            validation["result"]["theorem_complete"] is False,
            "validation claims terminal completion")
    require(validation["base_revision"] != BASE_REVISION,
            "stale validation-recipe boundary unexpectedly disappeared")

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by|run_tac)\b|"
        r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
        r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
        r"(?:axiom|constant|opaque|unsafe|extern)\b",
        flags=re.MULTILINE,
    )
    for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
        source = source_without_comments((HERE / name).read_text(encoding="utf-8"))
        source = re.sub(r"^#print sorries .*?$", "", source, flags=re.MULTILINE)
        require(prohibited.search(source) is None, f"prohibited source construct in {name}")
    proof_source = source_without_comments((HERE / "Proof.lean").read_text(encoding="utf-8"))
    require("KolmogorovThreeSeriesTarget := by" not in proof_source,
            "proof source now claims canonical root")
    require("obligationTree_necessity" not in proof_source and
            "ObligationTree.Necessity" not in proof_source,
            "proof source now contains necessity and needs reconciliation")

    manifest = load(LEAN_ROOT / "lake-manifest.json")
    mathlib_entry = next(row for row in manifest["packages"] if row["name"] == "mathlib")
    require(mathlib_entry["rev"] == mathlib_entry["inputRev"] == MATHLIB_REVISION,
            "mathlib pin drifted")
    require(MATHLIB.resolve().is_dir(), "canonical pinned mathlib artifact missing")
    require(git("rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION,
            "mathlib revision drifted")
    require(git("rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE,
            "mathlib tree drifted")
    require(git("status", "--porcelain=v1", cwd=MATHLIB) == "",
            "mathlib source worktree is dirty")

    require(spec["schema_version"] == "stage1-validation-recipe/1.0",
            "release recipe schema drifted")
    require(spec["item_id"] == ITEM and spec["theorem_id"] == THEOREM,
            "release recipe identity drifted")
    require(spec["argv"] == ["python3", "-B", f"Stage1_Instances/{THEOREM}/check_release.py"],
            "release recipe argv drifted")
    require(spec["cwd"] == "." and spec["timeout_seconds"] == 120,
            "release recipe cwd or timeout drifted")
    require(spec["network_policy"] == "denied" and
            "does not invoke a network client" in spec["network_enforcement"],
            "release recipe network boundary drifted")
    require(spec["expected_exit"] == 0, "release recipe expected exit drifted")
    require(set(spec["covered_obligation_ids"]) == ALL_OBLIGATIONS,
            "release recipe misses a frozen obligation")

    require(decision["item_id"] == ITEM and decision["theorem_id"] == THEOREM,
            "release decision identity drifted")
    require(decision["intent"] == "release" and decision["verdict"] == "blocked",
            "release decision is not blocked")
    require(decision["base_revision"] == BASE_REVISION and decision["base_tree"] == BASE_TREE,
            "decision base drifted")
    require(decision["decision_support"] == "provisional_worker_selftest" and
            decision["release_grade"] is False and decision["release_accepted"] is False,
            "decision support was promoted")
    require(decision["lifecycle_before"] == decision["lifecycle_after"] == "planned",
            "blocked release advanced lifecycle")
    require(decision["accepted_receipt_ids"] == [], "worker accepted a receipt")
    require(decision["root_vector"]["recorded_before"] == ["H1", "M3", "R3"] and
            decision["root_vector"]["recorded_after"] == ["H1", "M3", "R3"],
            "release vector changed")
    require(decision["terminal_decisions"] == {
        "audit_complete": False, "theorem_complete": False,
        "audit_z": "blocked", "theorem_z": "blocked",
    }, "terminal decisions are not fail-closed")
    dependency = decision["dependency"]
    require(dependency["item_id"] == validation["item_id"] and
            dependency["receipt_id"] == validation["receipt_id"],
            "decision dependency identity mismatch")
    require(dependency["receipt_sha256"] == VALIDATION_RECEIPT_SHA256 and
            dependency["master_accepted"] is False and
            dependency["recorded_recipe_replay"] == "stale_at_current_head",
            "decision dependency boundary drifted")
    require(decision["first_failed_gate"]["gate_id"] ==
            "S56-10.2-DEPENDENCY-ACCEPTANCE", "first node gate drifted")
    require(decision["first_failed_mathematical_gate"]["gate_id"] ==
            "proof.root_kernel_closure.M1007-L-BOUNDED-NEC",
            "first mathematical gate drifted")
    require(decision["first_failed_release_gate"]["gate_id"] ==
            "S56-7.3-7.4-TRANSITIVE-PROVENANCE-TCB-CLOSURE",
            "first release gate drifted")
    require(decision["first_failed_reproduction_gate"]["gate_id"] ==
            "S56-10.6-HERMETIC-COLD-BUILD", "reproduction gate drifted")
    for key in (
        "validation_dependency_master_acceptance", "audit_inventory_complete_and_accepted",
        "pinpoint_h0_and_independent_source_review", "independent_r0_review",
        "accepted_foundation_and_complete_transitive_provenance_tcb",
        "immutable_clean_release_input", "hermetic_cold_offline_replay",
        "sbom_license_and_durable_archive_closure",
        "two_independent_signed_runner_attestations",
        "independently_implemented_minimal_release_verifier",
        "protected_ci_and_required_adversarial_gates",
        "deterministic_content_addressed_release_bundle", "master_acceptance",
    ):
        require(decision["evidence_reconciliation"][key] is False,
                f"release cleared missing gate {key}")
    require(decision["evidence_reconciliation"]["accepted_closed_obligation_ids"] == [],
            "release accepted an obligation")

    require(receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM,
            "release receipt identity drifted")
    require(receipt["phase"] == receipt["intent"] == "release" and
            receipt["depends_on"] == ["S56-M-1007-VALIDATION"],
            "release receipt phase or dependency drifted")
    require(receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE,
            "release receipt base drifted")
    require(receipt["support_state"] == "provisional_worker_selftest" and
            receipt["proposed_state"] == "[_]" and receipt["accepted"] is False,
            "release receipt was accepted")
    require(receipt["release_grade"] is False and
            receipt["content_addressed_release_evidence"] is False and
            receipt["master_accepted"] is False,
            "release receipt was promoted")
    require(receipt["verdict"] == "blocked" and receipt["decision_id"] == decision["decision_id"],
            "receipt/decision verdict mismatch")
    require(receipt["dependency"]["receipt_sha256"] == VALIDATION_RECEIPT_SHA256,
            "receipt dependency hash drifted")
    result = receipt["result"]
    require(result["exact_root_kernel_closed"] is False and
            result["accepted_receipt_ids"] == [] and
            result["accepted_closed_obligation_ids"] == [],
            "release receipt accepted root evidence")
    require(result["mathematical_remaining_cut"] == MATHEMATICAL_CUT and
            result["authoritative_frozen_cut_set"] == FROZEN_CUT,
            "release receipt cut set drifted")
    require(result["audit_complete"] is False and result["theorem_complete"] is False and
            result["release_accepted"] is False,
            "release receipt claims completion")

    expected_packet = {
        "item_id": ITEM,
        "changed_paths": receipt["changed_paths"],
        "commands": receipt["commands_and_results"],
        "output_summary": "\n".join(SUMMARY_LINES),
        "base_revision": BASE_REVISION,
        "known_failures": receipt["known_failures"],
        "state": "[_]",
    }
    require(packet == expected_packet, "worker self-test packet drifted")
    require(set(receipt["changed_paths"]) == CHANGED_PATHS,
            "receipt changed-path set drifted")
    status = git("status", "--short", "--untracked-files=all")
    actual_changes = {
        line[3:] for line in status.splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    }
    require(actual_changes == CHANGED_PATHS, f"unexpected scoped changes: {actual_changes}")
    for relative in CHANGED_PATHS:
        assert_text_hygiene(ROOT / relative)
    print("\n".join(SUMMARY_LINES))


if __name__ == "__main__":
    main()
