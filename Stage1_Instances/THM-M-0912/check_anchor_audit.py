#!/usr/bin/env python3
"""Validate the immutable THM-M-0912 candidate inventory and exact adapters."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
SOURCE = HERE / "AnchorAudit.lean"
STATEMENT_SOURCE = HERE / "Statement.lean"
STATEMENT_RECORD = HERE / "statement.json"
AUDIT_PATH = HERE / "anchor-audit.json"
PROTOCOL_PATH = HERE / "anchor-discovery-protocol.json"
RECEIPT_PATH = HERE / "anchor-audit-receipt.json"
ITEM_ID = "S56-M-0912-ANCHOR_AUDIT"
THEOREM_ID = "THM-M-0912"
BASE_REVISION = "72e9e8092182121a6794921f61fcc9cae22f726d"
BASE_TREE = "0d6c1fdf06d1573c256af331c6b198e5a787af43"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
EXPRESSION_SHA256 = "b322549a05e57fbf466b60eb8ff89f4a08c6ee3b68ea5bf3ff3bf86d99521776"
STATEMENT_SHA256 = "63fda2462d33fba5f18ba0c46df33d7c34c2442609992e7435a2ab4ac33e434e"
PROTOCOL_SHA256 = "df2cf140c40d47f2798e7bee90bc75b5b85b0c92905ebd9c22e06a981d68f973"
LEAN_OUTPUT_SHA256 = "0eb74a201d0ac2601776cf5ff6580d3dda0fa9c6bc838b5becc0ab73ce25d862"
STATEMENT_NAMESPACE = "Stage1Instances.THM_M_0912"
STATEMENT_TARGET = "PascalIdentityTarget"
AUDIT_NAMESPACE = "Stage1Instances.THM_M_0912_AnchorAudit"
AUDIT_TARGET = "ExactTarget"
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
    path: path
    for path in [
        "Docs/Stage1_Targets_rev-5.6.json",
        "Docs/Stage1_Blueprint_rev-5.6.md",
        "Docs/Stage1_Execution_DAG_rev-5.6.json",
        "skills/execute-stage1-rev56/SKILL.md",
        "Docs/Blueprint_Guidelines.md",
        "Formalizations/Lean/lean-toolchain",
        "Formalizations/Lean/lake-manifest.json",
        f"Stage1_Instances/{THEOREM_ID}/Statement.lean",
        f"Stage1_Instances/{THEOREM_ID}/statement.json",
        f"Stage1_Instances/{THEOREM_ID}/statement-receipt.json",
    ]
}


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise SystemExit(f"{path} must contain a JSON object")
    return value


def output(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(args, cwd=cwd, text=True).strip()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def hash_slice(path: Path, start: int, end: int) -> str:
    lines = path.read_bytes().splitlines(keepends=True)
    return hashlib.sha256(b"".join(lines[start - 1 : end])).hexdigest()


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
    environment = os.environ.copy()
    environment.update({"LC_ALL": "C", "LANG": "C", "NO_COLOR": "1"})
    return subprocess.run(
        ["lake", "env", "lean", str(path)],
        cwd=LEAN_ROOT,
        env=environment,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=180,
        check=False,
    )


def serialized_expression(source: Path, declaration: str, end_marker: str) -> str:
    text = source.read_text(encoding="utf-8")
    if text.count(end_marker) != 1:
        raise SystemExit(f"print marker missing or ambiguous in {source.name}")
    prefix = text[: text.index(end_marker)]
    with tempfile.NamedTemporaryFile(
        "w", suffix=".lean", dir=HERE, delete=False, encoding="utf-8"
    ) as handle:
        handle.write(prefix)
        handle.write(f"#print {declaration}\n")
        temporary = Path(handle.name)
    try:
        result = run_lean(temporary)
        if result.returncode:
            sys.stdout.write(result.stdout)
            raise SystemExit(result.returncode)
        marker = f"def {declaration} : Prop :=\n"
        index = result.stdout.rfind(marker)
        if index < 0:
            raise SystemExit(f"serialized expression missing for {declaration}")
        expression = result.stdout[index + len(marker) :].strip()
        if "?m." in expression:
            raise SystemExit(f"unresolved metavariable in {declaration}")
        return expression
    finally:
        temporary.unlink()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker-packet", type=Path)
    args = parser.parse_args()

    audit = load(AUDIT_PATH)
    protocol = load(PROTOCOL_PATH)
    receipt = load(RECEIPT_PATH)
    statement = load(STATEMENT_RECORD)
    instance = load(HERE / "instance.json")
    manifest = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")

    assert audit["item_id"] == protocol["item_id"] == receipt["item_id"] == ITEM_ID
    assert audit["theorem_id"] == protocol["theorem_id"] == receipt["theorem_id"] == THEOREM_ID
    assert audit["execution_rank"] == 1454
    assert audit["base_revision"] == receipt["base_revision"] == BASE_REVISION
    assert audit["base_tree"] == receipt["base_tree"] == BASE_TREE
    assert output("git", "rev-parse", "HEAD") == BASE_REVISION
    assert output("git", "rev-parse", "HEAD^{tree}") == BASE_TREE
    assert protocol["saturation_claim"] is False
    assert sha256(PROTOCOL_PATH) == PROTOCOL_SHA256
    assert audit["discovery_protocol"]["sha256"] == PROTOCOL_SHA256

    target = next(row for row in manifest["targets"] if row["theorem_id"] == THEOREM_ID)
    assert target["execution_rank"] == 1454
    assert target["name"] == "帕斯卡恒等式"
    assert target["baseline"] == "L0" and target["rework_required"] is True
    assert target["theorem_complete"] is False
    item = next(row for row in execution["items"] if row["id"] == ITEM_ID)
    assert item["phase"] == "anchor_audit" and item["layer"] == 2
    assert item["state"] == "[ ]"
    assert item["depends_on"] == ["S56-M-0912-STATEMENT"]
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]
    prerequisite = next(
        row for row in execution["items"] if row["id"] == "S56-M-0912-STATEMENT"
    )
    assert prerequisite["state"] == "[_]"

    formal = statement["canonical_formal_target"]
    assert formal["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert formal["statement_file_sha256"] == STATEMENT_SHA256
    assert sha256(STATEMENT_SOURCE) == STATEMENT_SHA256
    assert audit["canonical_target"]["expression_sha256"] == EXPRESSION_SHA256
    assert audit["canonical_target"]["statement_file_sha256"] == STATEMENT_SHA256
    canonical = serialized_expression(
        STATEMENT_SOURCE,
        f"{STATEMENT_NAMESPACE}.{STATEMENT_TARGET}",
        "#print Stage1Instances.THM_M_0912.PascalIdentityTarget",
    )
    candidate_target = serialized_expression(
        SOURCE,
        f"{AUDIT_NAMESPACE}.{AUDIT_TARGET}",
        "#print ExactTarget",
    )
    assert canonical == candidate_target
    assert hashlib.sha256(canonical.encode()).hexdigest() == EXPRESSION_SHA256

    env = audit["immutable_environment"]
    assert env["mathlib_revision"] == MATHLIB_REVISION
    assert env["mathlib_tree"] == MATHLIB_TREE
    assert output("git", "rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert output("git", "rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert output("git", "status", "--short", cwd=MATHLIB) == ""
    assert sha256(MATHLIB / "LICENSE") == env["mathlib_license_sha256"]
    assert sha256(LEAN_ROOT / "lake-manifest.json") == env["lake_manifest_sha256"]

    source_record = audit["pinned_mathlib_source"]
    basic = MATHLIB / source_record["file"]
    assert output("git", "rev-parse", f"HEAD:{source_record['file']}", cwd=MATHLIB) == (
        source_record["file_blob"]
    )
    assert sha256(basic) == source_record["file_sha256"]
    assert hash_slice(basic, 45, 82) == source_record["definition_and_recurrence_sha256"]
    assert hash_slice(basic, 65, 66) == source_record["successor_lines_sha256"]
    assert hash_slice(basic, 68, 81) == source_record["positive_predecessor_lines_sha256"]
    basic_text = basic.read_text(encoding="utf-8")
    for marker in (
        "def choose : ℕ → ℕ → ℕ",
        "theorem choose_succ_succ (n k : ℕ)",
        "theorem choose_succ_succ' (n k : ℕ)",
        "theorem choose_succ_left (n k : ℕ)",
        "theorem choose_succ_right (n k : ℕ)",
        "theorem choose_eq_choose_pred_add {n k : ℕ}",
    ):
        assert marker in basic_text, marker

    candidates = audit["candidates"]
    assert {row["candidate_id"] for row in candidates} == {
        "M0912-C01-MATHLIB-PREDECESSOR",
        "M0912-C02-MATHLIB-SUCCESSOR",
        "M0912-C03-MATHLIB-ADJACENT",
        "M0912-C04-PUBLIC-DOWNSTREAM-USERS",
        "M0912-C05-HISTORICAL-LEAN",
    }
    for candidate_id in (
        "M0912-C01-MATHLIB-PREDECESSOR",
        "M0912-C02-MATHLIB-SUCCESSOR",
    ):
        candidate = next(row for row in candidates if row["candidate_id"] == candidate_id)
        assert candidate["revision"] == MATHLIB_REVISION
        assert candidate["candidate_machine_classification"].startswith("M0-W route candidate")
        assert candidate["evidence_level"] == (
            "provisional direct local kernel probe; not accepted E1"
        )
        assert candidate["machine_reported_sorry_free"] is True
        assert candidate["accepted"] is False

    source = SOURCE.read_text(encoding="utf-8")
    for marker in (
        "def ExactTarget : Prop",
        "theorem exactTarget_mathlib_predecessor : ExactTarget",
        "theorem exactTarget_mathlib_successor : ExactTarget",
        "Nat.choose_eq_choose_pred_add hm hn",
        "Nat.choose_succ_succ' r k",
        "#print axioms exactTarget_mathlib_predecessor",
        "#print sorries exactTarget_mathlib_successor",
    ):
        assert marker in source, marker
    forbidden = re.compile(
        r"\b(?:sorry|admit|sorryAx|axiom|constant|unsafe|opaque|implemented_by|extern)\b"
    )
    assert not forbidden.search(without_comments(source))
    assert not forbidden.search(without_comments(basic_text))

    lean = run_lean(SOURCE)
    if lean.returncode:
        sys.stdout.write(lean.stdout)
        raise SystemExit(lean.returncode)
    normalized = re.sub(r"\s+", " ", lean.stdout)
    if normalized.count("does not depend on any axioms") != 2:
        sys.stdout.write(lean.stdout)
        raise SystemExit("unexpected axiom-free terminal count")
    if normalized.count("depends on axioms: [propext]") != 5:
        sys.stdout.write(lean.stdout)
        raise SystemExit("unexpected propext report count")
    if lean.stdout.count("Declarations are sorry-free!") != 7:
        sys.stdout.write(lean.stdout)
        raise SystemExit("unexpected sorry-free report count")
    if hashlib.sha256(lean.stdout.encode()).hexdigest() != LEAN_OUTPUT_SHA256:
        sys.stdout.write(lean.stdout)
        raise SystemExit("candidate Lean output changed")
    assert receipt["lean_output_sha256"] == LEAN_OUTPUT_SHA256

    result = audit["audit_result"]
    assert result["inventory_classified"] is True
    assert result["exact_pinned_candidate_located"] is True
    assert result["exact_adapter_kernel_checked"] is True
    assert result["candidate_machine_classification"].startswith("M0-W route candidate")
    assert result["candidate_evidence_boundary"] == (
        "provisional direct local kernel probe; not accepted E1"
    )
    assert result["accepted_root_machine_debt_after"] == "M3"
    assert instance["root_vector"] == {"H": "H1", "M": "M3", "R": "R4"}
    assert result["root_vector_before"] == instance["root_vector"]
    assert result["accepted_root_vector_after"] == instance["root_vector"]
    assert result["accepted_receipt_ids"] == []
    assert result["audit_complete"] is False and result["theorem_complete"] is False

    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["verdict"] == "no_state_change"
    assert set(receipt["changed_paths"]) == CHANGED_PATHS
    assert receipt["candidate_result"]["classification"].startswith("M0-W route candidate")
    assert receipt["candidate_result"]["evidence_level"] == (
        "provisional direct local kernel probe; not accepted E1"
    )
    assert receipt["audit_complete"] is False and receipt["theorem_complete"] is False
    assert receipt["accepted_receipt_ids"] == []
    assert receipt["root_vector_before"] == instance["root_vector"]
    assert receipt["accepted_root_vector_after"] == instance["root_vector"]
    assert receipt["artifact_hashes"] == {
        "AnchorAudit.lean": f"sha256:{sha256(SOURCE)}",
        "anchor-audit.json": f"sha256:{sha256(AUDIT_PATH)}",
        "anchor-audit-validation.md": (
            f"sha256:{sha256(HERE / 'anchor-audit-validation.md')}"
        ),
        "anchor-discovery-protocol.json": f"sha256:{sha256(PROTOCOL_PATH)}",
        "check_anchor_audit.py": f"sha256:{sha256(Path(__file__))}",
    }
    for key, relative in SOURCE_INPUTS.items():
        assert receipt["source_inputs"][key] == f"sha256:{sha256(ROOT / relative)}"

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
        assert packet["commands"] == receipt["commands_and_results"]
        assert packet["output_summary"] == receipt["output_summary"]

    for relative in CHANGED_PATHS - {".stage1-worker-selftest.json"}:
        check_text_file(ROOT / relative)

    print(
        "check_anchor_audit: ok "
        "(THM-M-0912; 5 classified groups; exact pinned mathlib M0-W route candidate; "
        "accepted root remains H1/M3/R4; audit_complete=false; theorem_complete=false)"
    )


if __name__ == "__main__":
    main()
