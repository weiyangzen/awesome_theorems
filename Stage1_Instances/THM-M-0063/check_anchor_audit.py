#!/usr/bin/env python3
"""Validate the immutable, locally checkable THM-M-0063 anchor inventory."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import urllib.request


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM_ID = "S56-M-0063-ANCHOR_AUDIT"
THEOREM_ID = "THM-M-0063"
BASE_REVISION = "59c86ca38b16fe4d3901ba66530aae4df0e881b0"
BASE_TREE = "2b8fc12c558d4fe807d7b4ac4b2c9a127002338e"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
EXPRESSION_SHA256 = "40929846f1d1d1ff4479e5be6a989358a65ecebec5a2646f6e2dab508c641a1a"
STATEMENT_SHA256 = "37e52256a1a3d1e5e56a00888309b208d7f2c2ee1b45932ac761c5f01e3bf950"
LEAN_OUTPUT_SHA256 = "9aeb8fbb89c21a933859ba1df34d59611ae394a7c4f9c6fa35ea48920bda9b78"
MIL_REVISION = "dd6d752fedb14082f557913c2dccb2d4851e5173"
MIL_SOURCE_SHA256 = "c5f7f3631511e3e27482f7e1946ae842e4dcb4c35a76d0e42b677ba9f8b98709"
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM_ID}/AnchorAudit.lean",
    f"Stage1_Instances/{THEOREM_ID}/anchor-audit-receipt.json",
    f"Stage1_Instances/{THEOREM_ID}/anchor-audit-validation.md",
    f"Stage1_Instances/{THEOREM_ID}/anchor-audit.json",
    f"Stage1_Instances/{THEOREM_ID}/anchor-discovery-protocol.json",
    f"Stage1_Instances/{THEOREM_ID}/check_anchor_audit.py",
}


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise SystemExit(f"{path} must contain a JSON object")
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def output(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(args, cwd=cwd, text=True).strip()


def without_comments(source: str) -> str:
    source = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
    return re.sub(r"--.*", "", source)


def git_blob_sha1(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def line_slice_sha256(path: Path, line_range: str) -> str:
    start, end = (int(value) for value in line_range.split("-"))
    lines = path.read_bytes().splitlines(keepends=True)
    return hashlib.sha256(b"".join(lines[start - 1 : end])).hexdigest()


def immutable_mil_source() -> bytes:
    url = (
        "https://raw.githubusercontent.com/leanprover-community/mathematics_in_lean/"
        f"{MIL_REVISION}/MIL/C09_Groups_and_Rings/S01_Groups.lean"
    )
    request = urllib.request.Request(url, headers={"User-Agent": "stage1-anchor-audit/1.0"})
    with urllib.request.urlopen(request, timeout=30) as response:
        data = response.read()
    if hashlib.sha256(data).hexdigest() != MIL_SOURCE_SHA256:
        raise SystemExit("immutable Mathematics in Lean source hash changed")
    return data


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker-packet", type=Path)
    args = parser.parse_args()

    audit = load(HERE / "anchor-audit.json")
    protocol = load(HERE / "anchor-discovery-protocol.json")
    receipt = load(HERE / "anchor-audit-receipt.json")
    statement = load(HERE / "statement.json")
    manifest = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")

    assert audit["schema_version"] == "stage1-anchor-audit/1.0"
    assert audit["item_id"] == ITEM_ID and audit["theorem_id"] == THEOREM_ID
    assert audit["execution_rank"] == 1094
    assert audit["base_revision"] == BASE_REVISION and audit["base_tree"] == BASE_TREE
    assert output("git", "rev-parse", "HEAD") == BASE_REVISION
    assert output("git", "rev-parse", "HEAD^{tree}") == BASE_TREE

    target = next(row for row in manifest["targets"] if row["theorem_id"] == THEOREM_ID)
    assert target["execution_rank"] == 1094
    assert target["baseline"] == "L0" and target["rework_required"] is True
    assert target["theorem_complete"] is False
    item = next(row for row in execution["items"] if row["id"] == ITEM_ID)
    assert item["phase"] == "anchor_audit" and item["layer"] == 2
    assert item["state"] == "[ ]"
    assert item["depends_on"] == ["S56-M-0063-STATEMENT"]
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]

    assert audit["canonical_target_expression_sha256"] == EXPRESSION_SHA256
    assert audit["canonical_statement_file_sha256"] == STATEMENT_SHA256
    assert sha256(HERE / "Statement.lean") == STATEMENT_SHA256
    formal = statement["canonical_formal_target"]
    assert formal["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert formal["statement_file_sha256"] == STATEMENT_SHA256

    assert protocol["schema_version"] == "stage1-anchor-discovery-protocol/1.0"
    assert protocol["item_id"] == ITEM_ID and protocol["theorem_id"] == THEOREM_ID
    assert protocol["committed_before_final_classification"] is True
    assert protocol["saturation_claim"] is False
    discovery = audit["discovery_protocol"]
    assert discovery["protocol_id"] == protocol["protocol_id"]
    assert discovery["sha256"] == sha256(HERE / "anchor-discovery-protocol.json")

    env = audit["immutable_environment"]
    assert env["mathlib_revision"] == MATHLIB_REVISION
    assert env["mathlib_tree"] == MATHLIB_TREE
    assert output("git", "rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert output("git", "rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert output("git", "status", "--porcelain=v1", "--untracked-files=no", cwd=MATHLIB) == ""
    assert sha256(LEAN_ROOT / "lake-manifest.json") == env["manifest_sha256"]
    assert sha256(LEAN_ROOT / "lean-toolchain") == env["lean_toolchain_file_sha256"]
    assert sha256(MATHLIB / "LICENSE") == env["mathlib_license_sha256"]

    direct = next(c for c in audit["candidates"] if c["candidate_id"] == "M0063-C01-MATHLIB-CAYLEY")
    assert direct["revision"] == MATHLIB_REVISION and direct["tree"] == MATHLIB_TREE
    direct_source = MATHLIB / direct["file"]
    assert output("git", "rev-parse", f"HEAD:{direct['file']}", cwd=MATHLIB) == direct["file_blob"]
    assert sha256(direct_source) == direct["file_sha256"]
    assert line_slice_sha256(direct_source, direct["body_lines"]) == direct["body_sha256"]
    assert direct["candidate_classification"] == "M0-W"
    assert direct["evidence_level"] == "E2"
    for revision in (
        direct["historical_provenance"]["lean4_port_commit"],
        direct["historical_provenance"]["theorem_name_documentation_commit"],
    ):
        output("git", "merge-base", "--is-ancestor", revision, MATHLIB_REVISION, cwd=MATHLIB)

    source = direct_source.read_text(encoding="utf-8")
    for marker in (
        "we prove **Cayley's theorem**",
        "noncomputable def subgroupOfMulAction",
        "Setting " + chr(96) + "H = G" + chr(96),
        "MulEquiv.ofLeftInverse' _ (Classical.choose_spec MulAction.toPerm_injective.hasLeftInverse)",
    ):
        assert marker in source, marker
    forbidden = re.compile(r"\b(?:sorry|admit|sorryAx|axiom|unsafe|opaque)\b")
    assert not forbidden.search(without_comments(source))

    composite = next(
        c for c in audit["candidates"] if c["candidate_id"] == "M0063-C02-MATHLIB-INJECTIVE-COMPOSITE"
    )
    for record in composite["source_records"]:
        path = MATHLIB / record["file"]
        assert output("git", "rev-parse", f"HEAD:{record['file']}", cwd=MATHLIB) == record["blob"]
        assert sha256(path) == record["sha256"]
        assert line_slice_sha256(path, record["lines"]) == record["body_sha256"]
    assert composite["candidate_classification"] == "M3_support_duplicate"

    mil = next(c for c in audit["candidates"] if c["candidate_id"] == "M0063-C03-MATHEMATICS-IN-LEAN")
    mil_data = immutable_mil_source()
    assert git_blob_sha1(mil_data) == mil["file_blob"]
    mil_text = mil_data.decode("utf-8")
    assert "def CayleyIsoMorphism (G : Type*) [Group G]" in mil_text
    assert "Equiv.Perm.subgroupOfMulAction G G" in mil_text
    assert re.search(r"\bsorry\b", without_comments(mil_text))
    assert mil["candidate_classification"] == "M3_duplicate_wrapper"

    adapter_path = HERE / "AnchorAudit.lean"
    adapter = adapter_path.read_text(encoding="utf-8")
    for marker in (
        "def ExactTarget : Prop",
        "theorem exactTarget_mathlib_candidate : ExactTarget",
        "exact ⟨Equiv.Perm.subgroupOfMulAction G G⟩",
        "theorem exactTarget_from_injective_candidate : ExactTarget",
        "exact ⟨MonoidHom.ofInjective MulAction.toPerm_injective⟩",
        "#print sorries exactTarget_mathlib_candidate",
    ):
        assert marker in adapter, marker
    assert not forbidden.search(without_comments(adapter))

    lean = subprocess.run(
        ["lake", "env", "lean", "../../Stage1_Instances/THM-M-0063/AnchorAudit.lean"],
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
    assert hashlib.sha256(lean.stdout.encode()).hexdigest() == LEAN_OUTPUT_SHA256
    normalized = re.sub(r"\s+", " ", lean.stdout)
    assert normalized.count("propext, Classical.choice, Quot.sound") == 3
    assert "'MulAction.toPerm_injective' depends on axioms: [propext]" in lean.stdout
    assert lean.stdout.count("Declarations are sorry-free!") == 3
    assert "sorryAx" not in lean.stdout

    result = audit["audit_result"]
    assert result["source_boundary_coverage"].startswith("4/4 frozen candidate groups")
    assert result["inventory_classified"] is result["exact_candidate_located"] is True
    assert result["candidate_kernel_checked"] is True
    assert result["candidate_accepted_by_master"] is False
    assert result["eligible_external_integration_debt"] is False
    assert result["root_machine_debt_before"] == "M3"
    assert result["root_machine_candidate_route"] == "M0-W"
    assert result["accepted_root_machine_debt_after"] == "M3"
    assert result["root_evidence_level"] == "E2"
    assert result["audit_complete"] is result["theorem_complete"] is False

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == ITEM_ID and receipt["theorem_id"] == THEOREM_ID
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["content_addressed"] is False
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert set(receipt["changed_paths"]) == CHANGED_PATHS
    assert receipt["candidate_result"]["classification"] == "M0-W"
    assert receipt["candidate_result"]["evidence_level"] == "E2"
    assert receipt["candidate_result"]["master_accepted"] is False
    assert receipt["lean_output_sha256"] == LEAN_OUTPUT_SHA256
    assert receipt["audit_complete"] is receipt["theorem_complete"] is False

    if args.worker_packet:
        packet = load(args.worker_packet.resolve())
        assert set(packet) == {
            "item_id",
            "changed_paths",
            "commands",
            "output_summary",
            "base_revision",
            "known_failures",
            "state",
        }
        assert packet["item_id"] == ITEM_ID and packet["state"] == "[_]"
        assert packet["base_revision"] == BASE_REVISION
        assert set(packet["changed_paths"]) == CHANGED_PATHS
        assert packet["known_failures"] == receipt["known_failures"]
        actual_changed = {
            line[3:]
            for line in output("git", "status", "--short", "--untracked-files=all").splitlines()
        }
        assert actual_changed == CHANGED_PATHS | {"Formalizations/Lean/.lake"}

    for relative in CHANGED_PATHS:
        data = (ROOT / relative).read_bytes()
        assert data.endswith(b"\n"), f"missing final newline: {relative}"
        assert b"\r" not in data and b"\0" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())

    print(
        "check_anchor_audit: ok "
        "(THM-M-0063; 4/4 candidate groups; pinned mathlib M0-W/E2 route; "
        "accepted root M3; audit_complete=false; theorem_complete=false)"
    )


if __name__ == "__main__":
    main()
