#!/usr/bin/env python3
"""Validate the immutable, target-owned THM-M-0822 anchor audit."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
AUDIT_PATH = HERE / "anchor-audit.json"
PROTOCOL_PATH = HERE / "anchor-discovery-protocol.json"
RECEIPT_PATH = HERE / "anchor-audit-receipt.json"
SOURCE = HERE / "AnchorAudit.lean"
STATEMENT_SOURCE = HERE / "Statement.lean"
STATEMENT_RECORD = HERE / "statement.json"
ITEM_ID = "S56-M-0822-ANCHOR_AUDIT"
THEOREM_ID = "THM-M-0822"
RANK = 1380
BASE_REVISION = "a1c9974d7fb28cd680e6494b968544bf801a93a2"
BASE_TREE = "1fa287bc821355aca2ca9e3ce107830a3eb58e64"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_FILE = "Mathlib/Combinatorics/SetFamily/KruskalKatona.lean"
MATHLIB_FILE_BLOB = "f388fc0bfd201e1d9eb1279b5bd1c6dcbd253b34"
MATHLIB_FILE_SHA256 = "c6351d7ee422db9eed8f45335f4128eb3a66fe09997d12abc15eba38e9863f1c"
MATHLIB_BLOCK_SHA256 = "bafaad9695ea929dc30acd5dbc1275c48eb5d062b99c56e0ddd2013374e783c0"
MATHLIB_INTRODUCTION = "174e4bd31d28b82604fc68a45c04fbc15140c394"
EXPRESSION_SHA256 = "646e9860afcf5efd962b6f69c9c2825220f23418d05f7675490b783e63afe209"
STATEMENT_SHA256 = "b91d0fce7cd10a12585860b11af519cbe7496f555d04a751d5b4b6309309582d"
PROTOCOL_SHA256 = "3fdc28d737cda0a60a0bcf42c598b6b15de4cfbcf0e80565ec2f691aa239b31f"
ANCHOR_SHA256 = "aa5e4a4a1f155c5913bc3e4b6fc135b9babe56f53dd7b1b950f4a437594b6426"
AUDIT_SHA256 = "380c1d6f3e10084bc82f24fca8a881a12fdc4794885b2e3f1ff7b5fd7985afee"
LEAN_OUTPUT_SHA256 = "7ba98b0926c0615ec57796af59ce0d29ebeef2db2da0011d701955401b754e97"
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM_ID}/AnchorAudit.lean",
    f"Stage1_Instances/{THEOREM_ID}/anchor-audit-receipt.json",
    f"Stage1_Instances/{THEOREM_ID}/anchor-audit-validation.md",
    f"Stage1_Instances/{THEOREM_ID}/anchor-audit.json",
    f"Stage1_Instances/{THEOREM_ID}/anchor-discovery-protocol.json",
    f"Stage1_Instances/{THEOREM_ID}/check_anchor_audit.py",
}
SOURCE_INPUTS = {
    "Docs/Stage1_Targets_rev-5.6.json": "Docs/Stage1_Targets_rev-5.6.json",
    "Docs/Stage1_Blueprint_rev-5.6.md": "Docs/Stage1_Blueprint_rev-5.6.md",
    "Docs/Stage1_Execution_DAG_rev-5.6.json": "Docs/Stage1_Execution_DAG_rev-5.6.json",
    "skills/execute-stage1-rev56/SKILL.md": "skills/execute-stage1-rev56/SKILL.md",
    "Formalizations/Lean/lean-toolchain": "Formalizations/Lean/lean-toolchain",
    "Formalizations/Lean/lake-manifest.json": "Formalizations/Lean/lake-manifest.json",
    f"Stage1_Instances/{THEOREM_ID}/Statement.lean": f"Stage1_Instances/{THEOREM_ID}/Statement.lean",
    f"Stage1_Instances/{THEOREM_ID}/statement.json": f"Stage1_Instances/{THEOREM_ID}/statement.json",
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


def check_text_file(path: Path) -> None:
    data = path.read_bytes()
    if not data.endswith(b"\n"):
        raise SystemExit(f"missing final newline: {path}")
    if b"\r" in data or b"\x00" in data:
        raise SystemExit(f"invalid byte in {path}")
    if any(line.endswith((b" ", b"\t")) for line in data.splitlines()):
        raise SystemExit(f"trailing whitespace in {path}")


def run_lean(path: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["lake", "env", "lean", str(path)],
        cwd=LEAN_ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=180,
        check=False,
    )


def source_block(source: str) -> str:
    start = source.index("/-- The **Erdős–Ko–Rado theorem**.")
    end = source.index("\nend Finset", start)
    return source[start:end] + "\n"


def combined_exact_check() -> str:
    statement = STATEMENT_SOURCE.read_text(encoding="utf-8")
    statement = statement.replace(
        "import Mathlib.Combinatorics.SetFamily.Intersecting\n",
        "import Mathlib.Combinatorics.SetFamily.KruskalKatona\n",
        1,
    )
    closing = "\nend Stage1Instances.THM_M_0822\n"
    if statement.count(closing) != 1:
        raise SystemExit("statement namespace boundary is missing or ambiguous")
    statement = statement.replace(closing, "\n", 1)
    combined = statement + """

/-- Checker-only exact composition of the frozen attainment and pinned upper bound. -/
theorem canonicalTarget_of_pinnedCandidate : ErdosKoRadoMaximumTarget := by
  intro n r hr hhalf
  exact ⟨erdosKoRadoStar_attains n r hr hhalf,
    fun A hIntersecting hSized =>
      Finset.erdos_ko_rado hIntersecting hSized hhalf⟩

#print axioms canonicalTarget_of_pinnedCandidate

end Stage1Instances.THM_M_0822
"""
    with tempfile.TemporaryDirectory(
        prefix="thm-m-0822-anchor-", dir=HERE
    ) as directory:
        path = Path(directory) / "CombinedAnchorAudit.lean"
        path.write_text(combined, encoding="utf-8")
        result = run_lean(path)
    if result.returncode:
        sys.stdout.write(result.stdout)
        raise SystemExit(result.returncode)
    expected = "[propext, Classical.choice, Quot.sound]"
    if expected not in re.sub(r"\s+", " ", result.stdout):
        sys.stdout.write(result.stdout)
        raise SystemExit("combined exact-root axiom report is missing")
    if "sorryAx" in result.stdout or "declaration uses 'sorry'" in result.stdout:
        sys.stdout.write(result.stdout)
        raise SystemExit("combined exact-root check reports a placeholder")
    return result.stdout


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker-packet", type=Path)
    args = parser.parse_args()

    audit = load(AUDIT_PATH)
    protocol = load(PROTOCOL_PATH)
    receipt = load(RECEIPT_PATH)
    statement = load(STATEMENT_RECORD)
    manifest = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")

    assert audit["schema_version"] == "stage1-anchor-audit/1.0"
    assert protocol["schema_version"] == "stage1-anchor-discovery-protocol/1.0"
    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert audit["item_id"] == protocol["item_id"] == receipt["item_id"] == ITEM_ID
    assert audit["theorem_id"] == protocol["theorem_id"] == receipt["theorem_id"] == THEOREM_ID
    assert audit["execution_rank"] == RANK
    assert audit["base_revision"] == protocol["base_revision"] == receipt["base_revision"] == BASE_REVISION
    assert audit["base_tree"] == protocol["base_tree"] == receipt["base_tree"] == BASE_TREE
    assert output("git", "rev-parse", "HEAD") == BASE_REVISION
    assert output("git", "rev-parse", "HEAD^{tree}") == BASE_TREE
    assert protocol["saturation_claim"] is False
    assert sha256(PROTOCOL_PATH) == PROTOCOL_SHA256
    assert audit["discovery_protocol_sha256"] == PROTOCOL_SHA256

    target = next(row for row in manifest["targets"] if row["theorem_id"] == THEOREM_ID)
    assert target["execution_rank"] == RANK
    assert target["name"] == "Erdős-Ko-Rado定理"
    assert target["baseline"] == "L0" and target["rework_required"] is True
    assert target["legacy_artifacts_accepted"] is False
    assert target["lifecycle_mode"] == "planned" and target["theorem_complete"] is False
    item = next(row for row in execution["items"] if row["id"] == ITEM_ID)
    assert item["phase"] == "anchor_audit" and item["layer"] == 2
    assert item["state"] == "[ ]"
    assert item["depends_on"] == ["S56-M-0822-STATEMENT"]
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]
    assert item["deliverable"] == "Audit mathlib and external Lean 4 candidates at immutable revisions."
    prerequisite = next(
        row for row in execution["items"] if row["id"] == "S56-M-0822-STATEMENT"
    )
    assert prerequisite["state"] == "[_]"

    formal = statement["canonical_formal_target"]
    assert formal["declaration_or_expression"] == (
        "Stage1Instances.THM_M_0822.ErdosKoRadoMaximumTarget"
    )
    assert formal["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert formal["statement_file_sha256"] == STATEMENT_SHA256
    assert sha256(STATEMENT_SOURCE) == STATEMENT_SHA256
    canonical = audit["canonical_target"]
    assert canonical["expression_sha256"] == EXPRESSION_SHA256
    assert canonical["statement_file_sha256"] == STATEMENT_SHA256
    assert sha256(SOURCE) == ANCHOR_SHA256
    assert sha256(AUDIT_PATH) == AUDIT_SHA256

    env = audit["immutable_environment"]
    assert env["mathlib_revision"] == MATHLIB_REVISION
    assert env["mathlib_tree"] == MATHLIB_TREE
    assert output("git", "rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert output("git", "rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert output("git", "status", "--short", cwd=MATHLIB) == ""
    assert sha256(LEAN_ROOT / "lake-manifest.json") == env["lake_manifest_sha256"]
    assert sha256(MATHLIB / "LICENSE") == env["mathlib_license_sha256"]

    terminal = next(
        candidate for candidate in audit["candidates"]
        if candidate["candidate_id"] == "M0822-C02-MATHLIB-UPPER-BOUND"
    )
    assert terminal["revision"] == MATHLIB_REVISION and terminal["tree"] == MATHLIB_TREE
    assert terminal["file_blob"] == MATHLIB_FILE_BLOB
    terminal_source = MATHLIB / MATHLIB_FILE
    assert output("git", "rev-parse", f"HEAD:{MATHLIB_FILE}", cwd=MATHLIB) == MATHLIB_FILE_BLOB
    assert sha256(terminal_source) == MATHLIB_FILE_SHA256
    source = terminal_source.read_text(encoding="utf-8")
    assert hashlib.sha256(source_block(source).encode()).hexdigest() == MATHLIB_BLOCK_SHA256
    for marker in (
        "theorem erdos_ko_rado",
        "kruskal_katona_lovasz_form",
        "have : Disjoint 𝒜",
        "Set.Sized.card_le",
    ):
        assert marker in source_block(source), marker
    assert output(
        "git", "merge-base", "--is-ancestor", MATHLIB_INTRODUCTION,
        MATHLIB_REVISION, cwd=MATHLIB
    ) == ""
    assert terminal["candidate_classification"] == "M3"
    assert terminal["eligible_route_shape_after_E1"] == "M0-W"
    assert terminal["evidence_level"] == "node_local_below_E1"
    assert terminal["kernel_checked"] is True and terminal["accepted"] is False
    assert terminal["axioms"] == ["propext", "Classical.choice", "Quot.sound"]

    anchor = SOURCE.read_text(encoding="utf-8")
    for marker in (
        "def UpperBoundTarget : Prop",
        "theorem upperBound_of_pinnedMathlib : UpperBoundTarget",
        "Finset.erdos_ko_rado hIntersecting hSized hhalf",
        "#print axioms Finset.erdos_ko_rado",
        "#print axioms upperBound_of_pinnedMathlib",
    ):
        assert marker in anchor, marker
    forbidden = re.compile(r"\b(?:sorry|admit|sorryAx|axiom|constant|unsafe|opaque)\b")
    assert not forbidden.search(without_comments(anchor))
    assert not forbidden.search(without_comments(source_block(source)))

    candidate_ids = {candidate["candidate_id"] for candidate in audit["candidates"]}
    assert candidate_ids == {
        "M0822-C01-LOCAL-STATEMENT-STAR",
        "M0822-C02-MATHLIB-UPPER-BOUND",
        "M0822-C03-ATLAS-WRAPPER",
        "M0822-C04-FORMALBOOK-KATONA",
        "M0822-C05-Q-ANALOG-MISMATCH",
    }
    formalbook = next(c for c in audit["candidates"] if c["candidate_id"].endswith("FORMALBOOK-KATONA"))
    assert formalbook["candidate_classification"] == "M3"
    assert formalbook["toolchain"] == "leanprover/lean4:v4.27.0-rc1"
    assert "Independent Katona" in formalbook["body_provenance"]
    mismatch = next(c for c in audit["candidates"] if c["candidate_id"].endswith("Q-ANALOG-MISMATCH"))
    assert mismatch["candidate_classification"] == "M5"
    assert "Statement mismatch" in mismatch["blocker"]
    result = audit["audit_result"]
    assert result["inventory_classified"] is True
    assert result["source_boundary_coverage"].startswith("5/5")
    assert result["exhaustive_discovery_claim"] is False
    assert result["candidate_kernel_checked"] is True
    assert result["candidate_accepted_by_master"] is False
    assert result["candidate_route_classification"] == "M3"
    assert result["eligible_route_shape_after_E1"] == "M0-W"
    assert result["root_machine_candidate_after"] == "M3"
    assert result["accepted_root_machine_debt_after"] == "M3"
    assert result["root_candidate_vector_after"] == {"H": "H1", "M": "M3", "R": "R4"}
    assert result["accepted_root_vector_after"] == {"H": "H1", "M": "M3", "R": "R4"}
    assert result["audit_complete"] is False and result["theorem_complete"] is False
    provenance = audit["provenance_packet"]
    assert provenance["terminal_declaration"] == "Finset.erdos_ko_rado"
    assert provenance["transitive_trust_closure_hash"] is None

    lean = run_lean(SOURCE)
    if lean.returncode:
        sys.stdout.write(lean.stdout)
        raise SystemExit(lean.returncode)
    normalized = re.sub(r"\s+", " ", lean.stdout)
    expected_axioms = "[propext, Classical.choice, Quot.sound]"
    if normalized.count(expected_axioms) != 2:
        sys.stdout.write(lean.stdout)
        raise SystemExit("unexpected terminal or adapter axiom report")
    for marker in (
        "Finset.erdos_ko_rado",
        "Finset.kruskal_katona_lovasz_form",
        "Finset.iterated_kk",
        "Finset.kruskal_katona",
    ):
        if marker not in lean.stdout:
            raise SystemExit(f"Lean output is missing {marker}")
    if "sorryAx" in lean.stdout or "declaration uses 'sorry'" in lean.stdout:
        sys.stdout.write(lean.stdout)
        raise SystemExit("Lean output reports a placeholder")
    assert hashlib.sha256(lean.stdout.encode()).hexdigest() == LEAN_OUTPUT_SHA256
    assert receipt["lean_output_sha256"] == LEAN_OUTPUT_SHA256
    combined_output = combined_exact_check()
    assert hashlib.sha256(combined_output.encode()).hexdigest() == receipt["combined_output_sha256"]

    assert receipt["verdict"] == "no_state_change"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["content_addressed"] is False
    assert set(receipt["changed_paths"]) == CHANGED_PATHS
    candidate_result = receipt["candidate_result"]
    assert candidate_result["classification"] == "M3"
    assert candidate_result["eligible_route_shape_after_E1"] == "M0-W"
    assert candidate_result["evidence_level"] == "node_local_below_E1"
    assert candidate_result["master_accepted"] is False
    assert receipt["audit_complete"] is False and receipt["theorem_complete"] is False
    assert receipt["accepted_receipt_ids"] == []
    assert receipt["canonical_obligation_ids"] == []
    assert receipt["typed_graph_changes"] == receipt["composition_certificates"] == []
    assert receipt["content_addressed_recipe_or_receipt_ids"] == []
    assert receipt["artifact_hashes"] == {
        "AnchorAudit.lean": f"sha256:{sha256(SOURCE)}",
        "anchor-audit.json": f"sha256:{sha256(AUDIT_PATH)}",
        "anchor-audit-validation.md": f"sha256:{sha256(HERE / 'anchor-audit-validation.md')}",
        "anchor-discovery-protocol.json": f"sha256:{sha256(PROTOCOL_PATH)}",
        "check_anchor_audit.py": f"sha256:{sha256(Path(__file__))}",
    }
    for key, relative in SOURCE_INPUTS.items():
        assert receipt["source_inputs"][key] == f"sha256:{sha256(ROOT / relative)}"
    impact = receipt["ownership_and_change_impact"]
    assert impact["actual_source_ownership"] == [f"Stage1_Instances/{THEOREM_ID}"]
    assert impact["change_impact_set"] == [ITEM_ID]
    assert impact["cross_target_credit"] == []

    if args.worker_packet:
        packet = load(args.worker_packet)
        assert set(packet) == {
            "item_id", "changed_paths", "commands", "output_summary",
            "base_revision", "known_failures", "state",
        }
        assert packet["item_id"] == ITEM_ID and packet["state"] == "[_]"
        assert packet["base_revision"] == BASE_REVISION
        assert set(packet["changed_paths"]) == CHANGED_PATHS
        assert packet["known_failures"] == receipt["known_failures"]
        assert isinstance(packet["commands"], list) and packet["commands"]
        assert isinstance(packet["output_summary"], str) and packet["output_summary"]
        check_text_file(args.worker_packet)

    for relative in CHANGED_PATHS - {".stage1-worker-selftest.json"}:
        check_text_file(ROOT / relative)

    print(
        "check_anchor_audit: ok "
        "(THM-M-0822; 5 candidates; exact pinned mathlib M0-W-shaped route "
        "kernel-checked; evidence below E1; accepted root M3; "
        "audit_complete=false; theorem_complete=false)"
    )


if __name__ == "__main__":
    main()
