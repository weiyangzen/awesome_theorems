#!/usr/bin/env python3
"""Fail-closed checks for the THM-M-1061 proof-phase packet."""

from __future__ import annotations

import hashlib
import json
import pathlib
import re
import subprocess
import sys


ROOT = pathlib.Path(__file__).resolve().parents[2]
TARGET = ROOT / "Stage1_Instances" / "THM-M-1061"
PROOF = TARGET / "Proof.lean"
RECEIPT = TARGET / "proof-receipt.json"
BLOCKER = TARGET / "proof-blocker.json"

EXPECTED_DECLARATIONS = {
    "Stage1Instances.THM_M_1061.Proof.closed_upper_of_satisfiesLDP",
    "Stage1Instances.THM_M_1061.Proof.open_lower_of_satisfiesLDP",
    "Stage1Instances.THM_M_1061.Proof.lowerSemicontinuous_of_isGoodRateFunction",
    "Stage1Instances.THM_M_1061.Proof.compact_sublevel_of_isGoodRateFunction",
    "Stage1Instances.THM_M_1061.Proof.logExpIntegral_upper_bound",
    "Stage1Instances.THM_M_1061.Proof.logExpIntegral_lower_bound",
    "Stage1Instances.THM_M_1061.Proof.logExpIntegral_bounds_of_satisfiesLDP",
    "Stage1Instances.THM_M_1061.Proof.tendsto_of_variational_liminf_limsup",
    "Stage1Instances.THM_M_1061.Proof.logExpIntegral_tendsto_of_bounds",
}
EXPECTED_PARTIAL = {
    "M1061-S-BOUNDARIES",
    "M1061-N-VARIATIONAL",
    "M1061-L-LOWER-LOCAL",
    "M1061-C-COMPACT-COVER",
    "M1061-L-CORE-UPPER",
    "M1061-T-LIMIT-MERGE",
}
EXPECTED_CLOSED: set[str] = set()
ALLOWED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
AXIOM_REPORT = re.compile(
    r"'(?P<decl>[^']+)' depends on axioms:\s*\[(?P<axioms>.*?)\]",
    re.DOTALL,
)
PROHIBITED = re.compile(
    r"\b(?:sorry|admit|sorryAx|unsafe|opaque|extern|implemented_by|native_decide)\b"
    r"|^[ \t]*(?:axiom|constant)\b",
    re.MULTILINE,
)


def fail(message: str) -> None:
    raise SystemExit(f"FAIL THM-M-1061 proof phase: {message}")


def sha256(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: pathlib.Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        fail(f"cannot load {path.relative_to(ROOT)}: {error}")


def main() -> None:
    source = PROOF.read_text(encoding="utf-8")
    match = PROHIBITED.search(source)
    if match:
        fail(f"prohibited Lean construct {match.group(0)!r} in Proof.lean")

    receipt = load(RECEIPT)
    blocker = load(BLOCKER)
    registry = load(TARGET / "obligation-registry.json")
    graphs = load(TARGET / "typed-graphs.json")
    target_manifest = load(ROOT / "Docs" / "Stage1_Targets_rev-5.6.json")

    if receipt.get("item_id") != "S56-M-1061-PROOF":
        fail("receipt item mismatch")
    if receipt.get("theorem_id") != "THM-M-1061":
        fail("receipt theorem mismatch")
    if receipt.get("support_state") != "provisional_worker_selftest":
        fail("receipt must remain worker-provisional")
    if receipt.get("accepted") is not False or receipt.get("proposed_state") != "[_]":
        fail("receipt overstates acceptance")
    if receipt.get("verdict") != "no_state_change":
        fail("partial proof packet must use no_state_change")
    if set(receipt.get("exact_declarations", [])) != EXPECTED_DECLARATIONS:
        fail("receipt declaration set mismatch")
    if set(receipt.get("provisionally_closed_obligation_ids", [])) != EXPECTED_CLOSED:
        fail("receipt closed-obligation set mismatch")
    if set(receipt.get("accepted_closed_obligation_ids", [])):
        fail("worker receipt cannot contain accepted closed obligations")
    if set(receipt.get("partial_progress_toward_obligation_ids", [])) != EXPECTED_PARTIAL:
        fail("receipt partial-obligation set mismatch")
    if set(receipt.get("result", {}).get("axioms", [])) != ALLOWED_AXIOMS:
        fail("receipt axiom set mismatch")
    for field in ("root_kernel_closed", "audit_complete", "theorem_complete"):
        if receipt.get("result", {}).get(field) is not False:
            fail(f"receipt must record {field}=false")
    for field in ("root_closed", "root_kernel_closed", "audit_complete", "theorem_complete"):
        if receipt.get(field) is True:
            fail(f"receipt top-level {field} cannot be true")
    if receipt.get("root_vector_accepted") != {"H": "H1", "M": "M3", "R": "R3"}:
        fail("receipt accepted root vector mismatch")
    if receipt.get("proof_body", {}).get("source_sha256") != sha256(PROOF):
        fail("Proof.lean hash mismatch")
    if receipt.get("inputs", {}).get("statement_sha256") != sha256(TARGET / "Statement.lean"):
        fail("Statement.lean hash mismatch")
    if receipt.get("inputs", {}).get("obligation_registry_sha256") != sha256(
        TARGET / "obligation-registry.json"
    ):
        fail("obligation registry hash mismatch")
    if receipt.get("inputs", {}).get("typed_graphs_sha256") != sha256(
        TARGET / "typed-graphs.json"
    ):
        fail("typed graph hash mismatch")
    if receipt.get("inputs", {}).get("anchor_audit_sha256") != sha256(
        TARGET / "anchor-audit.json"
    ):
        fail("anchor audit hash mismatch")
    if receipt.get("inputs", {}).get("check_proof_py_sha256") != sha256(
        TARGET / "check_proof.py"
    ):
        fail("proof validator hash mismatch")
    if receipt.get("inputs", {}).get("check_proof_sh_sha256") != sha256(
        TARGET / "check_proof.sh"
    ):
        fail("proof replay script hash mismatch")
    if receipt.get("canonical_target_expression_sha256") != load(
        TARGET / "statement.json"
    ).get("canonical_formal_target", {}).get("elaborated_expression_sha256"):
        fail("canonical target expression hash mismatch")

    obligations = {row["obligation_id"] for row in registry.get("obligations", [])}
    if not (EXPECTED_CLOSED | EXPECTED_PARTIAL) <= obligations:
        fail("receipt references an unknown frozen obligation")
    graph_nodes = {
        row["obligation_id"]: row for row in graphs.get("nodes", [])
    }
    limit_node = graph_nodes.get("M1061-T-LIMIT-MERGE", {})
    if limit_node.get("semantic_step_ledger", {}).get("premises") != (
        "M1061-T-LOWER, M1061-T-UPPER, M1061-N-VARIATIONAL"
    ):
        fail("frozen limit-merge premise set changed")

    targets = target_manifest.get("targets", target_manifest if isinstance(target_manifest, list) else [])
    target = next((row for row in targets if row.get("theorem_id") == "THM-M-1061"), None)
    if target is None or target.get("execution_rank") != 504:
        fail("manifest membership or rank mismatch")
    if target.get("theorem_complete") is not False:
        fail("authoritative manifest unexpectedly claims theorem completion")

    if blocker.get("theorem_id") != "THM-M-1061":
        fail("blocker theorem mismatch")
    if blocker.get("root_closed") is not False or blocker.get("theorem_complete") is not False:
        fail("blocker overstates root status")
    if blocker.get("first_failed_gate") != "M1061-L-LOWER-LOCAL":
        fail("blocker first failed gate mismatch")
    if not str(receipt.get("first_failed_gate", "")).startswith("M1061-L-LOWER-LOCAL:"):
        fail("receipt first failed gate mismatch")
    if set(receipt.get("remaining_root_cut_set", [])) != set(
        blocker.get("remaining_root_cut_set", [])
    ):
        fail("receipt/blocker remaining cut sets disagree")

    completed = subprocess.run(
        ["bash", str(TARGET / "check_proof.sh")],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    if completed.returncode != 0:
        sys.stdout.write(completed.stdout)
        fail(f"Lean replay exited {completed.returncode}")
    for declaration in EXPECTED_DECLARATIONS:
        short = declaration.rsplit(".", 1)[1]
        if short not in completed.stdout or f"'{declaration}' depends on axioms:" not in completed.stdout:
            fail(f"missing Lean type/axiom output for {declaration}")
    reports = {}
    for match in AXIOM_REPORT.finditer(completed.stdout):
        reports[match.group("decl")] = {
            item.strip() for item in match.group("axioms").split(",") if item.strip()
        }
    for declaration in EXPECTED_DECLARATIONS:
        actual = reports.get(declaration)
        if actual is None:
            fail(f"cannot parse axiom report for {declaration}")
        if actual - ALLOWED_AXIOMS:
            fail(f"unexpected axioms for {declaration}: {sorted(actual - ALLOWED_AXIOMS)}")
        if actual != ALLOWED_AXIOMS:
            fail(f"axiom report for {declaration} differs from the attested exact set")

    print(
        "PASS THM-M-1061 proof phase: local boundary, pointwise integral-bound, and "
        "conditional limit-merge bodies elaborate; no frozen obligation or root is claimed closed"
    )


if __name__ == "__main__":
    main()
