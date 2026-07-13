#!/usr/bin/env python3
"""Fail-closed structural checks for the THM-M-0276 planned intake."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
THEOREM_ID = "THM-M-0276"
ITEM_ID = "S56-M-0276-INTAKE"
RANK = 1282
BASE_REVISION = "bd81d4853a030765585ef6fed4310484ceb1e458"
BASE_TREE = "fb92fc7476bff9a2ce8c20f1d7be34c6655ca6b4"
SOURCE_COMMIT = "bcf3f9fa79ab8c2b6610c9875668c2589b35b74f"
SOURCE_BLOB = "5c1de0c2bda67f7257142dd99b0dd91d69e0a3bf"
SOURCE_EXCERPT_SHA256 = "be93eb081d599e7c4564dcd771df6af8138adb0d7c8406d921bb1515cf26c72f"
STAGE0_EXCERPT_SHA256 = "e13d15e4bba3744826a007620d257a6616585a2b9c7b5156fa8ac9c5cb945dc1"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
PROBE_OUTPUT_SHA256 = "d84aba7fe0dadb887b30bb30c68f486caa6404fc9f686410fee8c78813d04774"
ROTEM_COMMIT = "6aeecbd2a7d6df63455f3d7beb273b6b4512dfbc"
ROTEM_ARCHIVE_SHA256 = "664a51f3cdf150ac6522702c67677bde27beb3e291e64dcbfa0b5f1a877dfa47"
ROTEM_TEX_SHA256 = "2b1acb4cd1e680e4a0e348c48dbd1c07eee1a8847f7b373f00129afccada9bd4"
ROTEM_EXCERPT_SHA256 = "826821f7a25c2c73cad62e7050bf424826dc0028ed8f9233a68ad7a23b1a9825"
OWNED_FILES = {
    "README.md",
    "instance.json",
    "scope-map.md",
    "source-statement-crosswalk.md",
    "task-dag.json",
    "IntakeProbe.lean",
    "check_intake.py",
    "validation.md",
    "intake-receipt.json",
}
TASK_SUFFIXES = (
    "STATEMENT",
    "ANCHOR_AUDIT",
    "OBLIGATION_TREE",
    "PROOF",
    "VALIDATION",
    "RELEASE",
)
PROBE_DECLARATIONS = (
    "ContinuousLinearMap.exists_approx_preimage_norm_le",
    "ContinuousLinearMap.exists_preimage_norm_le",
    "ContinuousLinearMap.isOpenMap",
    "ContinuousLinearMap.isQuotientMap",
    "LinearEquiv.continuous_symm",
    "IsOpenMap",
)
FORMAL_CANDIDATES = {
    "ContinuousLinearMap.isOpenMap",
    "ContinuousLinearMap.exists_preimage_norm_le",
    "ContinuousLinearMap.isQuotientMap",
    "LinearEquiv.continuous_symm",
}
PACKET_KEYS = {
    "item_id",
    "changed_paths",
    "commands",
    "output_summary",
    "base_revision",
    "known_failures",
    "state",
}
SOURCE_HASH_FIELDS = {
    "target_manifest_sha256": "Docs/Stage1_Targets_rev-5.6.json",
    "authoritative_blueprint_sha256": "Docs/Stage1_Blueprint_rev-5.6.md",
    "execution_dag_sha256": "Docs/Stage1_Execution_DAG_rev-5.6.json",
    "execution_skill_sha256": "skills/execute-stage1-rev56/SKILL.md",
    "blueprint_guidelines_sha256": "Docs/Blueprint_Guidelines.md",
    "repository_math_source_sha256": "Docs/researches/math_theorems.md",
    "stage0_blueprint_sha256": "Docs/Stage0_Blueprint.md",
    "lean_toolchain_file_sha256": "Formalizations/Lean/lean-toolchain",
    "lake_manifest_sha256": "Formalizations/Lean/lake-manifest.json",
}


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict), f"{path} must contain a JSON object"
    return value


def git(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(
        ["git", *args], cwd=cwd, text=True, stderr=subprocess.DEVNULL
    ).strip()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def excerpt_sha256(path: Path, first: int, last: int) -> str:
    lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
    return hashlib.sha256("".join(lines[first - 1 : last]).encode()).hexdigest()


def check_source_archive(path: Path) -> None:
    """Replay the optional immutable H2 source-gap bundle when supplied."""
    assert sha256(path) == ROTEM_ARCHIVE_SHA256
    member = (
        "functional_analysis_notes-6aeecbd2a7d6df63455f3d7beb273b6b4512dfbc/"
        "functional_analysis.tex"
    )
    run = subprocess.run(
        ["tar", "-xOf", str(path), member],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
        timeout=30,
    )
    assert run.returncode == 0, run.stderr.decode(errors="replace")
    assert hashlib.sha256(run.stdout).hexdigest() == ROTEM_TEX_SHA256
    lines = run.stdout.decode("utf-8").splitlines(keepends=True)
    excerpt = "".join(lines[1132:1198]).encode()
    assert hashlib.sha256(excerpt).hexdigest() == ROTEM_EXCERPT_SHA256
    text = excerpt.decode("utf-8")
    assert "\\begin{definition}[Open Map]" in text
    assert "\\begin{theorem}[The Open Mapping Theorem]" in text
    assert "Let $X,Y$ be Banach spaces" in text
    assert "If $T$ is onto, it's open." in text
    assert "By Baire's theorem" in text and "\\end{proof}" in text
    flawed_cover = (
        r"\[Y = T\prs{X} = \bigcup_{n \in \mbb{N}_+} "
        r"T\prs{B_X\prs{0,1}} \text{.}\]"
    )
    assert flawed_cover in text, "pinned source gap changed; re-audit its correction boundary"
    assert r"\overline{T\prs{B\prs{0,n}} - Tx}" in text


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker-packet", type=Path)
    parser.add_argument("--source-archive", type=Path)
    args = parser.parse_args()

    manifest = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    instance = load(HERE / "instance.json")
    dag = load(HERE / "task-dag.json")
    receipt = load(HERE / "intake-receipt.json")

    target = next(row for row in manifest["targets"] if row["theorem_id"] == THEOREM_ID)
    item = next(row for row in execution["items"] if row["id"] == ITEM_ID)
    assert target["execution_rank"] == instance["execution_rank"] == RANK
    assert target["name"] == instance["name_zh"] == "开映射定理"
    assert target["category"] == instance["category"] == "分析学 / 实分析"
    assert target["legacy_priority_slot"] is instance["legacy_priority_slot"] is None
    assert target["baseline"] == instance["baseline"] == "L0"
    assert target["rework_required"] is instance["rework_required"] is True
    assert target["legacy_artifacts_accepted"] is instance["legacy_artifacts_accepted"] is False
    assert target["target_lane"] == instance["target_lane"]
    assert target["intake_score"] == instance["intake_score"] == 86
    assert target["source_status_untrusted"] == instance["source_status_untrusted"] == "已验证"
    assert target["lifecycle_mode"] == instance["lifecycle_mode"] == dag["lifecycle_mode"] == "planned"
    assert target["theorem_complete"] is instance["theorem_complete"] is dag["theorem_complete"] is False

    assert item["theorem_id"] == THEOREM_ID and item["execution_rank"] == RANK
    assert item["phase"] == "intake" and item["layer"] == 0
    assert item["state"] == "[ ]" and item["depends_on"] == []
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]
    assert item["deliverable"] == "Create the theorem dossier, scope map, and source-statement crosswalk."
    assert item["completion_gate"] == "rev-5.6 node-specific receipt and master acceptance"

    assert instance["schema_version"] == "stage1-instance-intake/1.0"
    assert instance["normative_profile"] == "machine-theorem-assurance/1.0"
    assert instance["theorem_id"] == dag["theorem_id"] == receipt["theorem_id"] == THEOREM_ID
    assert instance["item_id"] == receipt["item_id"] == ITEM_ID
    assert instance["intent"] == receipt["intent"] == "intake"
    assert instance["lifecycle"] == dag["lifecycle"] == "planned"
    assert instance["literal_source_claim_zh"] == "满射有界线性算子是开映射"
    assert instance["canonical_statement"] is None and instance["canonical_claim"] is None
    formal = instance["canonical_formal_target"]
    for key in ("module", "declaration_or_expression", "elaborated_expression_hash", "environment_fingerprint"):
        assert formal[key] is None
    assert instance["quantifiers"] == instance["ordered_binders"] == []
    assert instance["hypotheses"] == instance["alternate_encodings"] == []
    assert instance["excluded_degenerate_cases"] == []
    assert instance["obligation_registry_hash"] is instance["discovery_protocol_hash"] is None
    assert instance["root_vector"] == {"H": "H2", "M": "M3", "R": "R4"}
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == dag["accepted_states"] == []
    assert instance["audit_complete"] is receipt["audit_complete"] is dag["audit_complete"] is False
    assert instance["theorem_complete"] is receipt["theorem_complete"] is False

    source = instance["source_revisions"]
    assert source["repository_base"] == receipt["base_revision"] == BASE_REVISION
    assert source["repository_base_tree"] == receipt["base_tree"] == BASE_TREE
    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    assert git("rev-parse", f"{SOURCE_COMMIT}:Docs/researches/math_theorems.md") == SOURCE_BLOB
    assert source["repository_source_record_commit"] == SOURCE_COMMIT
    assert source["repository_source_record_blob"] == SOURCE_BLOB
    assert git("hash-object", "Docs/researches/math_theorems.md") == source["current_repository_math_source_blob"]
    for field, relative in SOURCE_HASH_FIELDS.items():
        assert source[field] == sha256(ROOT / relative), f"stale source hash: {field}"
    assert excerpt_sha256(ROOT / "Docs/researches/math_theorems.md", 1985, 1990) == SOURCE_EXCERPT_SHA256
    assert excerpt_sha256(ROOT / "Docs/researches/math_theorems.md", 2260, 2265) == SOURCE_EXCERPT_SHA256
    assert excerpt_sha256(ROOT / "Docs/Stage0_Blueprint.md", 7630, 7655) == STAGE0_EXCERPT_SHA256
    assert source["repository_record_excerpt_sha256"] == source["repository_duplicate_excerpt_sha256"] == SOURCE_EXCERPT_SHA256
    assert source["stage0_projection_excerpt_sha256"] == STAGE0_EXCERPT_SHA256
    assert source["inspected_rotem_notes_commit"] == ROTEM_COMMIT
    assert source["inspected_rotem_notes_archive_sha256"] == ROTEM_ARCHIVE_SHA256
    assert source["inspected_rotem_notes_tex_sha256"] == ROTEM_TEX_SHA256
    assert source["inspected_rotem_open_mapping_excerpt_sha256"] == ROTEM_EXCERPT_SHA256
    if args.source_archive is not None:
        check_source_archive(args.source_archive.resolve())

    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    assert git("rev-parse", "HEAD", cwd=mathlib) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == MATHLIB_TREE
    assert source["mathlib"] == MATHLIB_REVISION and source["mathlib_tree"] == MATHLIB_TREE
    assert source["banach_source_sha256"] == sha256(mathlib / "Mathlib/Analysis/Normed/Operator/Banach.lean")
    assert source["topology_defs_source_sha256"] == sha256(mathlib / "Mathlib/Topology/Defs/Basic.lean")

    dependency = ITEM_ID
    expected_tasks = []
    for layer, suffix in enumerate(TASK_SUFFIXES, start=1):
        task_id = f"S56-M-0276-{suffix}"
        expected_tasks.append((task_id, [dependency], layer))
        authoritative = next(row for row in execution["items"] if row["id"] == task_id)
        task = next(row for row in dag["tasks"] if row["id"] == task_id)
        assert task["phase"] == authoritative["phase"]
        assert task["layer"] == authoritative["layer"] == layer
        assert task["owned_paths"] == authoritative["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]
        assert task["deliverable"] == authoritative["deliverable"]
        assert task["completion_gate"] == authoritative["completion_gate"]
        assert task["evidence_ids"] == []
        dependency = task_id
    assert [(task["id"], task["depends_on"], task["layer"]) for task in dag["tasks"]] == expected_tasks
    assert all(task["state"] == "open" for task in dag["tasks"])

    catalog = (ROOT / "Docs/researches/math_theorems.md").read_text(encoding="utf-8")
    assert catalog.count("- 陈述: 满射有界线性算子是开映射") == 2
    assert "- 陈述: 非常值全纯函数是开映射" in catalog
    assert {row["theorem_id"] for row in instance["neighbor_target_boundaries"]} == {"THM-M-0235", "THM-M-0277"}
    assert {row["declaration"] for row in instance["formal_candidates_not_credited"]} == FORMAL_CANDIDATES
    assert len(instance["human_source_candidates_not_credited"]) == 1
    source_lead = instance["human_source_candidates_not_credited"][0]
    assert "Theorem 2.2.11" in source_lead["citation"] and ROTEM_COMMIT in source_lead["candidate_locator"]

    actual_files = {path.name for path in HERE.iterdir() if path.is_file()}
    assert set(instance["owned_artifacts"]) == actual_files == OWNED_FILES
    expected_changed = {".stage1-worker-selftest.json"} | {
        f"Stage1_Instances/{THEOREM_ID}/{name}" for name in actual_files
    }
    assert set(receipt["changed_paths"]) == expected_changed
    for relative, expected in receipt["owned_artifact_sha256"].items():
        if relative.endswith("/intake-receipt.json"):
            assert expected == "self_referential_excluded_from_provisional_digest"
        else:
            assert sha256(ROOT / relative) == expected, f"stale owned artifact hash: {relative}"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["verdict"] == "no_state_change" and receipt["content_addressed"] is False
    assert receipt["selftest_result"] == "pass"
    assert receipt["accepted_receipt_ids"] == receipt["proof_body_locations"] == []
    assert receipt["canonical_obligation_ids"] == receipt["statement_fingerprints"] == []
    assert receipt["typed_graph_changes"] == receipt["composition_certificates"] == []
    assert receipt["remaining_root_cut_set"] == [task["id"] for task in dag["tasks"]]

    for relative in instance["public_merge_targets"]:
        assert relative.startswith(f"Stage1_Instances/{THEOREM_ID}/")
        assert (ROOT / relative).is_file()
    checked_paths = list(HERE.iterdir())
    if args.worker_packet is not None:
        checked_paths.append(args.worker_packet.resolve())
    for path in checked_paths:
        if not path.is_file():
            continue
        data = path.read_bytes()
        assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())

    probe = (HERE / "IntakeProbe.lean").read_text(encoding="utf-8")
    for declaration in PROBE_DECLARATIONS:
        assert f"#check {declaration}" in probe
    prohibited = ("sorry", "admit", "sorryAx", "axiom ", "constant ", "opaque ", "unsafe ")
    assert all(token not in probe for token in prohibited)
    lean_run = subprocess.run(
        ["lake", "env", "lean", "../../Stage1_Instances/THM-M-0276/IntakeProbe.lean"],
        cwd=ROOT / "Formalizations/Lean",
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
        timeout=120,
    )
    assert lean_run.returncode == 0, lean_run.stdout
    assert hashlib.sha256(lean_run.stdout.encode()).hexdigest() == PROBE_OUTPUT_SHA256
    for declaration in PROBE_DECLARATIONS:
        assert declaration in lean_run.stdout

    if args.worker_packet is not None:
        packet = load(args.worker_packet.resolve())
        assert set(packet) == PACKET_KEYS
        assert packet["item_id"] == ITEM_ID and packet["state"] == "[_]"
        assert packet["base_revision"] == BASE_REVISION
        assert set(packet["changed_paths"]) == expected_changed
        assert isinstance(packet["commands"], list) and packet["commands"]
        assert isinstance(packet["output_summary"], str) and packet["output_summary"]
        assert packet["known_failures"] == receipt["known_failures"]

    print("intake invariant check: ok (THM-M-0276 planned; H2/M3/R4; six open tasks)")


if __name__ == "__main__":
    main()
