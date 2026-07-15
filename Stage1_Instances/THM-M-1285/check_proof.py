#!/usr/bin/env python3
"""Narrow structural checks for the provisional THM-M-1285 proof receipt."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-1285"
PROOF_SHA256 = "bb9581ad1b9840d95c7a37b66221dd5234b5730268f6173efc9e8892bc07a8fb"
STATEMENT_SHA256 = "5b3e9ec5606263ee7aac7cd59ba0c7c91c1f8017ba41ada01f8c0327528ac5e6"
DENOMINATOR_SHA256 = "6e441bf6a37b0bb83ae0a752e94b30ebf47c8eb567a9284969e869f68b032e9c"
REGISTRY_SHA256 = "b3efcc1e3e14dcf4798268f8017f67a924c0c25a996bea06255d9ed3cc4ef68a"
GRAPHS_SHA256 = "e97017ba4c2f659866a5ce8fff8f3cd6a2e7b32191f04b8c9d98353fe320d219"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


assert digest(HERE / "Proof.lean") == PROOF_SHA256
assert digest(HERE / "Statement.lean") == STATEMENT_SHA256
assert digest(HERE / "obligation-registry.json") == REGISTRY_SHA256
assert digest(HERE / "typed-graphs.json") == GRAPHS_SHA256

source = (HERE / "Proof.lean").read_text(encoding="utf-8")
for required in (
    "theorem volume_ball_radiusForVolume",
    "theorem distribution_iSup_rat_gt",
    "theorem strictSuperlevel_starProfile",
    "theorem measure_strictSuperlevel_starProfile",
    "theorem schwarzRearrangementTarget_proof : SchwarzRearrangementTarget",
    "#print axioms schwarzRearrangementTarget_proof",
):
    assert required in source, required
stripped = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
stripped = re.sub(r"--.*", "", stripped)
prohibited = re.compile(
    r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by)\b"
    r"|^[ \t]*(?:axiom|constant|opaque|unsafe|extern)\b",
    re.MULTILINE,
)
assert prohibited.search(stripped) is None

registry = json.loads((HERE / "obligation-registry.json").read_text(encoding="utf-8"))
graphs = json.loads((HERE / "typed-graphs.json").read_text(encoding="utf-8"))
assert "M1285-ROOT" in json.dumps(registry, sort_keys=True)
assert "M1285-T-PACKAGE" in json.dumps(graphs, sort_keys=True)
assert registry["denominator_sha256"] == DENOMINATOR_SHA256

dag = json.loads((ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json").read_text())
matches = []


def find_item(value: object) -> None:
    if isinstance(value, dict):
        if value.get("id") == "S56-M-1285-PROOF":
            matches.append(value)
        for child in value.values():
            find_item(child)
    elif isinstance(value, list):
        for child in value:
            find_item(child)


find_item(dag)
assert len(matches) == 1
item = matches[0]
assert item["theorem_id"] == "THM-M-1285"
assert item["phase"] == "proof"
assert item["depends_on"] == ["S56-M-1285-OBLIGATION_TREE"]
assert item["owned_paths"] == ["Stage1_Instances/THM-M-1285"]

mathlib = (ROOT / "Formalizations/Lean/.lake/packages/mathlib").resolve()
assert subprocess.check_output(
    ["git", "-C", str(mathlib), "rev-parse", "HEAD"], text=True
).strip() == MATHLIB_REVISION
assert subprocess.check_output(
    ["git", "-C", str(mathlib), "rev-parse", "HEAD^{tree}"], text=True
).strip() == MATHLIB_TREE
assert subprocess.check_output(
    ["git", "-C", str(mathlib), "status", "--short"], text=True
).strip() == ""

receipt = json.loads((HERE / "proof-receipt.json").read_text(encoding="utf-8"))
assert receipt["item_id"] == "S56-M-1285-PROOF"
assert receipt["canonical_target"] == (
    "Stage1Instances.THM_M_1285.SchwarzRearrangementTarget"
)
assert receipt["registry_denominator_sha256"] == DENOMINATOR_SHA256
assert receipt["proof_body"]["source_sha256"] == PROOF_SHA256
assert receipt["inputs"]["obligation_registry_sha256"] == REGISTRY_SHA256
assert receipt["inputs"]["typed_graphs_sha256"] == GRAPHS_SHA256
assert set(receipt["provisionally_closed_obligation_ids"]) == set(
    receipt["obligation_body_map"]
)
registry_fingerprints = {
    obligation["obligation_id"]: obligation["statement_fingerprint"]
    for obligation in registry["obligations"]
}
assert receipt["obligation_statement_fingerprints"] == {
    obligation_id: registry_fingerprints[obligation_id]
    for obligation_id in receipt["provisionally_closed_obligation_ids"]
}
assert receipt["result"]["root_kernel_closed"] is True
assert receipt["result"]["theorem_complete"] is False
assert receipt["accepted"] is False
assert receipt["proposed_state"] == "[_]"

packet = json.loads((ROOT / ".stage1-worker-selftest.json").read_text(encoding="utf-8"))
assert packet["item_id"] == receipt["item_id"]
assert packet["base_revision"] == receipt["base_revision"]
assert packet["changed_paths"] == receipt["changed_paths"]
assert packet["known_failures"] == receipt["known_failures"]
assert packet["state"] == "[_]"

print(
    "PASS THM-M-1285 proof structure: exact root body, hashes, frozen IDs, "
    "provisional receipt, and worker packet agree"
)
