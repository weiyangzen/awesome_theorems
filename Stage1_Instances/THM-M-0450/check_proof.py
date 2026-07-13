#!/usr/bin/env python3
"""Fail-closed structural checks for the THM-M-0450 proof phase."""

import json
import re
import hashlib
from pathlib import Path

HERE = Path(__file__).resolve().parent
source = (HERE / "Proof.lean").read_text()
receipt = json.loads((HERE / "proof-receipt.json").read_text())
graphs = json.loads((HERE / "typed-graphs.json").read_text())


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

required = {
    "fg_iff_of_addEquiv",
    "finiteIndex_iff_of_addEquiv",
    "comap_doubling_range",
    "doubling_finiteIndex_iff_of_addEquiv",
    "northcott_comp_addEquiv",
    "nonnegative_comp_addEquiv",
    "parallelogram_comp_addEquiv",
    "jacobian_fg_iff_affine_fg",
    "jacobian_doubling_finiteIndex_iff_affine",
    "exactTarget_of_descent_packages",
}
declared = set(re.findall(r"^(?:theorem|structure)\s+([A-Za-z0-9_]+)", source, re.MULTILINE))
missing = required - declared
if missing:
    raise SystemExit(f"proof check failed: missing declarations {sorted(missing)}")

if not re.search(r"^import Statement$", source, re.MULTILINE):
    raise SystemExit("proof check failed: canonical Statement import missing")
if not re.search(r"^import ObligationTree$", source, re.MULTILINE):
    raise SystemExit("proof check failed: frozen ObligationTree import missing")
if re.search(r"\b(sorry|admit|sorryAx)\b|^\s*(axiom|unsafe)\b", source, re.MULTILINE):
    raise SystemExit("proof check failed: prohibited proof device")
if "theorem exactTarget_of_descent_packages" not in source or "ExactTarget.{u}" not in source:
    raise SystemExit("proof check failed: exact canonical-root assembly missing")

if receipt["item_id"] != "S56-M-0450-PROOF" or receipt["theorem_id"] != "THM-M-0450":
    raise SystemExit("proof check failed: receipt identity mismatch")
proof_sha256 = sha256(HERE / "Proof.lean")
if receipt["proof_body"]["source_sha256"] != proof_sha256:
    raise SystemExit("proof check failed: proof source hash mismatch")
for key, filename in (
    ("statement_sha256", "Statement.lean"),
    ("obligation_tree_sha256", "ObligationTree.lean"),
    ("obligation_registry_sha256", "obligation-registry.json"),
    ("typed_graphs_sha256", "typed-graphs.json"),
):
    digest = sha256(HERE / filename)
    if receipt["inputs"][key] != digest:
        raise SystemExit(f"proof check failed: {filename} hash mismatch")
if receipt["result"]["root_closed"] or receipt["result"]["theorem_complete"]:
    raise SystemExit("proof check failed: false root closure claim")
if receipt["closed_obligation_ids"]:
    raise SystemExit("proof check failed: this bounded contribution closes no whole frozen obligation")
if receipt["inputs"]["registry_denominator_sha256"] != graphs["registry_denominator_sha256"]:
    raise SystemExit("proof check failed: registry denominator mismatch")
if receipt["remaining_root_cut_set"] != graphs["closure_boundary"]["remaining_root_cut_set"]:
    raise SystemExit("proof check failed: remaining root cut mismatch")
if receipt["recipe"]["network_policy"] != "not_enforced; no network operation was invoked":
    raise SystemExit("proof check failed: replay network-policy boundary mismatch")
content_hashes = receipt["repository_state"]["content_hashes_excluding_self_referential_receipt"]
for relative, expected in content_hashes.items():
    path = HERE.parent.parent / relative
    if sha256(path) != expected:
        raise SystemExit(f"proof check failed: untracked input hash mismatch for {relative}")
manifest = hashlib.sha256()
for relative in sorted(content_hashes):
    manifest.update(relative.encode() + b"\0" + content_hashes[relative].encode() + b"\0")
if manifest.hexdigest() != receipt["repository_state"]["manifest_sha256_excluding_self_referential_receipt"]:
    raise SystemExit("proof check failed: untracked input manifest mismatch")

print("PASS THM-M-0450 proof phase: model transports and exact conditional assembly checked")
print("root closure: open (M3); weak Mordell-Weil and elliptic height remain open")
