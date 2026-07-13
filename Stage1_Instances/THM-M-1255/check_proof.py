#!/usr/bin/env python3
"""Fail-closed structural checks for the THM-M-1255 partial proof receipt."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    proof = (HERE / "Proof.lean").read_text(encoding="utf-8")
    receipt = json.loads((HERE / "proof-receipt.json").read_text(encoding="utf-8"))
    registry = json.loads((HERE / "obligation-registry.json").read_text(encoding="utf-8"))

    assert receipt["item_id"] == "S56-M-1255-PROOF"
    assert receipt["theorem_id"] == "THM-M-1255"
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["closed_obligation_ids"] == ["M1255-L-COMMUTE", "M1255-C-ACTION"]
    assert receipt["accepted_closed_obligation_ids"] == []
    assert receipt["result"]["root_closed"] is False
    assert receipt["result"]["theorem_complete"] is False
    assert receipt["first_failed_gate"] == "M1255-C-FUNDSOL"
    assert receipt["remaining_root_cut_set"] == ["M1255-C-FUNDSOL"]

    expected_fingerprints = {
        "M1255-L-COMMUTE":
            "planned:v1:sha256:81a742d52cd376db421d328dd45e929f6375545ca056b7d9c71c0ce951be5246",
        "M1255-C-ACTION":
            "planned:v1:sha256:730b94199dfb6cd3044fa742c473e900947928457288e9bc46d90399501fcbc9",
    }
    registry_fingerprints = {
        entry["obligation_id"]: entry["statement_fingerprint"]
        for entry in registry["obligations"]
        if entry["obligation_id"] in expected_fingerprints
    }
    assert registry_fingerprints == expected_fingerprints
    assert receipt["obligation_statement_fingerprints"] == expected_fingerprints
    assert registry["denominator_sha256"] == receipt["inputs"]["registry_denominator_sha256"]

    input_files = {
        "statement_sha256": HERE / "Statement.lean",
        "obligation_tree_sha256": HERE / "ObligationTree.lean",
        "obligation_registry_sha256": HERE / "obligation-registry.json",
        "typed_graphs_sha256": HERE / "typed-graphs.json",
        "lean_toolchain_sha256": ROOT / "Formalizations/Lean/lean-toolchain",
        "lake_manifest_sha256": ROOT / "Formalizations/Lean/lake-manifest.json",
    }
    assert receipt["proof_body"]["source_sha256"] == sha256(HERE / "Proof.lean")
    for key, path in input_files.items():
        assert receipt["inputs"][key] == sha256(path), (key, path)

    required = [
        "theorem coordinateDerivatives_commute",
        "def coordinatePowers",
        "def exponentAction",
        "def polynomialAction",
        "theorem polynomialAction_map_X",
        "def polynomialActionPackage",
    ]
    assert all(fragment in proof for fragment in required)
    assert "FundamentalSolutionsFor polynomialActionPackage" not in proof
    assert "MalgrangeEhrenpreisTarget" not in proof
    prohibited = re.compile(
        r"\b(sorry|admit|sorryAx|implemented_by|native_decide|extern)\b"
        r"|^[ \t]*(axiom|constant|opaque|unsafe)\b",
        re.MULTILINE,
    )
    assert prohibited.search(proof) is None
    print("THM-M-1255 proof receipt checks: ok")


if __name__ == "__main__":
    main()
