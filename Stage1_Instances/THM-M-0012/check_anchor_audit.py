#!/usr/bin/env python3
"""Validate the immutable, locally checkable THM-M-0012 anchor ledger."""

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
AUDIT_PATH = HERE / "anchor-audit.json"
ITEM_ID = "S56-M-0012-ANCHOR_AUDIT"
THEOREM_ID = "THM-M-0012"
BASE_REVISION = "02cc55f883d5b5d091ead6851bffe89199eb8391"
BASE_TREE = "035212d041a1e61553b3d2f465964c9bbb35e47d"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
EXPRESSION_SHA256 = "d14207f425a984b6daefaa986d8351a1543f58b7631d1c842e51a3ef2392ba74"
STATEMENT_SHA256 = "fce52766380ace58b4b202f267b8a3640f74655d0cacdea897de01bcf956ee46"
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM_ID}/AnchorAudit.lean",
    f"Stage1_Instances/{THEOREM_ID}/anchor-audit-receipt.json",
    f"Stage1_Instances/{THEOREM_ID}/anchor-audit-validation.md",
    f"Stage1_Instances/{THEOREM_ID}/anchor-audit.json",
    f"Stage1_Instances/{THEOREM_ID}/check_anchor_audit.py",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


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
    audit = load(AUDIT_PATH)
    receipt = load(HERE / "anchor-audit-receipt.json")
    statement = load(HERE / "statement.json")
    manifest = load(ROOT / "Docs" / "Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")
    packet_path = ROOT / ".stage1-worker-selftest.json"
    packet = load(packet_path) if packet_path.exists() else None

    assert audit["schema_version"] == "stage1-anchor-audit/1.0"
    assert audit["item_id"] == ITEM_ID and audit["theorem_id"] == THEOREM_ID
    assert audit["execution_rank"] == 1062
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
    assert receipt["lean_output_sha256"] == "3bf558a658747c81577bcf32a3690737ed5b0a27e4e5fbd7553620c3d7850148"
    assert receipt["audit_complete"] is False and receipt["theorem_complete"] is False
    if packet is not None:
        assert packet["item_id"] == ITEM_ID and packet["state"] == "[_]"
        assert packet["base_revision"] == BASE_REVISION
        assert set(packet["changed_paths"]) == CHANGED_PATHS
        assert packet["known_failures"] == receipt["known_failures"]

    target = next(row for row in manifest["targets"] if row["theorem_id"] == THEOREM_ID)
    assert target["execution_rank"] == 1062
    assert target["baseline"] == "L0" and target["rework_required"] is True
    assert target["theorem_complete"] is False
    item = next(row for row in execution["items"] if row["id"] == ITEM_ID)
    assert item["phase"] == "anchor_audit" and item["layer"] == 2
    assert item["state"] in {"[ ]", "[_]"}
    assert item["depends_on"] == ["S56-M-0012-STATEMENT"]
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]

    assert audit["canonical_target_expression_sha256"] == EXPRESSION_SHA256
    assert audit["canonical_statement_file_sha256"] == STATEMENT_SHA256
    assert sha256(HERE / "Statement.lean") == STATEMENT_SHA256
    formal = statement["canonical_formal_target"]
    assert formal["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert formal["statement_file_sha256"] == STATEMENT_SHA256

    env = audit["immutable_environment"]
    assert env["mathlib_revision"] == MATHLIB_REVISION
    assert env["mathlib_tree"] == MATHLIB_TREE
    assert output("git", "rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert output("git", "rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert output("git", "status", "--short", cwd=MATHLIB) == ""
    assert sha256(MATHLIB / "LICENSE") == env["mathlib_license_sha256"]
    assert sha256(LEAN_ROOT / "lake-manifest.json") == env["manifest_sha256"]

    direct = next(c for c in audit["candidates"] if c["candidate_id"] == "M0012-C01-MATHLIB-DIRECT")
    assert direct["revision"] == MATHLIB_REVISION and direct["tree"] == MATHLIB_TREE
    assert direct["file_blob"] == output("git", "rev-parse", f"HEAD:{direct['file']}", cwd=MATHLIB)
    assert sha256(MATHLIB / direct["file"]) == direct["file_sha256"]
    assert direct["declaration"] == "Complex.exists_root"
    assert direct["candidate_classification"] == "M0-W"
    assert direct["evidence_level"] == "E2"
    for revision in direct["historical_provenance"].values():
        if not isinstance(revision, str) or len(revision) != 40:
            continue
        assert output("git", "merge-base", "--is-ancestor", revision, MATHLIB_REVISION, cwd=MATHLIB) == ""

    source = (MATHLIB / direct["file"]).read_text(encoding="utf-8")
    for marker in (
        "theorem exists_root {f : ℂ[X]}",
        "by_contra! hf'",
        "(f.differentiable.inv hf').apply_eq_of_tendsto_cocompact",
        "using f.tendsto_norm_atTop",
        "obtain rfl : f = C 0 := Polynomial.funext",
        "instance isAlgClosed : IsAlgClosed ℂ",
        "Complex.exists_root <| degree_pos_of_irreducible hp",
    ):
        assert marker in source, marker

    support = next(c for c in audit["candidates"] if c["candidate_id"] == "M0012-C02-MATHLIB-ALGEBRAIC-CLOSURE")
    generic = MATHLIB / support["generic_source"]
    assert output("git", "rev-parse", f"HEAD:{support['generic_source']}", cwd=MATHLIB) == support["generic_source_blob"]
    assert sha256(generic) == support["generic_source_sha256"]
    assert "theorem exists_root [IsAlgClosed k]" in generic.read_text(encoding="utf-8")

    documentation = next(c for c in audit["candidates"] if c["candidate_id"] == "M0012-C03-READ-LEAN-DOCUMENTATION")
    assert documentation["candidate_classification"] == "M3_documentation_only"
    assert documentation["revision"] == "ad424b95eba1c815823f295df8eec963d4c57acb"
    assert documentation["readme_sha256"] == "de11b90ac2d95ee703dae614feed780e18078975dc0317326705f7d7094507e1"
    assert documentation["lean_source_sha256"] == "81b3580c63dfcb2152d4836f1dcb8920fb5535357db65782b396eaa06c36e644"

    adapter = (HERE / "AnchorAudit.lean").read_text(encoding="utf-8")
    for marker in (
        "def ExactTarget : Prop",
        "forall f : Polynomial Complex, Nonconstant f ->",
        "theorem exactTarget_mathlib_candidate : ExactTarget",
        "apply Complex.exists_root",
        "eq_C_of_degree_le_zero hdegree",
        "#print axioms Complex.exists_root",
        "#print axioms IsAlgClosed.exists_root",
        "#print axioms exactTarget_mathlib_candidate",
    ):
        assert marker in adapter, marker
    forbidden = re.compile(r"\b(?:sorry|admit|sorryAx|axiom|unsafe|opaque)\b")
    assert not forbidden.search(without_comments(adapter))
    assert not forbidden.search(without_comments(source[0:source.index("end Complex")]))

    result = audit["audit_result"]
    assert result["inventory_classified"] is True
    assert result["source_boundary_coverage"].startswith("3/3 classified candidates")
    assert result["exact_candidate_located"] is True
    assert result["candidate_kernel_checked"] is True
    assert result["candidate_accepted_by_master"] is False
    assert result["root_machine_debt_before"] == "M3"
    assert result["root_machine_candidate_after"] == "M0-W"
    assert result["accepted_root_machine_debt_after"] == "M3"
    assert result["root_evidence_level"] == "E2"
    assert result["audit_complete"] is False and result["theorem_complete"] is False
    assert audit["discovery_protocol"]["saturation_claim"] is False

    lean = subprocess.run(
        ["lake", "env", "lean", "../../Stage1_Instances/THM-M-0012/AnchorAudit.lean"],
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
    if normalized.count("propext, Classical.choice, Quot.sound") != 4:
        sys.stdout.write(lean.stdout)
        raise SystemExit("unexpected candidate axiom report")
    if "theorem Complex.exists_root" not in lean.stdout or "theorem Complex.isAlgClosed" not in lean.stdout:
        sys.stdout.write(lean.stdout)
        raise SystemExit("candidate proof-body print is missing")
    if "sorry" in lean.stdout:
        sys.stdout.write(lean.stdout)
        raise SystemExit("Lean output contains a proof placeholder")
    if hashlib.sha256(lean.stdout.encode()).hexdigest() != receipt["lean_output_sha256"]:
        sys.stdout.write(lean.stdout)
        raise SystemExit("candidate Lean output changed")

    print(
        "check_anchor_audit: ok "
        "(THM-M-0012; 3 candidates; exact pinned mathlib wrapper M0-W/E2; "
        "accepted root remains M3; audit_complete=false; theorem_complete=false)"
    )


if __name__ == "__main__":
    main()
