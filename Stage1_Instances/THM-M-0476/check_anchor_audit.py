#!/usr/bin/env python3
"""Validate the immutable local evidence for the THM-M-0476 anchor audit."""

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
THEOREM_ID = "THM-M-0476"
ITEM_ID = "S56-M-0476-ANCHOR_AUDIT"
BASE_REVISION = "db4b8793e70ce8af74c9c9490acfa50aa3684d5e"
BASE_TREE = "6434a20532ae7c523ad293e67a6228ab384bfb8a"
EXPRESSION_SHA256 = "ee76edb160426d3e8d95b11bfedca7febcfe915f50007e042875c922ebc8a4ac"
STATEMENT_SHA256 = "3903de3f1e1cdd6d2f048917005da8f2b744d6726507d09120661e79d217dff9"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
LEAN_OUTPUT_SHA256 = "7140ce7219450a2ff7e96017cc575988989901f60b8c2a3798eb25317660480e"
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
    assert audit["item_id"] == protocol["item_id"] == receipt["item_id"] == ITEM_ID
    assert audit["theorem_id"] == protocol["theorem_id"] == receipt["theorem_id"] == THEOREM_ID
    assert audit["execution_rank"] == 1357
    assert audit["base_revision"] == receipt["base_revision"] == BASE_REVISION
    assert audit["base_tree"] == receipt["base_tree"] == BASE_TREE
    current_revision = output("git", "rev-parse", "HEAD")
    current_tree = output("git", "rev-parse", "HEAD^{tree}")
    assert packet["item_id"] in {
        ITEM_ID,
        "S56-M-0476-OBLIGATION_TREE",
        "S56-M-0476-PROOF",
        "S56-M-0476-VALIDATION",
    }
    assert packet["state"] == "[_]"
    if packet["item_id"] == ITEM_ID:
        assert current_revision == BASE_REVISION and current_tree == BASE_TREE
        assert packet["base_revision"] == BASE_REVISION
        assert set(packet["changed_paths"]) == set(receipt["changed_paths"]) == CHANGED_PATHS
        assert packet["known_failures"] == receipt["known_failures"]
    else:
        assert packet["base_revision"] == current_revision
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False

    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM_ID)
    item = next(row for row in execution["items"] if row["id"] == ITEM_ID)
    assert target["execution_rank"] == 1357
    assert target["baseline"] == "L0" and target["rework_required"] is True
    assert target["theorem_complete"] is False
    assert item["phase"] == "anchor_audit" and item["layer"] == 2
    assert item["depends_on"] == ["S56-M-0476-STATEMENT"]
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]

    assert audit["canonical_target_expression_sha256"] == EXPRESSION_SHA256
    assert audit["canonical_statement_file_sha256"] == STATEMENT_SHA256
    assert sha256(HERE / "Statement.lean") == STATEMENT_SHA256
    formal = statement["canonical_formal_target"]
    assert formal["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert formal["statement_file_sha256"] == STATEMENT_SHA256
    assert instance["root_vector"] == {"H": "H1", "M": "M3", "R": "R4"}

    assert protocol["protocol_id"] == "S56-M-0476-ANCHOR-DISCOVERY-20260713-01"
    assert protocol["saturation_claim"] is False
    assert len(protocol["aliases"]) >= 8 and len(protocol["surfaces"]) >= 7
    assert sha256(HERE / "anchor-discovery-protocol.json") == (
        "2069bfed989cf0d0f8198d6e0a30a99dd84f0ea3442e5765040ea98f5cdac042"
    )

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
    assert len(candidate_ids) == len(set(candidate_ids)) == 7
    direct = next(c for c in candidates if c["candidate_id"] == "M0476-C01-MATHLIB-DIRECT")
    assert direct["revision"] == MATHLIB_REVISION and direct["tree"] == MATHLIB_TREE
    assert direct["terminal_declaration"] == "ZMod.wilsons_lemma"
    assert direct["local_role"] == "audit-only exact wrapper candidate"
    assert direct["terminal_proof_body_id"] == (
        "git-blob:9401f7b96b43c2c0afa1f823857bd31a20ae0ac2:ZMod.wilsons_lemma"
    )
    assert len(direct["direct_proof_dependencies"]) >= 6
    assert direct["direct_module_imports"] == ["Mathlib.FieldTheory.Finite.Basic"]
    assert direct["machine_axioms"] == ["propext", "Classical.choice", "Quot.sound"]
    wilson = MATHLIB / direct["file"]
    assert sha256(wilson) == direct["source_sha256"]
    assert output("git", "rev-parse", f"HEAD:{direct['file']}", cwd=MATHLIB) == direct["source_git_blob"]
    body_slice = b"".join(wilson.read_bytes().splitlines(keepends=True)[42:68])
    assert hashlib.sha256(body_slice).hexdigest() == direct["proof_body_slice_sha256"]
    assert output(
        "git", "merge-base", "--is-ancestor", direct["introduction_revision"], "HEAD", cwd=MATHLIB
    ) == ""
    wilson_source = wilson.read_text(encoding="utf-8")
    for marker in (
        "theorem wilsons_lemma : ((p - 1)! : ZMod p) = -1 := by",
        "Finset.prod_Ico_id_eq_factorial",
        "prod_univ_units_id_eq_neg_one",
        "theorem prod_Ico_one_prime",
        "theorem prime_of_fac_equiv_neg_one",
        "theorem prime_iff_fac_equiv_neg_one",
        "exact ZMod.wilsons_lemma n",
    ):
        assert marker in wilson_source, marker
    assert not FORBIDDEN.search(without_comments(wilson_source))

    support = next(c for c in candidates if c["candidate_id"] == "M0476-C03-MATHLIB-SUPPORT")
    support_source = MATHLIB / support["file"]
    assert sha256(support_source) == support["source_sha256"]
    assert output("git", "rev-parse", f"HEAD:{support['file']}", cwd=MATHLIB) == support["source_git_blob"]
    assert "theorem prod_univ_units_id_eq_neg_one" in support_source.read_text(encoding="utf-8")

    external = next(c for c in candidates if c["candidate_id"] == "M0476-C04-ADIMCHIMMA-INT-MODEQ")
    assert external["revision"] == "441b532e68f39d1d46636be8619d3349a80f253e"
    assert external["tree"] == "82a1cac0594c2d5d2cb92c51c9af0aec83f04200"
    assert external["source_git_blob"] == "7da68f757fa0b45eb9484ab5075f93b32712fde0"
    assert external["source_sha256"] == "982a9129064f60c223cdd4ff831cf66451b30264e7c3b9a2f4b9d1c747ba551e"
    assert external["candidate_machine_classification"] == "M3_related_external_not_integrated"

    adapter = (HERE / "AnchorAudit.lean").read_text(encoding="utf-8")
    for marker in (
        "def ExactTarget : Prop",
        "forall (p : Nat), p.Prime -> ((p - 1)! : ZMod p) = -1",
        "theorem exactTarget_mathlib_candidate : ExactTarget := by",
        "letI : Fact p.Prime := ⟨hp⟩",
        "exact ZMod.wilsons_lemma p",
        "#print sorries ZMod.wilsons_lemma",
        "#print sorries exactTarget_mathlib_candidate",
        "#print axioms exactTarget_mathlib_candidate",
    ):
        assert marker in adapter, marker
    assert not FORBIDDEN.search(without_comments(adapter))

    decision = audit["inventory_decision"]
    assert decision["inventory_classified"] is True
    assert decision["source_boundary_coverage"].startswith("7/7")
    assert decision["exact_candidate_located"] is True
    assert decision["exact_candidate_kernel_probed"] is True
    assert decision["candidate_accepted_by_master"] is False
    assert decision["root_machine_candidate_classification"] == (
        "M0-W_candidate_pending_downstream_acceptance"
    )
    assert decision["authoritative_root_vector_before"] == instance["root_vector"]
    assert decision["authoritative_root_vector_after"] == instance["root_vector"]
    assert decision["kernel_closed_as_accepted_root"] is False
    assert audit["accepted_receipt_ids"] == receipt["accepted_receipt_ids"] == []
    assert audit["audit_complete"] is receipt["audit_complete"] is False
    assert audit["theorem_complete"] is receipt["theorem_complete"] is False

    lean = subprocess.run(
        ["lake", "env", "lean", "../../Stage1_Instances/THM-M-0476/AnchorAudit.lean"],
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
    normalized = re.sub(r"\s+", " ", lean.stdout)
    if normalized.count("depends on axioms: [propext, Classical.choice, Quot.sound]") != 6:
        sys.stdout.write(lean.stdout)
        raise SystemExit("unexpected candidate axiom report")
    if lean.stdout.count("Declarations are sorry-free!") != 2:
        sys.stdout.write(lean.stdout)
        raise SystemExit("unexpected transitive sorry report")
    if hashlib.sha256(lean.stdout.encode()).hexdigest() != LEAN_OUTPUT_SHA256:
        sys.stdout.write(lean.stdout)
        raise SystemExit("candidate Lean output changed")

    print(
        "check_anchor_audit: ok "
        "(THM-M-0476; 7 records; exact pinned mathlib adapter; "
        "candidate M0-W, accepted root H1/M3/R4; audit_complete=false; theorem_complete=false)"
    )


if __name__ == "__main__":
    main()
