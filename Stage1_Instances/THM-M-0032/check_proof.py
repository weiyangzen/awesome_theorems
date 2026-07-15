#!/usr/bin/env python3
"""Fail-closed checks for the M0032-N-DOMAIN partial proof packet."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ITEM = "S56-M-0032-PROOF"
THEOREM = "THM-M-0032"
BASE_REVISION = "20808d65f53d8801e78f061504b93bb7efd49489"
BASE_TREE = "a5bf33a278a7a285878c89177838ae1a0dcc9990"
DENOMINATOR_SHA256 = "7ddbec795ccfc7f42c1efc171aee6f2e8d1a82af6f5bb5d2382c926d64d451c7"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/DomainProof.lean",
    f"Stage1_Instances/{THEOREM}/check_proof.py",
    f"Stage1_Instances/{THEOREM}/check_proof.sh",
    f"Stage1_Instances/{THEOREM}/proof-execution-2026-07-15-slot67.md",
    f"Stage1_Instances/{THEOREM}/proof-receipt-partial-domain.json",
}


def reject_duplicates(pairs: list[tuple[str, object]]) -> dict:
    result: dict[str, object] = {}
    for key, value in pairs:
        assert key not in result, f"duplicate JSON key: {key}"
        result[key] = value
    return result


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates)
    assert isinstance(value, dict), path
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(["git", *args], cwd=cwd, text=True).strip()


def strip_comments_and_strings(source: str) -> str:
    out: list[str] = []
    index = 0
    depth = 0
    quoted = False
    escaped = False
    while index < len(source):
        pair = source[index:index + 2]
        char = source[index]
        if depth:
            if pair == "/-":
                depth += 1
                out.extend("  ")
                index += 2
            elif pair == "-/":
                depth -= 1
                out.extend("  ")
                index += 2
            else:
                out.append("\n" if char == "\n" else " ")
                index += 1
        elif quoted:
            out.append("\n" if char == "\n" else " ")
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                quoted = False
            index += 1
        elif pair == "/-":
            depth = 1
            out.extend("  ")
            index += 2
        elif pair == "--":
            end = source.find("\n", index)
            if end == -1:
                out.extend(" " * (len(source) - index))
                index = len(source)
            else:
                out.extend(" " * (end - index))
                index = end
        elif char == '"':
            quoted = True
            out.append(" ")
            index += 1
        else:
            out.append(char)
            index += 1
    assert depth == 0 and not quoted
    return "".join(out)


def main() -> None:
    proof_path = HERE / "DomainProof.lean"
    proof = proof_path.read_text(encoding="utf-8")
    receipt = load(HERE / "proof-receipt-partial-domain.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item["theorem_id"] == THEOREM and item["execution_rank"] == 1076
    assert item["phase"] == "proof" and item["layer"] == 4
    assert item["state"] in {"[ ]", "[_]", "[x]"}
    assert item["depends_on"] == ["S56-M-0032-OBLIGATION_TREE"]
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM}"]
    predecessor = next(
        row for row in execution["items"] if row["id"] == "S56-M-0032-OBLIGATION_TREE"
    )
    assert predecessor["state"] in {"[_]", "[x]"}

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|implemented_by|native_decide|run_tac)\b|"
        r"^[ \t]*(?:axiom|constant|opaque|unsafe|extern)\b",
        re.MULTILINE,
    )
    assert prohibited.search(strip_comments_and_strings(proof)) is None
    for marker in (
        "theorem regularLocalRing_isDomain",
        "theorem regularLocalDomainPackage",
        "ObligationTree.RegularLocalDomainPackage",
        "assert_no_sorry regularLocalRing_isDomain",
        "assert_no_sorry regularLocalDomainPackage",
        "#print axioms regularLocalRing_isDomain",
        "#print axioms regularLocalDomainPackage",
    ):
        assert marker in proof, marker

    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    by_id = {row["obligation_id"]: row for row in registry["obligations"]}
    assert by_id["M0032-N-DOMAIN"]["statement_fingerprint"] == (
        "planned:v1:sha256:1d178f6b95e0a58d2c40071bb37bfcf4eb13d344425b791f2db0c3647100ebfa"
    )
    assert by_id["M0032-A-PRIME-ELEMENT"]["terminal_proof_body_id"] is None

    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    assert git("rev-parse", "HEAD", cwd=mathlib) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == MATHLIB_TREE
    assert git("status", "--porcelain=v1", cwd=mathlib) == ""

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == packet["item_id"] == ITEM
    assert receipt["theorem_id"] == THEOREM
    assert receipt["base_revision"] == packet["base_revision"] == BASE_REVISION
    assert receipt["base_tree"] == BASE_TREE
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["verdict"] == "no_state_change"
    assert receipt["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert receipt["proof_body"]["source_sha256"] == sha256(proof_path)
    assert receipt["provisionally_closed_obligation_ids"] == ["M0032-N-DOMAIN"]
    assert receipt["accepted_closed_obligation_ids"] == []
    assert receipt["remaining_machine_proof_cut_set"] == ["M0032-A-PRIME-ELEMENT"]
    assert receipt["remaining_root_cut_set"] == [
        "M0032-A-PRIME-ELEMENT",
        "M0032-X-PRIMARY-SOURCE",
        "M0032-S-FOUNDATION",
        "M0032-X-PROVENANCE",
        "M0032-X-TRUST",
        "M0032-X-READABLE",
        "M0032-X-WORKFLOW",
    ]
    for key, filename in (
        ("statement_sha256", "Statement.lean"),
        ("obligation_tree_sha256", "ObligationTree.lean"),
        ("obligation_registry_sha256", "obligation-registry.json"),
        ("typed_graphs_sha256", "typed-graphs.json"),
        ("anchor_audit_sha256", "anchor-audit.json"),
        ("check_proof_py_sha256", "check_proof.py"),
        ("check_proof_sh_sha256", "check_proof.sh"),
    ):
        assert receipt["inputs"][key] == sha256(HERE / filename), key
    result = receipt["result"]
    assert result["exit_code"] == 0
    assert result["axioms"] == ["propext", "Classical.choice", "Quot.sound"]
    assert result["domain_package_kernel_closed"] is True
    assert result["root_kernel_closed"] is False
    assert result["audit_complete"] is result["theorem_complete"] is False

    assert set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert packet["state"] == "[_]"
    assert set(packet["changed_paths"]) == set(receipt["changed_paths"]) == CHANGED_PATHS
    assert packet["known_failures"] == receipt["known_failures"]
    status = subprocess.check_output(
        ["git", "status", "--short", "--untracked-files=all"], cwd=ROOT, text=True
    )
    actual_changed = {
        line[3:] for line in status.splitlines() if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual_changed == CHANGED_PATHS, (actual_changed, CHANGED_PATHS)

    execution_text = (HERE / "proof-execution-2026-07-15-slot67.md").read_text()
    assert "M0032-N-DOMAIN" in execution_text
    assert "theorem_complete=false" in execution_text
    for relative in CHANGED_PATHS - {".stage1-worker-selftest.json"}:
        data = (ROOT / relative).read_bytes()
        assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())

    print("PASS THM-M-0032 proof phase: M0032-N-DOMAIN body and evidence checked")
    print("exact root remains open on M0032-A-PRIME-ELEMENT; theorem_complete=false")


if __name__ == "__main__":
    main()
