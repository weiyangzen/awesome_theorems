#!/usr/bin/env python3
"""Validate the structured S56-M-0626-STATEMENT handoff without changing state."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[2]
OWNED = Path(__file__).resolve().parent
ITEM_ID = "S56-M-0626-STATEMENT"
THEOREM_ID = "THM-M-0626"
BASE = "0f70149d61a952d44f907f4662a143372bcb4c44"
TREE = "35328e4f56f47446a4e1dfdbe361a1b70a4b18a7"
EXPRESSION_HASH = "5c32b45abf131975cd4673ca095ca1a8e0122e4104bf616a4afab09a03289231"
ENVIRONMENT_HASH = "aee8c1e19573413be5fb0ad0c854de55a1cfc41e45f473e37b2a886c9b587eac"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def command(*argv: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(argv, cwd=cwd, text=True).strip()


def main() -> None:
    statement = load(OWNED / "statement.json")
    receipt = load(OWNED / "statement-receipt.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")
    execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")
    assigned = next(item for item in execution["items"] if item["id"] == ITEM_ID)

    assert assigned == {
        "id": ITEM_ID,
        "theorem_id": THEOREM_ID,
        "execution_rank": 1320,
        "phase": "statement",
        "layer": 1,
        "state": "[ ]",
        "depends_on": ["S56-M-0626-INTAKE"],
        "owned_paths": ["Stage1_Instances/THM-M-0626"],
        "deliverable": "Elaborate the exact Lean 4 target with the minimal pinned imports.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }

    assert statement["item_id"] == receipt["item_id"] == packet["item_id"] == ITEM_ID
    assert statement["theorem_id"] == receipt["theorem_id"] == THEOREM_ID
    assert receipt["phase"] == assigned["phase"]
    assert receipt["assigned_layer"] == assigned["layer"]
    assert receipt["authoritative_state_before"] == assigned["state"]
    assert receipt["completion_gate"] == assigned["completion_gate"]
    assert receipt["proposed_state"] == packet["state"] == "[_]"
    assert receipt["accepted"] is False and receipt["content_addressed"] is False
    assert receipt["accepted_receipt_ids"] == statement["accepted_receipt_ids"] == []
    assert statement["statement_elaborated"] is True
    assert statement["theorem_proved"] is False
    assert statement["audit_complete"] is receipt["audit_complete"] is False
    assert statement["theorem_complete"] is receipt["theorem_complete"] is False
    assert statement["root_vector_before"] == statement["root_vector_after"] == {
        "H": "H1", "M": "M3", "R": "R4"
    }
    assert receipt["root_vector_before"] == receipt["root_vector_after"] == {
        "H": "H1", "M": "M3", "R": "R4"
    }

    formal = statement["canonical_formal_target"]
    assert formal["declaration_or_expression"] == receipt["canonical_declaration"] == (
        "Stage1Instances.THM_M_0626.ConnectedImageTarget"
    )
    assert formal["elaborated_expression_sha256"] == (
        receipt["elaborated_expression_sha256"]
    ) == EXPRESSION_HASH
    assert formal["environment_fingerprint_sha256"] == (
        receipt["environment_fingerprint_sha256"]
    ) == ENVIRONMENT_HASH
    assert formal["unresolved_metavariables"] is receipt["unresolved_metavariables"] is False
    assert statement["direct_imports"] == receipt["direct_imports"] == [
        "Mathlib.Topology.Connected.Basic"
    ]
    assert len(receipt["mutation_tests"]) == 5
    assert {mutation["kind"] for mutation in receipt["mutation_tests"]} >= {
        "removed_hypothesis", "changed_domain", "changed_binder_scope", "boundary_case"
    }
    assert receipt["proof_body_locations"] == []
    assert receipt["canonical_obligation_ids"] == []
    assert receipt["typed_graph_changes"] == []
    assert receipt["composition_certificates"] == []

    expected_changed = [
        ".stage1-worker-selftest.json",
        "Stage1_Instances/THM-M-0626/README.md",
        "Stage1_Instances/THM-M-0626/Statement.lean",
        "Stage1_Instances/THM-M-0626/check_statement.py",
        "Stage1_Instances/THM-M-0626/check_statement_artifacts.py",
        "Stage1_Instances/THM-M-0626/statement.json",
        "Stage1_Instances/THM-M-0626/statement-receipt.json",
        "Stage1_Instances/THM-M-0626/statement-validation.md",
    ]
    assert receipt["changed_paths"] == packet["changed_paths"] == expected_changed
    assert receipt["base_revision"] == packet["base_revision"] == BASE
    assert receipt["base_tree"] == TREE
    assert packet.keys() == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state"
    }
    assert packet["commands"] and all(isinstance(item, str) and item for item in packet["commands"])
    assert packet["known_failures"]

    hash_fields = {
        "statement_file_sha256": OWNED / "Statement.lean",
        "statement_record_sha256": OWNED / "statement.json",
        "checker_sha256": OWNED / "check_statement.py",
    }
    for field, path in hash_fields.items():
        assert receipt[field] == sha256(path), f"hash mismatch: {field}"
    for path_string, tagged_hash in receipt["source_inputs"].items():
        algorithm, expected = tagged_hash.split(":", 1)
        assert algorithm == "sha256"
        assert sha256(ROOT / path_string) == expected, f"source hash mismatch: {path_string}"
    for path_string, tagged_hash in receipt["public_projection_hashes"].items():
        algorithm, expected = tagged_hash.split(":", 1)
        assert algorithm == "sha256"
        assert sha256(ROOT / path_string) == expected, f"projection hash mismatch: {path_string}"

    raw_expression = statement["elaborated_expression"]
    assert hashlib.sha256(raw_expression.encode("utf-8")).hexdigest() == EXPRESSION_HASH
    environment = {
        "direct_imports": [
            {
                "module": "Mathlib.Topology.Connected.Basic",
                "source_sha256": "929f0e1c789b8c0ed10c3164aa174e369b9b250317c525a8ad2f2dcca2a65e9c",
            }
        ],
        "lake_manifest_sha256": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
        "lean_toolchain": "leanprover/lean4:v4.29.0",
        "lean_version": "Lean (version 4.29.0, x86_64-unknown-linux-gnu, commit 98dc76e3c0a9b856c9b98726b713fb04fab16740, Release)",
        "mathlib_revision": MATHLIB_REVISION,
        "mathlib_tree": "bdc39a3123201dae413a9d9be56ec242c19e5c2b",
        "namespace": "Stage1Instances.THM_M_0626",
        "serialization_options": ["pp.explicit=true", "pp.universes=true"],
        "universes": ["u", "v"],
    }
    serialized_environment = json.dumps(
        environment, ensure_ascii=True, separators=(",", ":"), sort_keys=True
    )
    assert hashlib.sha256(serialized_environment.encode("utf-8")).hexdigest() == ENVIRONMENT_HASH

    assert command("git", "rev-parse", "HEAD") == BASE
    assert command("git", "rev-parse", "HEAD^{tree}") == TREE
    mathlib = ROOT / "Formalizations" / "Lean" / ".lake" / "packages" / "mathlib"
    assert command("git", "rev-parse", "HEAD", cwd=mathlib) == MATHLIB_REVISION
    assert command("git", "status", "--short", cwd=mathlib) == ""

    for path in [
        OWNED / "README.md",
        OWNED / "Statement.lean",
        OWNED / "check_statement.py",
        OWNED / "check_statement_artifacts.py",
        OWNED / "statement.json",
        OWNED / "statement-receipt.json",
        OWNED / "statement-validation.md",
        ROOT / ".stage1-worker-selftest.json",
    ]:
        data = path.read_bytes()
        assert data.endswith(b"\n"), f"missing final newline: {path}"
        assert b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())

    print(
        "statement artifact check: ok "
        "(THM-M-0626 exact target; five mutations; statement-only; theorem_complete=false)"
    )


if __name__ == "__main__":
    main()
