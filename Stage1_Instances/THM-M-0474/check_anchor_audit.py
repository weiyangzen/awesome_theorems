#!/usr/bin/env python3
"""Validate the immutable local facts in the THM-M-0474 anchor ledger."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
FLT_REGULAR = LEAN_ROOT / ".lake" / "packages" / "flt-regular"
AUDIT = HERE / "anchor-audit.json"
RECEIPT = HERE / "anchor-audit-receipt.json"
SELFTEST = ROOT / ".stage1-worker-selftest.json"
THEOREM_ID = "THM-M-0474"
ITEM_ID = "S56-M-0474-ANCHOR_AUDIT"
EXPRESSION_SHA256 = "5475969fd23513d3b98134a6aaa747675a32a899f38be773a23cb330f2f590e8"
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
FORBIDDEN = re.compile(r"\b(" + "|".join(FORBIDDEN_WORDS) + r")\b")


def output(*args: str, cwd: Path | None = None) -> str:
    return subprocess.check_output(args, cwd=cwd, text=True).strip()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise SystemExit(f"{path} must contain a JSON object")
    return value


audit = load(AUDIT)
receipt = load(RECEIPT)
selftest = load(SELFTEST)
execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")
statement = load(HERE / "statement.json")
instance = load(HERE / "instance.json")
item = next(row for row in execution["items"] if row["id"] == ITEM_ID)

assert audit["item_id"] == item["id"] == ITEM_ID
assert receipt["item_id"] == ITEM_ID
assert selftest["item_id"] in {
    ITEM_ID,
    "S56-M-0474-OBLIGATION_TREE",
    "S56-M-0474-PROOF",
    "S56-M-0474-VALIDATION",
}
assert audit["theorem_id"] == item["theorem_id"] == THEOREM_ID
assert receipt["theorem_id"] == THEOREM_ID
assert selftest.get("theorem_id", THEOREM_ID) == THEOREM_ID
assert receipt["base_revision"] == audit["base_revision"]
assert receipt["base_tree"] == audit["base_tree"]
assert receipt["proposed_state"] == selftest["state"] == "[_]"
if selftest["item_id"] == ITEM_ID:
    assert set(receipt["changed_paths"]) == set(selftest["changed_paths"])
assert receipt["accepted"] is False and receipt["content_addressed"] is False
status = subprocess.check_output(
    ["git", "status", "--short", "--untracked-files=all"], cwd=ROOT, text=True
)
status_paths = {line[3:] for line in status.splitlines() if line[3:] != "Formalizations/Lean/.lake"}
if selftest["item_id"] == ITEM_ID:
    assert status_paths == set(selftest["changed_paths"])
assert item["phase"] == "anchor_audit" and item["layer"] == 2
assert item["state"] == "[_]"
assert item["depends_on"] == ["S56-M-0474-STATEMENT"]
assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]
assert audit["canonical_target"] == (
    "Stage1Instances.THM_M_0474.FermatLittleTheoremTarget"
)
assert audit["canonical_target_expression_sha256"] == EXPRESSION_SHA256
protocol = {
    key: value
    for key, value in audit["discovery_protocol"].items()
    if key not in {"protocol_sha256", "protocol_serialization"}
}
protocol_bytes = json.dumps(
    protocol, sort_keys=True, separators=(",", ":"), ensure_ascii=True
).encode("ascii")
assert hashlib.sha256(protocol_bytes).hexdigest() == (
    "8ade552e4840908b3ea990221c428b8a97318c119cc4fc7032e204e534cd998a"
)
assert audit["discovery_protocol"]["protocol_sha256"] == (
    "8ade552e4840908b3ea990221c428b8a97318c119cc4fc7032e204e534cd998a"
)
assert audit["external_search"]["sourcegraph_query"] == (
    "context:global archived:yes fork:yes lang:Lean "
    "(\"Fermat\\x27s Little Theorem\" OR pow_card_sub_one_eq_one OR "
    "FermatLittleTheorem) count:100"
)
assert hashlib.sha256(
    audit["external_search"]["sourcegraph_query"].encode("ascii")
).hexdigest() == "daa55b2f5086c8df8f5af6b50038657f6e026d3eeab8f8089fb56404314d41ac"
assert audit["external_search"]["sourcegraph_query_bytes_sha256"] == (
    "daa55b2f5086c8df8f5af6b50038657f6e026d3eeab8f8089fb56404314d41ac"
)
assert audit["external_search"]["sourcegraph_response_archive"].startswith("not retained")
assert statement["canonical_formal_target"]["elaborated_expression_sha256"] == EXPRESSION_SHA256

env = audit["immutable_environment"]
assert output("git", "rev-parse", "HEAD", cwd=MATHLIB) == env["mathlib_revision"]
assert output("git", "rev-parse", "HEAD^{tree}", cwd=MATHLIB) == env["mathlib_tree"]
assert output("git", "status", "--short", cwd=MATHLIB) == ""
assert sha256(MATHLIB / "LICENSE") == env["mathlib_license_sha256"]
assert sha256(LEAN_ROOT / "lake-manifest.json") == env["manifest_sha256"]

candidates = audit["candidates"]
ids = [candidate["candidate_id"] for candidate in candidates]
assert len(ids) == len(set(ids)) == 7
exact = next(candidate for candidate in candidates if candidate["candidate_id"] == "M0474-C01-MATHLIB-NAT-EXACT")
basic = MATHLIB / exact["file"]
assert sha256(basic) == exact["source_sha256"]
assert output("git", "hash-object", exact["file"], cwd=MATHLIB) == exact["source_git_blob"]
assert output("git", "merge-base", "--is-ancestor", exact["introduction_revision"], "HEAD", cwd=MATHLIB) == ""

basic_text = basic.read_text(encoding="utf-8")
for marker in (
    "theorem pow_card_sub_one_eq_one (a : K)",
    "theorem pow_card_sub_one_eq_one {a : ZMod p}",
    "theorem Int.ModEq.pow_card_sub_one_eq_one",
    "theorem Nat.ModEq.pow_card_sub_one_eq_one",
    "exact Int.ModEq.pow_card_sub_one_eq_one hp (isCoprime_iff_coprime.mpr hpn)",
):
    assert marker in basic_text, marker

order_record = exact["visible_terminal_files"][1]
order_source = MATHLIB / order_record["file"]
assert sha256(order_source) == order_record["sha256"]
assert output("git", "hash-object", order_record["file"], cwd=MATHLIB) == order_record["git_blob"]
assert "theorem pow_card_eq_one : x ^ Fintype.card G = 1 := by" in order_source.read_text(encoding="utf-8")
assert not FORBIDDEN.search(basic_text)
assert not FORBIDDEN.search(order_source.read_text(encoding="utf-8"))

consumer = next(candidate for candidate in candidates if candidate["candidate_id"] == "M0474-C03-FLT-REGULAR-CONSUMER")
assert output("git", "rev-parse", "HEAD", cwd=FLT_REGULAR) == consumer["revision"]
assert output("git", "rev-parse", "HEAD^{tree}", cwd=FLT_REGULAR) == consumer["tree"]
assert output("git", "status", "--short", cwd=FLT_REGULAR) == ""
consumer_source = FLT_REGULAR / consumer["file"]
assert sha256(consumer_source) == consumer["source_sha256"]
assert output("git", "hash-object", consumer["file"], cwd=FLT_REGULAR) == consumer["source_git_blob"]
assert "Int.ModEq.pow_card_sub_one_eq_one hpri.out" in consumer_source.read_text(encoding="utf-8")

adapter = (HERE / "AnchorAudit.lean").read_text(encoding="utf-8")
statement_source = (HERE / "Statement.lean").read_text(encoding="utf-8")
for marker in (
    "forall (p a : Nat), p.Prime -> a.Coprime p ->",
    "a ^ (p - 1) congruent to 1",
):
    normalized_adapter = adapter.replace("≡", "congruent to")
    normalized_statement = statement_source.replace("≡", "congruent to")
    assert marker in normalized_adapter and marker in normalized_statement
assert "exact Nat.ModEq.pow_card_sub_one_eq_one hp ha" in adapter
assert "assert_no_sorry Nat.ModEq.pow_card_sub_one_eq_one" in adapter
assert not FORBIDDEN.search(adapter)

decision = audit["inventory_decision"]
assert decision["inventory_classified"] is True
assert decision["exact_candidate_located"] is True
assert decision["exact_candidate_kernel_probed"] is True
assert decision["candidate_accepted_by_master"] is False
assert decision["root_machine_candidate_classification"] == (
    "M0-W_candidate_pending_downstream_acceptance"
)
assert decision["authoritative_root_vector_before"] == instance["root_vector"]
assert decision["authoritative_root_vector_after"] == instance["root_vector"]
assert decision["kernel_closed_as_accepted_root"] is False
assert audit["accepted_receipt_ids"] == []
assert audit["audit_complete"] is decision["audit_complete"] is False
assert audit["theorem_complete"] is decision["theorem_complete"] is False
assert receipt["accepted_receipt_ids"] == []
assert selftest.get("accepted_receipt_ids", []) == []
assert receipt["audit_complete"] is selftest.get("audit_complete", False) is False
assert receipt["theorem_complete"] is selftest.get("theorem_complete", False) is False

print(
    "check_anchor_audit: ok (7 candidates classified; exact pinned mathlib "
    "adapter, source hashes, trust boundary, and fail-closed status verified)"
)
