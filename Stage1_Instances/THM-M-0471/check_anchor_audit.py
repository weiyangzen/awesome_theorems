#!/usr/bin/env python3
"""Validate the immutable THM-M-0471 anchor inventory and exact candidate."""

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
SOURCE = HERE / "AnchorAudit.lean"
STATEMENT_SOURCE = HERE / "Statement.lean"
STATEMENT_RECORD = HERE / "statement.json"
AUDIT_PATH = HERE / "anchor-audit.json"
PROTOCOL_PATH = HERE / "anchor-discovery-protocol.json"
RECEIPT_PATH = HERE / "anchor-audit-receipt.json"
ITEM_ID = "S56-M-0471-ANCHOR_AUDIT"
THEOREM_ID = "THM-M-0471"
BASE_REVISION = "a3b18eec39bf04be025b1641cae02f4d44fdf11a"
BASE_TREE = "fdfff18dea4c6798c5b322b6088dfe556109c134"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
EXPRESSION_SHA256 = "07ae92b7b398b89a1bbe8413563f1c30da5b8bbd0522f6d070fd62dcea0ac4e4"
STATEMENT_SHA256 = "775b86743247571a1a5e5e7f1aa099683f26368e4dd7bee9e23a0b2a2ddbc715"
PROTOCOL_SHA256 = "50a0fc489c85a9cd53f256388ea26a9e987586b0e05cdb6c30ef872f38ff4986"
LEAN_OUTPUT_SHA256 = "e7e41f7bea6174f222eb64e38bae605687e352478d526b3f689814ecf13b890f"
NAMESPACE = "Stage1Instances.THM_M_0471"
TARGET = "FundamentalTheoremOfArithmeticTarget"
AUDIT_NAMESPACE = "Stage1Instances.THM_M_0471_AnchorAudit"
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
    "Docs/Stage1_Targets_rev-5.6.json": "Docs/Stage1_Targets_rev-5.6.json",
    "Docs/Stage1_Blueprint_rev-5.6.md": "Docs/Stage1_Blueprint_rev-5.6.md",
    "Docs/Stage1_Execution_DAG_rev-5.6.json": "Docs/Stage1_Execution_DAG_rev-5.6.json",
    "skills/execute-stage1-rev56/SKILL.md": "skills/execute-stage1-rev56/SKILL.md",
    "Formalizations/Lean/lean-toolchain": "Formalizations/Lean/lean-toolchain",
    "Formalizations/Lean/lake-manifest.json": "Formalizations/Lean/lake-manifest.json",
    f"Stage1_Instances/{THEOREM_ID}/Statement.lean": (
        f"Stage1_Instances/{THEOREM_ID}/Statement.lean"
    ),
    f"Stage1_Instances/{THEOREM_ID}/statement.json": (
        f"Stage1_Instances/{THEOREM_ID}/statement.json"
    ),
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
    return subprocess.run(
        ["lake", "env", "lean", str(path)],
        cwd=LEAN_ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=180,
        check=False,
    )


def serialized_expression(source: Path, marker: str, declaration: str) -> str:
    text = source.read_text(encoding="utf-8")
    if text.count(marker) != 1:
        raise SystemExit(f"print marker is missing or ambiguous: {marker}")
    text = text[: text.index(marker)] + marker.replace("#print ", f"#print {declaration}\n-- ", 1)
    with tempfile.NamedTemporaryFile(
        "w", suffix=".lean", dir=HERE, delete=False, encoding="utf-8"
    ) as handle:
        handle.write(text)
        temporary = Path(handle.name)
    try:
        result = run_lean(temporary)
        if result.returncode:
            sys.stdout.write(result.stdout)
            raise SystemExit(result.returncode)
        expression_marker = f"def {declaration} : Prop :=\n"
        index = result.stdout.rfind(expression_marker)
        if index < 0:
            raise SystemExit(f"missing serialized expression for {declaration}")
        expression = result.stdout[index + len(expression_marker) :].strip()
        if "?m." in expression:
            raise SystemExit("unresolved metavariable in serialized target")
        return expression
    finally:
        temporary.unlink()


def statement_expression() -> str:
    text = STATEMENT_SOURCE.read_text(encoding="utf-8")
    marker = "#print FundamentalTheoremOfArithmeticTarget"
    if text.count(marker) != 1:
        raise SystemExit("statement print marker is missing or ambiguous")
    result = run_lean(STATEMENT_SOURCE)
    if result.returncode:
        sys.stdout.write(result.stdout)
        raise SystemExit(result.returncode)
    expression_marker = f"def {NAMESPACE}.{TARGET} : Prop :=\n"
    index = result.stdout.rfind(expression_marker)
    if index < 0:
        raise SystemExit("canonical statement expression is missing")
    return result.stdout[index + len(expression_marker) :].strip()


def audit_expression() -> str:
    result = run_lean(SOURCE)
    if result.returncode:
        sys.stdout.write(result.stdout)
        raise SystemExit(result.returncode)
    expression_marker = f"def {AUDIT_NAMESPACE}.{AUDIT_TARGET} : Prop :=\n"
    index = result.stdout.rfind(expression_marker)
    if index < 0:
        raise SystemExit("audit target expression is missing")
    return result.stdout[index + len(expression_marker) :].strip()


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
    assert audit["execution_rank"] == 1353
    assert audit["base_revision"] == receipt["base_revision"] == BASE_REVISION
    assert audit["base_tree"] == receipt["base_tree"] == BASE_TREE
    assert output("git", "rev-parse", "HEAD") == BASE_REVISION
    assert output("git", "rev-parse", "HEAD^{tree}") == BASE_TREE
    assert protocol["saturation_claim"] is False
    assert sha256(PROTOCOL_PATH) == PROTOCOL_SHA256
    assert audit["discovery_protocol_sha256"] == PROTOCOL_SHA256

    target = next(row for row in manifest["targets"] if row["theorem_id"] == THEOREM_ID)
    assert target["execution_rank"] == 1353
    assert target["baseline"] == "L0" and target["rework_required"] is True
    assert target["theorem_complete"] is False
    item = next(row for row in execution["items"] if row["id"] == ITEM_ID)
    assert item["phase"] == "anchor_audit" and item["layer"] == 2
    assert item["state"] == "[ ]"
    assert item["depends_on"] == ["S56-M-0471-STATEMENT"]
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]
    prerequisite = next(
        row for row in execution["items"] if row["id"] == "S56-M-0471-STATEMENT"
    )
    assert prerequisite["state"] == "[_]"

    formal = statement["canonical_formal_target"]
    assert formal["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert formal["statement_file_sha256"] == STATEMENT_SHA256
    assert sha256(STATEMENT_SOURCE) == STATEMENT_SHA256
    assert audit["canonical_target"]["expression_sha256"] == EXPRESSION_SHA256
    assert audit["canonical_target"]["statement_file_sha256"] == STATEMENT_SHA256
    canonical = statement_expression()
    candidate_target = audit_expression()
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

    candidates = audit["candidates"]
    assert {candidate["candidate_id"] for candidate in candidates} == {
        "M0471-C01-MATHLIB-PRIME-LIST",
        "M0471-C02-MATHLIB-EXPONENT-MAP",
        "M0471-C03-EXTERNAL-WELL-ORDERED-RING",
        "M0471-C04-HISTORICAL-LEAN3-XENA",
    }
    direct = next(c for c in candidates if c["candidate_id"] == "M0471-C01-MATHLIB-PRIME-LIST")
    assert direct["candidate_machine_classification"] == (
        "M0-W_candidate_pending_E1_and_master_acceptance"
    )
    assert direct["evidence_level"] == "E3_plus_direct_kernel_probe_nonrelease"
    assert direct["kernel_checked"] is True
    assert direct["accepted"] is False
    factors = MATHLIB / direct["file"]
    assert output("git", "rev-parse", f"HEAD:{direct['file']}", cwd=MATHLIB) == direct["file_git_blob"]
    assert sha256(factors) == direct["file_sha256"]
    hashes = direct["source_slice_hashes"]
    assert hash_slice(factors, 55, 81) == hashes["primality_and_product_lines_55_81_sha256"]
    assert hash_slice(factors, 131, 132) == hashes["nonempty_lines_131_132_sha256"]
    assert hash_slice(factors, 167, 179) == hashes["uniqueness_lines_167_179_sha256"]
    factor_lines = factors.read_bytes().splitlines(keepends=True)
    combined = b"".join(
        line
        for start, end in ((55, 81), (131, 132), (167, 179))
        for line in factor_lines[start - 1 : end]
    )
    assert hashlib.sha256(combined).hexdigest() == hashes["combined_sha256"]
    factors_text = factors.read_text(encoding="utf-8")
    for marker in (
        "theorem prime_of_mem_primeFactorsList",
        "theorem prod_primeFactorsList",
        "theorem primeFactorsList_ne_nil",
        "/-- **Fundamental theorem of arithmetic** -/",
        "theorem primeFactorsList_unique",
        "refine perm_of_prod_eq_prod",
    ):
        assert marker in factors_text, marker

    list_prime = MATHLIB / "Mathlib/Data/List/Prime.lean"
    assert output("git", "rev-parse", "HEAD:Mathlib/Data/List/Prime.lean", cwd=MATHLIB) == (
        "17337ba91fd2f4b2b947301cca165a253662e377"
    )
    assert sha256(list_prime) == "148cf3e70ddc39591270dd3c4d9da733a91ff574e8f5c1bd6fd8fd2f42e33591"
    assert hash_slice(list_prime, 58, 78) == (
        "513da0ba5f6f0db17636ca8c66b48c99420967030d9d6e37e2a77e44fb1066a6"
    )

    exponent = next(c for c in candidates if c["candidate_id"] == "M0471-C02-MATHLIB-EXPONENT-MAP")
    exponent_source = MATHLIB / exponent["file"]
    assert output("git", "rev-parse", f"HEAD:{exponent['file']}", cwd=MATHLIB) == exponent["file_git_blob"]
    assert sha256(exponent_source) == exponent["file_sha256"]

    external = next(c for c in candidates if c["candidate_id"] == "M0471-C03-EXTERNAL-WELL-ORDERED-RING")
    assert external["revision"] == "f64a9056ce28ebe5c3946d6c522a1a79e56f835d"
    assert external["tree"] == "a6fd29cf50955470d0aa613cc9b83f7146711d97"
    assert external["candidate_machine_classification"] == "M5"
    assert external["license"].startswith("No license")

    source = SOURCE.read_text(encoding="utf-8")
    for marker in (
        "def ExactTarget : Prop",
        "theorem exactTarget_mathlib_candidate : ExactTarget",
        "Nat.primeFactorsList_ne_nil",
        "Nat.prime_of_mem_primeFactorsList",
        "Nat.prod_primeFactorsList",
        "Nat.primeFactorsList_unique",
        "#print axioms exactTarget_mathlib_candidate",
        "#print sorries exactTarget_mathlib_candidate",
    ):
        assert marker in source, marker
    forbidden = re.compile(
        r"\b(?:sorry|admit|sorryAx|axiom|constant|unsafe|opaque|implemented_by|extern)\b"
    )
    assert not forbidden.search(without_comments(source))
    assert not forbidden.search(without_comments(factors_text))
    assert not forbidden.search(without_comments(list_prime.read_text(encoding="utf-8")))

    lean = run_lean(SOURCE)
    if lean.returncode:
        sys.stdout.write(lean.stdout)
        raise SystemExit(lean.returncode)
    normalized = re.sub(r"\s+", " ", lean.stdout)
    if normalized.count("depends on axioms: [propext, Classical.choice, Quot.sound]") != 6:
        sys.stdout.write(lean.stdout)
        raise SystemExit("unexpected candidate axiom report")
    if lean.stdout.count("Declarations are sorry-free!") != 6:
        sys.stdout.write(lean.stdout)
        raise SystemExit("unexpected transitive sorry report")
    if hashlib.sha256(lean.stdout.encode()).hexdigest() != LEAN_OUTPUT_SHA256:
        sys.stdout.write(lean.stdout)
        raise SystemExit("candidate Lean output changed")
    assert receipt["lean_output_sha256"] == LEAN_OUTPUT_SHA256

    result = audit["audit_result"]
    assert result["inventory_classified"] is True
    assert result["source_boundary_coverage"].startswith("4/4 canonical")
    assert result["candidate_classification"] == (
        "M0-W_candidate_pending_E1_and_master_acceptance"
    )
    assert result["candidate_accepted_by_master"] is False
    assert result["accepted_root_machine_debt_after"] == "M3"
    assert instance["root_vector"] == {"H": "H1", "M": "M3", "R": "R4"}
    assert result["root_vector_before"] == instance["root_vector"]
    assert result["accepted_root_vector_after"] == instance["root_vector"]
    assert result["audit_complete"] is False and result["theorem_complete"] is False

    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert set(receipt["changed_paths"]) == CHANGED_PATHS
    assert receipt["candidate_result"]["classification"] == (
        "M0-W_candidate_pending_E1_and_master_acceptance"
    )
    assert receipt["candidate_result"]["evidence_level"] == (
        "E3_plus_direct_kernel_probe_nonrelease"
    )
    assert receipt["audit_complete"] is False and receipt["theorem_complete"] is False
    assert receipt["accepted_receipt_ids"] == []
    assert receipt["root_vector_before"] == instance["root_vector"]
    assert receipt["accepted_root_vector_after"] == instance["root_vector"]
    assert receipt["artifact_hashes"] == {
        "AnchorAudit.lean": f"sha256:{sha256(SOURCE)}",
        "anchor-audit.json": f"sha256:{sha256(AUDIT_PATH)}",
        "anchor-audit-validation.md": f"sha256:{sha256(HERE / 'anchor-audit-validation.md')}",
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
        "(THM-M-0471; 4 classified candidates; exact pinned mathlib M0-W candidate; "
        "accepted root remains H1/M3/R4; audit_complete=false; theorem_complete=false)"
    )


if __name__ == "__main__":
    main()
