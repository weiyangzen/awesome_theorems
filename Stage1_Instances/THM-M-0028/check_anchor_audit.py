#!/usr/bin/env python3
"""Validate the immutable, locally checkable THM-M-0028 anchor ledger."""

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
ITEM_ID = "S56-M-0028-ANCHOR_AUDIT"
THEOREM_ID = "THM-M-0028"
BASE_REVISION = "7e54c0fcaf9c0e53fa7afbbeb0a36218152f932c"
BASE_TREE = "80ece87e35401b07ba76abc36ea83440b5fa7f31"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
EXPRESSION_SHA256 = "89e7e911ed4a5b75c153d824133091ad74ba20a0ecab19bd609b23a54badbee4"
STATEMENT_SHA256 = "db7cbc8250aa905f1d8a2686ab14e9b31eeeba3409179d22e7169627df02f3a7"
LEAN_OUTPUT_SHA256 = "b099c3dcca75b288d619b7d78dbce9c36ca849df14ade18b4ce5e993364bb223"
ATLAS_REVISION = "34ffed396f376454c1a9b297f3fd74c5c801fb50"
ATLAS_TREE = "c12fe2315fe475d70a4fcee81d6b731f853373ab"
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
    assert audit["execution_rank"] == 1073
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
    assert receipt["external_candidate_result"]["classification"] == "M1"
    assert receipt["external_candidate_result"]["in_dependency_closure"] is False
    assert receipt["external_candidate_result"]["license_approved_for_integration"] is False
    assert receipt["lean_output_sha256"] == LEAN_OUTPUT_SHA256
    assert receipt["audit_complete"] is False and receipt["theorem_complete"] is False
    if packet is not None:
        assert set(packet) == {
            "item_id", "changed_paths", "commands", "output_summary",
            "base_revision", "known_failures", "state",
        }
        assert packet["item_id"] == ITEM_ID and packet["state"] == "[_]"
        assert packet["base_revision"] == BASE_REVISION
        assert set(packet["changed_paths"]) == CHANGED_PATHS
        assert packet["known_failures"] == receipt["known_failures"]

    target = next(row for row in manifest["targets"] if row["theorem_id"] == THEOREM_ID)
    assert target["execution_rank"] == 1073
    assert target["baseline"] == "L0" and target["rework_required"] is True
    assert target["theorem_complete"] is False
    item = next(row for row in execution["items"] if row["id"] == ITEM_ID)
    assert item["phase"] == "anchor_audit" and item["layer"] == 2
    assert item["state"] in {"[ ]", "[_]"}
    assert item["depends_on"] == ["S56-M-0028-STATEMENT"]
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]

    assert audit["canonical_target_expression_sha256"] == EXPRESSION_SHA256
    assert audit["canonical_statement_file_sha256"] == STATEMENT_SHA256
    assert sha256(HERE / "Statement.lean") == STATEMENT_SHA256
    formal = statement["canonical_formal_target"]
    assert formal["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert formal["statement_file_sha256"] == STATEMENT_SHA256
    assert instance["anchor_audit"]["item_id"] == ITEM_ID
    assert instance["anchor_audit"]["candidate_classification"] == "M0-W"
    assert instance["anchor_audit"]["external_classification"] == "M1"
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
    assert len(candidate_ids) == len(set(candidate_ids)) == 4
    direct = next(c for c in candidates if c["candidate_id"] == "M0028-C01-MATHLIB-COMPOSITION")
    assert direct["revision"] == MATHLIB_REVISION and direct["tree"] == MATHLIB_TREE
    assert direct["file_blob"] == output("git", "rev-parse", f"HEAD:{direct['file']}", cwd=MATHLIB)
    source_path = MATHLIB / direct["file"]
    assert sha256(source_path) == direct["file_sha256"]
    lines = source_path.read_bytes().splitlines(keepends=True)
    body = b"".join(lines[158:162]) + b"".join(lines[192:204])
    assert sha256_bytes(body) == direct["body_sha256"]
    assert direct["declarations"] == [
        "monotone_stabilizes_iff_noetherian", "isNoetherianRing_iff_ideal_fg"
    ]
    assert direct["classification"] == "M0-W" and direct["evidence_level"] == "E2"
    history = direct["historical_provenance"]
    for key in ("lean4_port_commit", "current_defs_split_commit"):
        assert output(
            "git", "merge-base", "--is-ancestor", history[key], MATHLIB_REVISION, cwd=MATHLIB
        ) == ""
    assert history["lean4_port_tree"] == output(
        "git", "rev-parse", f"{history['lean4_port_commit']}^{{tree}}", cwd=MATHLIB
    )
    assert history["current_defs_split_tree"] == output(
        "git", "rev-parse", f"{history['current_defs_split_commit']}^{{tree}}", cwd=MATHLIB
    )

    source = source_path.read_text(encoding="utf-8")
    for marker in (
        "theorem isNoetherian_iff'",
        "theorem monotone_stabilizes_iff_noetherian",
        "rw [isNoetherian_iff', wellFoundedGT_iff_monotone_chain_condition]",
        "theorem isNoetherianRing_iff_ideal_fg",
        "isNoetherianRing_iff.trans isNoetherian_def",
    ):
        assert marker in source, marker
    support = direct["support_boundary"]
    support_path = MATHLIB / support["file"]
    assert support["file_blob"] == output("git", "rev-parse", f"HEAD:{support['file']}", cwd=MATHLIB)
    assert support["file_sha256"] == sha256(support_path)
    assert "theorem wellFoundedGT_iff_monotone_chain_condition" in support_path.read_text(encoding="utf-8")

    atlas = next(c for c in candidates if c["candidate_id"] == "M0028-C02-ATLAS-EXACT-BICONDITIONAL")
    assert atlas["revision"] == ATLAS_REVISION and atlas["tree"] == ATLAS_TREE
    assert atlas["file_blob"] == "94dcebdb5ab4da6358f7bf3f44e9c7205c58dd0d"
    assert atlas["file_sha256"] == "167d06009cde5f2f64b74883f9b5c23ba5c17292eb9cc4eb9f820976037bf13c"
    assert atlas["declaration"] == "noetherian_fg_iff_acc"
    assert atlas["classification"] == "M1" and atlas["evidence_level"] == "E2"
    assert "not in the local dependency closure" in atlas["classification_boundary"]
    assert "no-training" in atlas["license"]
    atlas_support = next(
        c for c in candidates if c["candidate_id"] == "M0028-C03-ATLAS-NOETHERIAN-PREDICATE"
    )
    assert atlas_support["revision"] == ATLAS_REVISION and atlas_support["tree"] == ATLAS_TREE
    assert atlas_support["classification"] == "M3_deduplicated_wrapper"
    assert atlas_support["file_blob"] == "24d85b76caf8a59ec321c32e31fd211f5325aaf6"

    adapter = (HERE / "AnchorAudit.lean").read_text(encoding="utf-8")
    for marker in (
        "def ExactTarget : Prop",
        "(forall I : Ideal R, I.FG) ->",
        "forall f : Nat →o Ideal R",
        "theorem exactTarget_mathlib_candidate : ExactTarget",
        "(isNoetherianRing_iff_ideal_fg R).mpr hfg",
        "monotone_stabilizes_iff_noetherian.mpr hNoetherian f",
        "#print sorries monotone_stabilizes_iff_noetherian",
        "#print sorries exactTarget_mathlib_candidate",
        "#print axioms exactTarget_mathlib_candidate",
    ):
        assert marker in adapter, marker
    forbidden = re.compile(r"\b(?:sorry|admit|sorryAx|axiom|unsafe|opaque|proof_wanted)\b")
    assert not forbidden.search(without_comments(adapter))
    assert not forbidden.search(without_comments(source))

    result = audit["audit_result"]
    assert result["inventory_classified"] is True
    assert result["source_boundary_coverage"].startswith("4/4 frozen candidates")
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
        ["lake", "env", "lean", "../../Stage1_Instances/THM-M-0028/AnchorAudit.lean"],
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
    if lean.stdout.count("Declarations are sorry-free!") != 3:
        sys.stdout.write(lean.stdout)
        raise SystemExit("expected three machine-produced sorry-free reports")
    normalized = re.sub(r"\s+", " ", lean.stdout)
    if normalized.count("propext, Classical.choice, Quot.sound") != 2:
        sys.stdout.write(lean.stdout)
        raise SystemExit("unexpected terminal or wrapper axiom report")
    if "'isNoetherianRing_iff_ideal_fg' depends on axioms: [propext, Quot.sound]" not in lean.stdout:
        sys.stdout.write(lean.stdout)
        raise SystemExit("finite-generation bridge axiom report changed")
    if "theorem monotone_stabilizes_iff_noetherian" not in lean.stdout:
        sys.stdout.write(lean.stdout)
        raise SystemExit("chain theorem body was not printed")
    if "theorem isNoetherianRing_iff_ideal_fg" not in lean.stdout:
        sys.stdout.write(lean.stdout)
        raise SystemExit("finite-generation bridge body was not printed")
    exact_target = re.search(
        r"def Stage1Instances\.THM_M_0028_AnchorAudit\.ExactTarget\.\{u\} : Prop :=\n"
        r"(?P<expression>.*)\Z",
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
        "(THM-M-0028; 4 candidates classified; exact pinned mathlib composition M0-W/E2; "
        "Atlas exact wrapper M1/E2; accepted root remains M3; "
        "audit_complete=false; theorem_complete=false)"
    )


if __name__ == "__main__":
    main()
