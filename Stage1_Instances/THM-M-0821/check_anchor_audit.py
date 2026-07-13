#!/usr/bin/env python3
"""Validate the immutable THM-M-0821 anchor inventory and exact candidate."""

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
ITEM_ID = "S56-M-0821-ANCHOR_AUDIT"
THEOREM_ID = "THM-M-0821"
BASE_REVISION = "39704171d88ffcdc33a47365ae9791f855fa3a44"
BASE_TREE = "050ab5c6392560337051d2eadd1b82277dbe1c4f"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
EXPRESSION_SHA256 = "8f5d05428a35e3b6f13947097ac52417ba900b3cf9b1b45c0bb173766c914d7c"
STATEMENT_SHA256 = "572f1655ca4d40ce6e1ce1bf6567cee2d640eb54534569d8a8980dff184c0100"
PROTOCOL_SHA256 = "4e4ad386fbf8d4e2bad63c1ac3c3389f564260310f2cb81948ebc55742ab2f78"
LEAN_OUTPUT_SHA256 = "9b7df95ece298a00a837416bfcc3e9c492c90af5f5d256254f7a7d95c83bac23"
NAMESPACE = "Stage1Instances.THM_M_0821"
TARGET = "SpernerMaximumTarget"
CANDIDATE = "spernerMaximum_mathlib_candidate"
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


def serialized_expression(path: Path, marker: str) -> str:
    result = run_lean(path)
    if result.returncode:
        sys.stdout.write(result.stdout)
        raise SystemExit(result.returncode)
    index = result.stdout.rfind(marker)
    if index < 0:
        raise SystemExit(f"missing serialized target marker: {marker}")
    expression = result.stdout[index + len(marker):].strip()
    if "?m." in expression:
        raise SystemExit("unresolved metavariable in serialized target")
    return expression


def statement_expression() -> str:
    text = STATEMENT_SOURCE.read_text(encoding="utf-8")
    boundary = "/-- Equivalent concrete-witness form using the lower middle layer. -/"
    if text.count(boundary) != 1:
        raise SystemExit("statement canonical-target boundary is missing or ambiguous")
    prefix = text[: text.index(boundary)]
    fixture = prefix + f"\nend {NAMESPACE}\n\nset_option pp.explicit true in\n" \
        f"set_option pp.universes true in\n#print {NAMESPACE}.{TARGET}\n"
    with tempfile.NamedTemporaryFile(
        "w", suffix=".lean", dir=HERE, delete=False, encoding="utf-8"
    ) as handle:
        handle.write(fixture)
        temporary = Path(handle.name)
    try:
        return serialized_expression(
            temporary, f"def {NAMESPACE}.{TARGET}.{{u}} : Prop :=\n"
        )
    finally:
        temporary.unlink()


def candidate_expression() -> str:
    text = SOURCE.read_text(encoding="utf-8")
    candidate_print = (
        "set_option pp.explicit true in\n"
        "set_option pp.universes true in\n"
        f"#print {NAMESPACE}.{CANDIDATE}"
    )
    if text.count(candidate_print) != 1:
        raise SystemExit("candidate proof print marker is missing or ambiguous")
    proof_marker = "/-- Exact pinned-mathlib candidate for the full attainability-plus-bound target. -/"
    if text.count(proof_marker) != 1:
        raise SystemExit("candidate target/proof boundary is missing or ambiguous")
    text = (
        text[: text.index(proof_marker)]
        + f"\nend {NAMESPACE}\n\nset_option pp.explicit true in\n"
        + f"set_option pp.universes true in\n#print {NAMESPACE}.{TARGET}\n"
    )
    with tempfile.NamedTemporaryFile(
        "w", suffix=".lean", dir=HERE, delete=False, encoding="utf-8"
    ) as handle:
        handle.write(text)
        temporary = Path(handle.name)
    try:
        return serialized_expression(
            temporary, f"def {NAMESPACE}.{TARGET}.{{u}} : Prop :=\n"
        )
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
    manifest = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")

    assert audit["item_id"] == receipt["item_id"] == protocol["item_id"] == ITEM_ID
    assert audit["theorem_id"] == receipt["theorem_id"] == protocol["theorem_id"] == THEOREM_ID
    assert audit["execution_rank"] == 1379
    assert audit["base_revision"] == receipt["base_revision"] == BASE_REVISION
    assert audit["base_tree"] == receipt["base_tree"] == BASE_TREE
    assert output("git", "rev-parse", "HEAD") == BASE_REVISION
    assert output("git", "rev-parse", "HEAD^{tree}") == BASE_TREE
    assert protocol["saturation_claim"] is False
    assert sha256(PROTOCOL_PATH) == PROTOCOL_SHA256
    assert audit["discovery_protocol_sha256"] == PROTOCOL_SHA256

    target = next(row for row in manifest["targets"] if row["theorem_id"] == THEOREM_ID)
    assert target["execution_rank"] == 1379
    assert target["baseline"] == "L0" and target["rework_required"] is True
    assert target["theorem_complete"] is False
    item = next(row for row in execution["items"] if row["id"] == ITEM_ID)
    assert item["phase"] == "anchor_audit" and item["layer"] == 2
    assert item["state"] == "[ ]"
    assert item["depends_on"] == ["S56-M-0821-STATEMENT"]
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]
    prerequisite = next(
        row for row in execution["items"] if row["id"] == "S56-M-0821-STATEMENT"
    )
    assert prerequisite["state"] == "[_]"
    assert prerequisite["depends_on"] == ["S56-M-0821-INTAKE"]

    formal = statement["canonical_formal_target"]
    assert formal["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert formal["statement_file_sha256"] == STATEMENT_SHA256
    assert sha256(STATEMENT_SOURCE) == STATEMENT_SHA256
    assert audit["canonical_target"]["expression_sha256"] == EXPRESSION_SHA256
    assert audit["canonical_target"]["statement_file_sha256"] == STATEMENT_SHA256

    statement_serialized = statement_expression()
    candidate_serialized = candidate_expression()
    assert statement_serialized == candidate_serialized
    assert hashlib.sha256(statement_serialized.encode()).hexdigest() == EXPRESSION_SHA256

    env = audit["immutable_environment"]
    assert env["mathlib_revision"] == MATHLIB_REVISION
    assert env["mathlib_tree"] == MATHLIB_TREE
    assert output("git", "rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert output("git", "rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert output("git", "status", "--short", cwd=MATHLIB) == ""
    assert sha256(MATHLIB / "LICENSE") == env["mathlib_license_sha256"]
    assert sha256(LEAN_ROOT / "lake-manifest.json") == env["lake_manifest_sha256"]

    direct = next(c for c in audit["candidates"] if c["candidate_id"] == "M0821-C01-MATHLIB-COMPOSITE")
    assert direct["candidate_classification"] == "M0-W"
    assert direct["evidence_level"] == "E2" and direct["kernel_checked"] is True
    assert direct["accepted"] is False
    for source in direct["files"]:
        path = MATHLIB / source["path"]
        assert output("git", "rev-parse", f"HEAD:{source['path']}", cwd=MATHLIB) == source["blob"]
        assert sha256(path) == source["sha256"]
    lym = (MATHLIB / direct["files"][0]["path"]).read_text(encoding="utf-8")
    for marker in (
        "theorem _root_.IsAntichain.sperner",
        "lubell_yamamoto_meshalkin_inequality_sum_inv_choose h𝒜",
        "choose_le_middle _ _",
        "Provide equality cases.",
    ):
        assert marker in lym, marker

    source = SOURCE.read_text(encoding="utf-8")
    for marker in (
        "def SpernerMaximumTarget : Prop",
        "theorem spernerMaximum_mathlib_candidate : SpernerMaximumTarget",
        "Set.sized_powersetCard",
        "Set.Sized.isAntichain",
        "Finset.card_powersetCard",
        "exact hA.sperner",
        "#print axioms IsAntichain.sperner",
        "#print axioms spernerMaximum_mathlib_candidate",
    ):
        assert marker in source, marker
    forbidden = re.compile(r"\b(?:sorry|admit|sorryAx|axiom|constant|unsafe|opaque)\b")
    assert not forbidden.search(without_comments(source))
    for source_path in direct["files"]:
        actual = (MATHLIB / source_path["path"]).read_text(encoding="utf-8")
        assert not forbidden.search(without_comments(actual))

    candidate_ids = {candidate["candidate_id"] for candidate in audit["candidates"]}
    assert candidate_ids == {
        "M0821-C01-MATHLIB-COMPOSITE",
        "M0821-C02-ATLAS-SETSYSTEMS",
        "M0821-C03-ATLAS-ORDER",
        "M0821-C04-CAM-COMBI-LYM",
        "M0821-C05-SOLPIN-SPERNER-LEMMA",
    }
    solpin = next(c for c in audit["candidates"] if c["candidate_id"].endswith("SOLPIN-SPERNER-LEMMA"))
    assert solpin["candidate_classification"] == "M5"
    result = audit["audit_result"]
    assert result["inventory_classified"] is True
    assert result["source_boundary_coverage"].startswith("5/5 classified")
    assert result["candidate_classification"] == "M0-W"
    assert result["candidate_accepted_by_master"] is False
    assert result["root_machine_candidate_after"] == "M0-W"
    assert result["accepted_root_machine_debt_after"] == "M3"
    assert result["audit_complete"] is False and result["theorem_complete"] is False

    lean = run_lean(SOURCE)
    if lean.returncode:
        sys.stdout.write(lean.stdout)
        raise SystemExit(lean.returncode)
    normalized = re.sub(r"\s+", " ", lean.stdout)
    if normalized.count("propext, Classical.choice, Quot.sound") != 3:
        sys.stdout.write(lean.stdout)
        raise SystemExit("unexpected candidate axiom report")
    if "propext, Quot.sound" not in normalized:
        sys.stdout.write(lean.stdout)
        raise SystemExit("middle-layer antichain axiom report is missing")
    if "theorem IsAntichain.sperner" not in lean.stdout:
        sys.stdout.write(lean.stdout)
        raise SystemExit("terminal proof-body print is missing")
    if "sorryAx" in lean.stdout or "declaration uses 'sorry'" in lean.stdout:
        sys.stdout.write(lean.stdout)
        raise SystemExit("Lean output reports a proof placeholder")
    assert hashlib.sha256(lean.stdout.encode()).hexdigest() == LEAN_OUTPUT_SHA256
    assert receipt["lean_output_sha256"] == LEAN_OUTPUT_SHA256

    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert set(receipt["changed_paths"]) == CHANGED_PATHS
    assert receipt["candidate_result"]["classification"] == "M0-W"
    assert receipt["candidate_result"]["evidence_level"] == "E2"
    assert receipt["audit_complete"] is False and receipt["theorem_complete"] is False
    assert receipt["accepted_receipt_ids"] == []
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
        packet = load(args.worker_packet)
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

    for relative in CHANGED_PATHS - {".stage1-worker-selftest.json"}:
        check_text_file(ROOT / relative)

    print(
        "check_anchor_audit: ok "
        "(THM-M-0821; 5 classified candidates; exact pinned mathlib M0-W/E2 candidate; "
        "accepted root remains M3; audit_complete=false; theorem_complete=false)"
    )


if __name__ == "__main__":
    main()
