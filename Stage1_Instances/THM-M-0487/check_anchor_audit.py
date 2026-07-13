#!/usr/bin/env python3
"""Fail-closed checker for the THM-M-0487 bounded anchor inventory."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
THEOREM_ID = "THM-M-0487"
ITEM_ID = "S56-M-0487-ANCHOR_AUDIT"
BASE_REVISION = "a3b18eec39bf04be025b1641cae02f4d44fdf11a"
BASE_TREE = "fdfff18dea4c6798c5b322b6088dfe556109c134"
EXPRESSION_SHA256 = "29ac94dd615869191754270061d8fe7123991d403a07bbdf27a09f706665e703"
STATEMENT_SHA256 = "9d0200046173c0b0d9d0b52cbf696087f4beea6946c92bfa41f03402a4090b0d"
PROTOCOL_SHA256 = "000033f4f2a4a7bbafea46190fa559ae973d5e91b10eb97093a4d7d6974ae5b6"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
LEAN_OUTPUT_SHA256 = "3080be75bb8187099485ed48a4042fbe99a224e2cea234f9abd8c7faaf841f16"
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM_ID}/AnchorAudit.lean",
    f"Stage1_Instances/{THEOREM_ID}/anchor-audit-receipt.json",
    f"Stage1_Instances/{THEOREM_ID}/anchor-audit-validation.md",
    f"Stage1_Instances/{THEOREM_ID}/anchor-audit.json",
    f"Stage1_Instances/{THEOREM_ID}/anchor-discovery-protocol.json",
    f"Stage1_Instances/{THEOREM_ID}/check_anchor_audit.py",
}
FORBIDDEN_WORDS = tuple(
    "".join(chr(code) for code in codes)
    for codes in (
        (115, 111, 114, 114, 121),
        (97, 100, 109, 105, 116),
        (115, 111, 114, 114, 121, 65, 120),
        (97, 120, 105, 111, 109),
        (117, 110, 115, 97, 102, 101),
        (105, 109, 112, 108, 101, 109, 101, 110, 116, 101, 100, 95, 98, 121),
        (101, 120, 116, 101, 114, 110),
        (111, 112, 97, 113, 117, 101),
    )
)
FORBIDDEN = re.compile(r"\b(?:" + "|".join(FORBIDDEN_WORDS) + r")\b")


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise SystemExit(f"{path} must contain a JSON object")
    return value


def output(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(args, cwd=cwd, text=True).strip()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def without_comments(source: str) -> str:
    source = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
    return re.sub(r"--.*", "", source)


def main() -> None:
    audit = load(HERE / "anchor-audit.json")
    protocol = load(HERE / "anchor-discovery-protocol.json")
    receipt = load(HERE / "anchor-audit-receipt.json")
    statement = load(HERE / "statement.json")
    instance = load(HERE / "instance.json")
    targets = load(ROOT / "Docs" / "Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")

    assert audit["schema_version"] == "stage1-anchor-audit/1.0"
    assert protocol["schema_version"] == "stage1-anchor-discovery/1.0"
    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert audit["item_id"] == protocol["item_id"] == receipt["item_id"] == ITEM_ID
    assert audit["theorem_id"] == protocol["theorem_id"] == receipt["theorem_id"] == THEOREM_ID
    assert audit["base_revision"] == receipt["base_revision"] == packet["base_revision"] == BASE_REVISION
    assert audit["base_tree"] == receipt["base_tree"] == BASE_TREE
    assert output("git", "rev-parse", "HEAD") == BASE_REVISION
    assert output("git", "rev-parse", "HEAD^{tree}") == BASE_TREE
    assert packet["item_id"] == ITEM_ID and packet["state"] == "[_]"
    assert set(packet["changed_paths"]) == set(receipt["changed_paths"]) == CHANGED_PATHS
    assert packet["known_failures"] == receipt["known_failures"]
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False

    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM_ID)
    item = next(row for row in execution["items"] if row["id"] == ITEM_ID)
    assert target["execution_rank"] == audit["execution_rank"] == 1366
    assert target["baseline"] == "L0" and target["rework_required"] is True
    assert target["theorem_complete"] is False
    assert item["phase"] == "anchor_audit" and item["layer"] == 2
    assert item["depends_on"] == ["S56-M-0487-STATEMENT"]
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]

    formal = statement["canonical_formal_target"]
    assert audit["canonical_target_expression_sha256"] == formal["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert audit["canonical_statement_file_sha256"] == formal["statement_file_sha256"] == STATEMENT_SHA256
    assert sha256(HERE / "Statement.lean") == STATEMENT_SHA256
    assert audit["discovery_protocol_sha256"] == PROTOCOL_SHA256
    assert sha256(HERE / "anchor-discovery-protocol.json") == PROTOCOL_SHA256
    assert instance["root_vector"] == {"H": "H1", "M": "M3", "R": "R3"}

    assert protocol["protocol_id"] == "S56-M-0487-ANCHOR-DISCOVERY-20260713-01"
    assert protocol["saturation_claim"] is False
    assert len(protocol["aliases"]) >= 10 and len(protocol["surfaces"]) >= 9
    assert len(protocol["inventory_members"]) == 7

    env = audit["immutable_environment"]
    assert env["mathlib_revision"] == MATHLIB_REVISION
    assert env["mathlib_tree"] == MATHLIB_TREE
    assert output("git", "rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert output("git", "rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert output("git", "status", "--short", cwd=MATHLIB) == ""
    assert sha256(LEAN_ROOT / "lake-manifest.json") == env["manifest_sha256"]
    assert sha256(MATHLIB / "LICENSE") == env["mathlib_license_sha256"]

    candidates = audit["candidates"]
    candidate_ids = [candidate["candidate_id"] for candidate in candidates]
    assert candidate_ids == protocol["inventory_members"]
    assert len(candidate_ids) == len(set(candidate_ids)) == 7

    local = candidates[0]
    assert local["candidate_machine_classification"] == "M3"
    assert local["terminal_proof_body_id"] is None

    support = next(c for c in candidates if c["candidate_id"] == "M0487-C02-MATHLIB-SUPPORT")
    assert support["revision"] == MATHLIB_REVISION and support["tree"] == MATHLIB_TREE
    adapter = (HERE / "AnchorAudit.lean").read_text(encoding="utf-8")
    for declaration in support["declarations"]:
        assert f"#check {declaration}" in adapter
    identities = support["source_identities"]
    for relative in (
        "Mathlib/NumberTheory/PrimeCounting.lean",
        "Mathlib/NumberTheory/Chebyshev.lean",
        "Mathlib/NumberTheory/SumPrimeReciprocals.lean",
    ):
        path = MATHLIB / relative
        assert sha256(path) == identities[f"{relative}_sha256"]
        assert output("git", "rev-parse", f"HEAD:{relative}", cwd=MATHLIB) == identities[f"{relative}_git_blob"]
    assert not FORBIDDEN.search(without_comments(adapter))

    external = next(c for c in candidates if c["candidate_id"] == "M0487-C03-FORMAL-CONJECTURES-EXACT-PLACEHOLDER")
    assert external["source_git_blob"] == "5a57a2e198cba8c56ad69951219402a399a81349"
    assert external["source_sha256"] == "bf6a587c50ba159af919fbe9afa09f04375608c33c68361ffc52246018a5b447"
    assert external["candidate_machine_classification"] == "M5_placeholder_rejected"
    assert "literal placeholder" in external["placeholder_axiom_unsafe_oracle_status"]

    finite = next(c for c in candidates if c["candidate_id"] == "M0487-C04-PRIME-NUMBER-THEOREM-AND-FINITE")
    assert finite["revision"] == "5754873e8dae73f3b50f8f2b7a4f0b15d4df58aa"
    assert finite["tree"] == "e4a46c31867e6650647b3541a3e8a7abf896efa9"
    assert finite["source_git_blob"] == "5774db98691e2cfa0ecdb528c7e9b8ef13175c63"
    assert finite["candidate_machine_classification"] == "M5_statement_mismatch_and_placeholder_ancestry"

    binary = next(c for c in candidates if c["candidate_id"] == "M0487-C05-GOLDBACH-TM-BINARY")
    assert binary["revision"] == "6cd292062516a0a14ea1b34f2ab75154cae7ab1e"
    assert binary["tree"] == "2fd3c49410cdb2786ef3897907e5f8733d4f94fb"
    assert binary["candidate_machine_classification"] == "no_candidate_statement_mismatch"

    scaffold = next(c for c in candidates if c["candidate_id"] == "M0487-C06-FOOLISHAIR-EXACT-SCAFFOLD")
    assert scaffold["revision"] == "751b5ac33d8edc5a7738b0a6ef58ad42f2b15289"
    assert scaffold["tree"] == "ffe47b71e26f0b80d0d931e590e694ffa0b4988f"
    assert scaffold["source_git_blob"] == "f3161c8ea61aa22408f7d47d664d63373028a111"
    assert scaffold["source_sha256"] == "0958db8bc8d5222f1769ce74d091b353b093b92495c7c8131c249393a0259c07"
    assert scaffold["source_archive_sha256"] == "23cc8f4e7c3231fae86739c8c49321fb5f79cacbcbc417e9618311268eec88de"
    assert scaffold["archive_entry_count_including_directories"] == 14
    assert scaffold["source_line_count"] == 22134 and scaffold["source_byte_count"] == 1798597
    assert scaffold["native_decide_occurrences"] == 30662
    assert scaffold["candidate_machine_classification"] == "M3_exact_statement_and_conditional_scaffold"

    searches = audit["external_searches"]
    assert len(searches) == 13
    blocked = {entry["surface"]: entry for entry in searches if "blocked lane" in entry["completion_boundary"]}
    assert set(blocked) == {"GitHub REST code search", "grep.app Lean query"}
    broad = next(s for s in searches if s["query"] == "context:global archived:yes fork:yes lang:Lean Goldbach count:100")
    assert broad["completion_boundary"].startswith("result limit hit")

    decision = audit["inventory_decision"]
    assert decision["inventory_classified"] is True
    assert decision["source_boundary_coverage"].startswith("7/7")
    assert decision["saturation_claim"] is False
    assert decision["exact_placeholder_free_candidate_located"] is False
    assert decision["exact_candidate_kernel_probed"] is False
    assert decision["root_machine_classification_before"] == decision["root_machine_classification_after"] == "M3"
    assert decision["root_vector_before"] == decision["root_vector_after"] == instance["root_vector"]
    assert decision["kernel_closed_as_accepted_root"] is False
    assert audit["accepted_receipt_ids"] == receipt["accepted_receipt_ids"] == []
    assert audit["audit_complete"] is receipt["audit_complete"] is False
    assert audit["theorem_complete"] is receipt["theorem_complete"] is False

    lean = subprocess.run(
        ["lake", "env", "lean", "../../Stage1_Instances/THM-M-0487/AnchorAudit.lean"],
        cwd=LEAN_ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=180,
        check=False,
    )
    if lean.returncode:
        sys.stdout.write(lean.stdout)
        raise SystemExit(lean.returncode)
    for declaration in support["declarations"]:
        if declaration not in lean.stdout:
            sys.stdout.write(lean.stdout)
            raise SystemExit(f"missing Lean probe output for {declaration}")
    if "def Stage1Instances.THM_M_0487_AnchorAudit.ExactTarget : Prop" not in lean.stdout:
        sys.stdout.write(lean.stdout)
        raise SystemExit("missing printed exact target")
    if hashlib.sha256(lean.stdout.encode()).hexdigest() != LEAN_OUTPUT_SHA256:
        sys.stdout.write(lean.stdout)
        raise SystemExit("anchor Lean output changed")

    print(
        "check_anchor_audit: ok "
        "(THM-M-0487; 7 records; no exact placeholder-free candidate; "
        "root H1/M3/R3; audit_complete=false; theorem_complete=false)"
    )


if __name__ == "__main__":
    main()
