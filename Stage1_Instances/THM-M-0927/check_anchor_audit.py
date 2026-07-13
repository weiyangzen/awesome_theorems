#!/usr/bin/env python3
"""Validate the immutable THM-M-0927 anchor inventory and exact adapter."""

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
AUDIT_PATH = HERE / "anchor-audit.json"
PROTOCOL_PATH = HERE / "anchor-discovery-protocol.json"
RECEIPT_PATH = HERE / "anchor-audit-receipt.json"
THEOREM_ID = "THM-M-0927"
ITEM_ID = "S56-M-0927-ANCHOR_AUDIT"
BASE_REVISION = "4a10a7a4ddff88e302d5a303b16dd687d9468f63"
BASE_TREE = "730de242597680b39a7087d3204dfd1e6c41c60e"
EXPRESSION_SHA256 = "0a05e8c4976c01759ef82d364afc86f498f700edc1a0fcb3f8935765992b5a2f"
STATEMENT_SHA256 = "72172fb6015846b808a81dfc4995767dec5381de5845f68c47cbc5fdb2eeed8d"
PROTOCOL_SHA256 = "c85adf00494cf750c4814cf2204e1dc5fc15ea2688f329182fc98d2165f031cd"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
LEAN_OUTPUT_SHA256 = "b068ed13f0100c51b9a0b35ecea9b43d03e0258c38a7f911a97ef85b389f0209"
STATEMENT_DECLARATION = "Stage1Instances.THM_M_0927.BinetFormulaTarget"
AUDIT_DECLARATION = "Stage1Instances.THM_M_0927_AnchorAudit.ExactTarget"
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM_ID}/AnchorAudit.lean",
    f"Stage1_Instances/{THEOREM_ID}/anchor-audit-receipt.json",
    f"Stage1_Instances/{THEOREM_ID}/anchor-audit-validation.md",
    f"Stage1_Instances/{THEOREM_ID}/anchor-audit.json",
    f"Stage1_Instances/{THEOREM_ID}/anchor-discovery-protocol.json",
    f"Stage1_Instances/{THEOREM_ID}/check_anchor_audit.py",
}
FORBIDDEN = re.compile(
    r"\b(?:sorry|admit|sorryAx|axiom|constant|unsafe|opaque|"
    r"implemented_by|extern|proof_wanted)\b"
)


def load(path: Path) -> dict:
    def reject_duplicate_keys(pairs: list[tuple[str, object]]) -> dict:
        value: dict[str, object] = {}
        for key, item in pairs:
            if key in value:
                raise SystemExit(f"duplicate JSON key in {path}: {key}")
            value[key] = item
        return value

    value = json.loads(
        path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicate_keys
    )
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
    environment.update({"LC_ALL": "C", "LANG": "C", "NO_COLOR": "1", "TZ": "UTC"})
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


def serialized_expression(source: Path, declaration: str, marker: str) -> str:
    text = source.read_text(encoding="utf-8")
    if text.count(marker) != 1:
        raise SystemExit(f"print marker missing or ambiguous in {source.name}")
    prefix = text[: text.index(marker)]
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
        printed = f"def {declaration} : Prop :=\n"
        index = result.stdout.rfind(printed)
        if index < 0:
            raise SystemExit(f"serialized expression missing for {declaration}")
        expression = result.stdout[index + len(printed) :].strip()
        if "?m." in expression:
            raise SystemExit(f"unresolved metavariable in {declaration}")
        return expression
    finally:
        temporary.unlink()


def normalize_generated_proofs(expression: str) -> str:
    expression = re.sub(r"\b[A-Za-z0-9_'.]+\._proof_[0-9]+\b", "<proof>", expression)
    return " ".join(expression.split())


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker-packet", type=Path)
    args = parser.parse_args()

    audit = load(AUDIT_PATH)
    protocol = load(PROTOCOL_PATH)
    receipt = load(RECEIPT_PATH)
    statement = load(HERE / "statement.json")
    instance = load(HERE / "instance.json")
    targets = load(ROOT / "Docs" / "Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")

    assert audit["item_id"] == protocol["item_id"] == receipt["item_id"] == ITEM_ID
    assert audit["theorem_id"] == protocol["theorem_id"] == receipt["theorem_id"] == THEOREM_ID
    assert audit["execution_rank"] == 1546
    assert audit["base_revision"] == receipt["base_revision"] == BASE_REVISION
    assert audit["base_tree"] == receipt["base_tree"] == BASE_TREE
    assert output("git", "rev-parse", "HEAD") == BASE_REVISION
    assert output("git", "rev-parse", "HEAD^{tree}") == BASE_TREE
    assert protocol["saturation_claim"] is False
    assert protocol["frozen_before_candidate_classification"] is True
    assert sha256(PROTOCOL_PATH) == PROTOCOL_SHA256
    assert audit["discovery_protocol"]["sha256"] == PROTOCOL_SHA256

    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM_ID)
    item = next(row for row in execution["items"] if row["id"] == ITEM_ID)
    prerequisite = next(
        row for row in execution["items"] if row["id"] == "S56-M-0927-STATEMENT"
    )
    assert target["execution_rank"] == 1546 and target["name"] == "比内公式"
    assert target["baseline"] == "L0" and target["rework_required"] is True
    assert target["theorem_complete"] is False
    assert item["phase"] == "anchor_audit" and item["layer"] == 2
    assert item["state"] == "[ ]"
    assert item["depends_on"] == ["S56-M-0927-STATEMENT"]
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]
    assert prerequisite["state"] == "[_]"

    formal = statement["canonical_formal_target"]
    assert formal["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert formal["statement_file_sha256"] == STATEMENT_SHA256
    assert sha256(STATEMENT_SOURCE) == STATEMENT_SHA256
    assert audit["canonical_target_expression_sha256"] == EXPRESSION_SHA256
    assert audit["canonical_statement_file_sha256"] == STATEMENT_SHA256
    canonical = serialized_expression(
        STATEMENT_SOURCE, STATEMENT_DECLARATION, "#print BinetFormulaTarget"
    )
    candidate_target = serialized_expression(SOURCE, AUDIT_DECLARATION, "#print ExactTarget")
    assert normalize_generated_proofs(canonical) == normalize_generated_proofs(candidate_target)
    assert hashlib.sha256(canonical.encode()).hexdigest() == EXPRESSION_SHA256

    env = audit["immutable_environment"]
    assert env["mathlib_revision"] == MATHLIB_REVISION
    assert env["mathlib_tree"] == MATHLIB_TREE
    assert output("git", "rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert output("git", "rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert output("git", "status", "--porcelain=v1", "--untracked-files=all", cwd=MATHLIB) == ""
    assert sha256(LEAN_ROOT / "lake-manifest.json") == env["manifest_sha256"]
    assert sha256(MATHLIB / "LICENSE") == env["mathlib_license_sha256"]
    manifest = load(LEAN_ROOT / "lake-manifest.json")
    for package in manifest["packages"]:
        package_path = LEAN_ROOT / ".lake" / "packages" / package["name"].strip("«»")
        assert output("git", "rev-parse", "HEAD", cwd=package_path) == package["rev"]
        assert output(
            "git", "status", "--porcelain=v1", "--untracked-files=all", cwd=package_path
        ) == ""

    candidates = audit["candidates"]
    candidate_ids = [row["candidate_id"] for row in candidates]
    assert len(candidate_ids) == len(set(candidate_ids)) == 7
    direct = next(row for row in candidates if row["candidate_id"] == "M0927-C01-MATHLIB-NATURAL-BINET")
    terminal = next(row for row in candidates if row["candidate_id"] == "M0927-C02-MATHLIB-FUNCTION-TERMINAL")
    assert direct["revision"] == MATHLIB_REVISION and direct["tree"] == MATHLIB_TREE
    assert direct["terminal_declaration"] == "Real.coe_fib_eq'"
    assert direct["terminal_candidate_id"] == terminal["candidate_id"]
    assert direct["machine_axioms"] == ["propext", "Classical.choice", "Quot.sound"]
    golden = MATHLIB / direct["file"]
    assert sha256(golden) == direct["source_sha256"]
    assert output("git", "rev-parse", f"HEAD:{direct['file']}", cwd=MATHLIB) == direct["source_git_blob"]
    assert hash_slice(golden, 180, 195) == terminal["proof_body_slice_sha256"]
    assert hash_slice(golden, 180, 200) == direct["natural_binet_block_sha256"]
    assert output(
        "git", "merge-base", "--is-ancestor", direct["introduction_revision"], "HEAD", cwd=MATHLIB
    ) == ""
    golden_source = golden.read_text(encoding="utf-8")
    for marker in (
        "theorem coe_fib_eq' :",
        "rw [fibRec.sol_eq_of_eq_init]",
        "exact fib_isSol_fibRec",
        "geom_goldenRatio_isSol_fibRec",
        "geom_goldenConj_isSol_fibRec",
        "theorem coe_fib_eq : ∀ n",
        "rw [← funext_iff, Real.coe_fib_eq']",
        "theorem coe_intFib_eq",
    ):
        assert marker in golden_source, marker
    natural_block = "".join(golden_source.splitlines(keepends=True)[179:208])
    assert not FORBIDDEN.search(without_comments(natural_block))

    course = next(row for row in candidates if row["candidate_id"] == "M0927-C04-LEANCOURSE-INDEPENDENT-EDUCATIONAL")
    assert course["revision"] == "390f7c49ce3ced7ad5ffcf74e039dcc8f912afdf"
    assert course["tree"] == "84470467c9eb38c337fe8d9a1c4acf6542d1cb26"
    assert course["source_sha256"] == "d34c58055142cc07f59d5de411c50dff34799a4407a26a178dda730d4b0bed16"
    assert course["candidate_machine_classification"].startswith("M5_")
    wrapper = next(row for row in candidates if row["candidate_id"] == "M0927-C05-AUTOMATH-DOWNSTREAM-WRAPPER")
    assert wrapper["revision"] == "f76f46f07a1a48d5c12a20c2f8d366bb9df9330d"
    assert wrapper["proof_body"] == "Directly returns Real.coe_fib_eq n."

    adapter = SOURCE.read_text(encoding="utf-8")
    for marker in (
        "def ExactTarget : Prop",
        "theorem exactTarget_mathlib_candidate : ExactTarget := by",
        "rw [Real.coe_fib_eq n]",
        "simp only [Real.goldenRatio, Real.goldenConj, div_pow]",
        "assert_no_sorry Real.coe_fib_eq'",
        "#print sorries exactTarget_mathlib_candidate",
        "#print axioms exactTarget_mathlib_candidate",
    ):
        assert marker in adapter, marker
    assert not FORBIDDEN.search(without_comments(adapter))

    lean = run_lean(SOURCE)
    if lean.returncode:
        sys.stdout.write(lean.stdout)
        raise SystemExit(lean.returncode)
    normalized = re.sub(r"\s+", " ", lean.stdout)
    if normalized.count("depends on axioms: [propext, Classical.choice, Quot.sound]") != 4:
        sys.stdout.write(lean.stdout)
        raise SystemExit("unexpected candidate axiom report")
    if lean.stdout.count("Declarations are sorry-free!") != 4:
        sys.stdout.write(lean.stdout)
        raise SystemExit("unexpected sorry-free report")
    if hashlib.sha256(lean.stdout.encode()).hexdigest() != LEAN_OUTPUT_SHA256:
        sys.stdout.write(lean.stdout)
        raise SystemExit("candidate Lean output changed")
    assert receipt["lean_output_sha256"] == LEAN_OUTPUT_SHA256

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
    assert instance["root_vector"] == {"H": "H1", "M": "M3", "R": "R4"}
    assert decision["kernel_closed_as_accepted_root"] is False
    assert audit["accepted_receipt_ids"] == receipt["accepted_receipt_ids"] == []
    assert audit["audit_complete"] is receipt["audit_complete"] is False
    assert audit["theorem_complete"] is receipt["theorem_complete"] is False

    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["verdict"] == "no_state_change"
    assert set(receipt["changed_paths"]) == CHANGED_PATHS
    assert receipt["candidate_result"]["classification"] == (
        "M0-W_candidate_pending_downstream_acceptance"
    )
    assert receipt["candidate_result"]["master_accepted"] is False

    if args.worker_packet:
        packet = load(args.worker_packet.resolve())
        assert set(packet) == {
            "item_id", "changed_paths", "commands", "output_summary",
            "base_revision", "known_failures", "state",
        }
        assert packet["item_id"] == ITEM_ID and packet["state"] == "[_]"
        assert packet["base_revision"] == BASE_REVISION
        assert set(packet["changed_paths"]) == CHANGED_PATHS
        assert packet["known_failures"] == receipt["known_failures"]

    for relative in CHANGED_PATHS - {".stage1-worker-selftest.json"}:
        check_text_file(ROOT / relative)

    print(
        "check_anchor_audit: ok "
        "(THM-M-0927; 7 records; exact pinned mathlib M0-W route candidate; "
        "accepted root remains H1/M3/R4; audit_complete=false; theorem_complete=false)"
    )


if __name__ == "__main__":
    main()
