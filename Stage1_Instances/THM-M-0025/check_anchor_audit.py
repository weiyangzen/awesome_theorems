#!/usr/bin/env python3
"""Validate the immutable, locally checkable THM-M-0025 anchor ledger."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM_ID = "S56-M-0025-ANCHOR_AUDIT"
THEOREM_ID = "THM-M-0025"
BASE_REVISION = "94f6abf9359f26384e0f68bef694dc5b9aae624c"
BASE_TREE = "e0083f4f402c93febe4419b51498afa8ecf81c06"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
EXPRESSION_SHA256 = "9bb5ed6dd01550f3481d4a66e1d81009272b717997f9752ff422029da2828564"
STATEMENT_SHA256 = "d629f0c46384939ddcbaa4c35c3e1c75bb41d39ec3b79cb7355c174028186f6c"
LEAN_OUTPUT_SHA256 = "79b75df3fc67b8b32ef9b32a61fccc2bc9150bb866001c6350da1154ad2df223"
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM_ID}/AnchorAudit.lean",
    f"Stage1_Instances/{THEOREM_ID}/README.md",
    f"Stage1_Instances/{THEOREM_ID}/anchor-audit-receipt.json",
    f"Stage1_Instances/{THEOREM_ID}/anchor-audit-validation.md",
    f"Stage1_Instances/{THEOREM_ID}/anchor-audit.json",
    f"Stage1_Instances/{THEOREM_ID}/check_anchor_audit.py",
    f"Stage1_Instances/{THEOREM_ID}/instance.json",
    f"Stage1_Instances/{THEOREM_ID}/scope-map.md",
    f"Stage1_Instances/{THEOREM_ID}/source-statement-crosswalk.md",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def output(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(args, cwd=cwd, text=True).strip()


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise SystemExit(f"{path} must contain a JSON object")
    return value


def without_comments(source: str) -> str:
    source = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
    return re.sub(r"--.*", "", source)


def main() -> None:
    audit = load(HERE / "anchor-audit.json")
    receipt = load(HERE / "anchor-audit-receipt.json")
    statement = load(HERE / "statement.json")
    instance = load(HERE / "instance.json")
    manifest = load(ROOT / "Docs" / "Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")
    packet_path = ROOT / ".stage1-worker-selftest.json"
    packet = load(packet_path) if packet_path.exists() else None

    assert audit["schema_version"] == "stage1-anchor-audit/1.0"
    assert audit["item_id"] == ITEM_ID and audit["theorem_id"] == THEOREM_ID
    assert audit["execution_rank"] == 1070
    assert audit["base_revision"] == BASE_REVISION and audit["base_tree"] == BASE_TREE
    assert output("git", "rev-parse", "HEAD") == BASE_REVISION
    assert output("git", "rev-parse", "HEAD^{tree}") == BASE_TREE
    assert receipt["item_id"] == ITEM_ID and receipt["theorem_id"] == THEOREM_ID
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert set(receipt["changed_paths"]) == CHANGED_PATHS
    assert receipt["candidate_result"]["classification"] == "M0-W"
    assert receipt["candidate_result"]["evidence_level"] == "E2"
    assert receipt["candidate_result"]["master_accepted"] is False
    assert receipt["lean_output_sha256"] == LEAN_OUTPUT_SHA256
    assert receipt["audit_complete"] is False and receipt["theorem_complete"] is False
    if packet is not None:
        assert packet["item_id"] == ITEM_ID and packet["state"] == "[_]"
        assert packet["base_revision"] == BASE_REVISION
        assert set(packet["changed_paths"]) == CHANGED_PATHS
        assert packet["known_failures"] == receipt["known_failures"]

    target = next(row for row in manifest["targets"] if row["theorem_id"] == THEOREM_ID)
    assert target["execution_rank"] == 1070
    assert target["baseline"] == "L0" and target["rework_required"] is True
    assert target["theorem_complete"] is False
    item = next(row for row in execution["items"] if row["id"] == ITEM_ID)
    assert item["phase"] == "anchor_audit" and item["layer"] == 2
    assert item["state"] in {"[ ]", "[_]"}
    assert item["depends_on"] == ["S56-M-0025-STATEMENT"]
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]

    assert audit["canonical_target_expression_sha256"] == EXPRESSION_SHA256
    assert audit["canonical_statement_file_sha256"] == STATEMENT_SHA256
    assert sha256(HERE / "Statement.lean") == STATEMENT_SHA256
    formal = statement["canonical_formal_target"]
    assert formal["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert formal["statement_file_sha256"] == STATEMENT_SHA256
    assert instance["anchor_audit"]["item_id"] == ITEM_ID
    assert instance["anchor_audit"]["candidate_classification"] == "M0-W"
    assert instance["root_vector"] == {"H": "H1", "M": "M3", "R": "R3"}
    assert instance["audit_complete"] is False and instance["theorem_complete"] is False

    env = audit["immutable_environment"]
    assert env["mathlib_revision"] == MATHLIB_REVISION
    assert env["mathlib_tree"] == MATHLIB_TREE
    assert output("git", "rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert output("git", "rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert output("git", "status", "--short", cwd=MATHLIB) == ""
    assert sha256(MATHLIB / "LICENSE") == env["license_sha256"]
    assert sha256(LEAN_ROOT / "lake-manifest.json") == env["manifest_sha256"]

    candidates = audit["candidates"]
    candidate_ids = [candidate["candidate_id"] for candidate in candidates]
    assert len(candidate_ids) == len(set(candidate_ids)) == 3
    direct = next(c for c in candidates if c["candidate_id"] == "M0025-C01-MATHLIB-DIRECT")
    assert direct["revision"] == MATHLIB_REVISION and direct["tree"] == MATHLIB_TREE
    assert direct["file_blob"] == output("git", "rev-parse", f"HEAD:{direct['file']}", cwd=MATHLIB)
    source_path = MATHLIB / direct["file"]
    assert sha256(source_path) == direct["file_sha256"]
    lines = source_path.read_bytes().splitlines(keepends=True)
    body = b"".join(lines[731:806])
    helper_and_body = b"".join(lines[599:604]) + body
    assert sha256_bytes(body) == direct["body_sha256"]
    assert sha256_bytes(helper_and_body) == direct["helper_and_body_sha256"]
    assert direct["declaration"] == "Polynomial.isNoetherianRing"
    assert direct["classification"] == "M0-W" and direct["evidence_level"] == "E2"
    history = direct["historical_provenance"]
    assert history["lean4_port_tree"] == output(
        "git", "rev-parse", f"{history['lean4_port_commit']}^{{tree}}", cwd=MATHLIB
    )
    assert output(
        "git", "merge-base", "--is-ancestor",
        history["lean4_port_commit"], MATHLIB_REVISION, cwd=MATHLIB,
    ) == ""

    source = source_path.read_text(encoding="utf-8")
    for marker in (
        "protected theorem Polynomial.isNoetherianRing",
        "isNoetherianRing_iff.2",
        "inst.wf.min (Set.range I.leadingCoeffNth)",
        "let ⟨s, hs⟩ := I.is_fg_degreeLE N",
        "induction k using Nat.strong_induction_on",
        "Polynomial.degree_sub_lt",
        "attribute [instance] Polynomial.isNoetherianRing",
    ):
        assert marker in source, marker
    body_source = without_comments(body.decode("utf-8"))
    forbidden = re.compile(r"\b(?:sorry|admit|sorryAx|axiom|unsafe|opaque|proof_wanted)\b")
    assert not forbidden.search(body_source)

    adapter = (HERE / "AnchorAudit.lean").read_text(encoding="utf-8")
    for marker in (
        "def ExactTarget : Prop",
        "forall {R : Type u} [CommRing R] [IsNoetherianRing R]",
        "IsNoetherianRing (Polynomial R)",
        "theorem exactTarget_mathlib_candidate : ExactTarget",
        "exact Polynomial.isNoetherianRing",
        "#print sorries Polynomial.isNoetherianRing",
        "#print axioms exactTarget_mathlib_candidate",
    ):
        assert marker in adapter, marker
    assert not forbidden.search(without_comments(adapter))

    mismatch = next(c for c in candidates if c["candidate_id"] == "M0025-C03-POWER-SERIES-MISMATCH")
    assert mismatch["revision"] == "3599301fbaeb4fca4776ab9ae586af815610bbcf"
    assert mismatch["file_sha256"] == "9db647a46fe32113b419d3e83191a41727bff7173485fe63c14459d1fbc02072"
    assert mismatch["classification"] == "M5_statement_mismatch"
    assert "PowerSeries R" in mismatch["source_type"]

    result = audit["audit_result"]
    assert result["inventory_classified"] is True
    assert result["source_boundary_coverage"].startswith("3/3 frozen candidates")
    assert result["exact_candidate_located"] is True
    assert result["candidate_kernel_checked"] is True
    assert result["candidate_accepted_by_master"] is False
    assert result["root_machine_debt_before"] == "M3"
    assert result["root_machine_candidate_after"] == "M0-W"
    assert result["accepted_root_machine_debt_after"] == "M3"
    assert result["root_evidence_level"] == "E2"
    assert result["node_self_tested"] is True
    assert result["audit_complete"] is False and result["theorem_complete"] is False
    assert audit["discovery_protocol"]["saturation_claim"] is False

    lean = subprocess.run(
        ["lake", "env", "lean", "../../Stage1_Instances/THM-M-0025/AnchorAudit.lean"],
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
    if "Declarations are sorry-free!" not in lean.stdout:
        sys.stdout.write(lean.stdout)
        raise SystemExit("terminal declaration is not machine-reported sorry-free")
    normalized = re.sub(r"\s+", " ", lean.stdout)
    if normalized.count("propext, Classical.choice, Quot.sound") != 2:
        sys.stdout.write(lean.stdout)
        raise SystemExit("unexpected terminal or wrapper axiom report")
    if "protected theorem Polynomial.isNoetherianRing" not in lean.stdout:
        sys.stdout.write(lean.stdout)
        raise SystemExit("terminal proof body was not printed")
    exact_target = re.search(
        r"def Stage1Instances\.THM_M_0025_AnchorAudit\.ExactTarget\.\{u\} : Prop :=\n(?P<expression>.*)\Z",
        lean.stdout,
        re.DOTALL,
    )
    if exact_target is None:
        sys.stdout.write(lean.stdout)
        raise SystemExit("could not extract the audit target's explicit expression")
    if " ".join(exact_target.group("expression").split()) != formal["fully_explicit_expression"]:
        sys.stdout.write(lean.stdout)
        raise SystemExit("audit target is not expression-identical to the frozen statement")
    if hashlib.sha256(lean.stdout.encode()).hexdigest() != LEAN_OUTPUT_SHA256:
        sys.stdout.write(lean.stdout)
        raise SystemExit("candidate Lean output changed")

    print(
        "check_anchor_audit: ok "
        "(THM-M-0025; 3 candidates classified; exact pinned mathlib wrapper M0-W/E2; "
        "accepted root remains M3; audit_complete=false; theorem_complete=false)"
    )


if __name__ == "__main__":
    main()
