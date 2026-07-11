#!/usr/bin/env python3
"""Generate the frozen THM-M-0085 obligation registry and typed graphs."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def sha(data):
    if isinstance(data, str):
        data = data.encode()
    return hashlib.sha256(data).hexdigest()


def dump(name, value):
    (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n")


ids = [
    "M0085-ROOT", "M0085-B-INSTANCE", "M0085-A-BECK",
    "M0085-X-PROVENANCE", "M0085-W-RELEASE",
]
descriptions = {
    "M0085-ROOT": "Exact universally quantified creates-G-split-coequalizers target.",
    "M0085-B-INSTANCE": "Install the explicit CreatesColimitOfIsSplitPair G premise as the local typeclass instance required by the anchor.",
    "M0085-A-BECK": "Apply monadicOfCreatesGSplitCoequalizers to the same adjunction and project its eqv field.",
    "M0085-X-PROVENANCE": "Bind the terminal body, import, revisions, axiom report, and alias-deduplication record.",
    "M0085-W-RELEASE": "Publish a named canonical wrapper and execute later proof, validation, and release receipts.",
}
kinds = ["root", "bridge", "terminal_anchor", "certificate", "workflow_gate"]
terminal = "mathlib:Mathlib.CategoryTheory.Monad.Monadicity#CategoryTheory.Monad.monadicOfCreatesGSplitCoequalizers"
rows = []
for oid, kind in zip(ids, kinds):
    required = oid in ids[:3]
    rows.append({
        "obligation_id": oid,
        "statement_fingerprint": "sha256:" + sha(descriptions[oid]),
        "kind": kind,
        "root_relevant": True,
        "machine_eligibility": "required" if required else "informational",
        "human_source_eligibility": "required" if oid in (ids[0], ids[2]) else "not_applicable",
        "readable_eligibility": "required",
        "risk_class": "critical" if oid in (ids[0], ids[2], ids[3]) else "high",
        "exclusion_reason": None if required else "assurance_overlay_no_distinct_proof_credit",
        "terminal_proof_body_id": terminal if oid == ids[2] else None,
    })
fields = tuple(rows[0])
denominator = sha(json.dumps([{k: r[k] for k in fields} for r in rows], sort_keys=True, separators=(",", ":")))
registry = {
    "schema_version": "stage1-obligation-registry/1.0",
    "item_id": "S56-M-0085-OBLIGATION_TREE", "theorem_id": "THM-M-0085",
    "registry_version": 1, "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "Exact statement plus immutable pinned-anchor audit, frozen before the named proof wrapper and closure receipts.",
    "frozen_against_statement_sha256": sha((HERE / "Statement.lean").read_bytes()),
    "frozen_against_anchor_audit_sha256": sha((HERE / "anchor-audit.json").read_bytes()),
    "root_obligation_id": ids[0], "denominator_sha256": denominator,
    "frozen_denominators": {
        "inventory": ids,
        "required_machine": ids[:3],
        "required_human_source": [ids[0], ids[2]],
        "required_readable": ids,
        "informational_overlays": ids[3:],
    },
    "delta_policy": "Any correction, split, merge, exclusion, or eligibility change requires a new registry version and append-only old/new ID delta.",
    "obligations": rows,
}

nodes = []
for oid in ids:
    machine = "M0-P candidate" if oid in ids[:4] else "M3"
    nodes.append({
        "node_id": oid.lower(), "obligation_id": oid, "kind": rows[ids.index(oid)]["kind"],
        "human_statement": descriptions[oid],
        "formal_target": "Stage1.THM_M_0085.Statement" if oid == ids[0] else descriptions[oid],
        "output": descriptions[oid], "human_debt": "H3", "machine_debt": machine,
        "readability_debt": "R4", "evidence_ids": [],
        "source_crosswalk_id": "anchor-audit:S56-M-0085-C02" if oid in (ids[0], ids[2]) else None,
        "provenance_id": terminal if oid in (ids[2], ids[3]) else None,
        "foundation_profile": "Lean 4 dependent type theory; classical mathlib category theory",
        "tcb_profile": "Lean kernel 4.29.0 and pinned mathlib 8a178386ffc0f5fef0b77738bb5449d50efeea95",
        "computation_record": "No native computation or external certificate.", "step_budget": 8,
        "semantic_step_ledger": {"premises": [], "inference": descriptions[oid], "output": descriptions[oid], "outgoing_use": []},
        "public_readable_target": "obligation-tree.md#" + oid.lower(),
        "validation_spec_id": "VAL-" + oid, "status_boundary": "Frozen architecture; no accepted proof or release receipt.",
        "task_ids": ["S56-M-0085-OBLIGATION_TREE"], "owned_sources": ["Stage1_Instances/THM-M-0085"],
        "owner": "stage1-worker", "reviewer": "integration-master", "validity": "planned",
    })

edge_specs = {
    "proof": [(ids[0], ids[1], "proof_requires"), (ids[1], ids[0], "composes"),
              (ids[1], ids[2], "proof_requires"), (ids[2], ids[1], "composes")],
    "refinement": [(ids[0], ids[1], "logical_decomposition"), (ids[1], ids[2], "logical_decomposition")],
    "provenance": [(ids[2], ids[3], "provenance_of")],
    "evidence": [(ids[3], ids[2], "provenance_of")],
    "trust": [(ids[0], ids[3], "trusts")],
    "documentation": [(ids[0], ids[3], "documents")],
    "workflow": [(ids[3], ids[4], "workflow_depends_on")],
}
graphs = {}
counter = 0
for name, specs in edge_specs.items():
    edges = []
    for source, target, typ in specs:
        counter += 1
        edge = {"edge_id": f"E{counter:02d}", "from": source, "to": target, "type": typ}
        edges.append(edge)
    if name == "proof":
        for a, b in ((0, 1), (2, 3)):
            edges[a]["reciprocal_edge_id"] = edges[b]["edge_id"]
            edges[b]["reciprocal_edge_id"] = edges[a]["edge_id"]
    graphs[name] = {"edges": edges, "out": {i: [e["edge_id"] for e in edges if e["from"] == i] for i in ids},
                    "in": {i: [e["edge_id"] for e in edges if e["to"] == i] for i in ids}}

bundle = {
    "schema_version": "stage1-typed-graphs/1.0", "item_id": registry["item_id"], "theorem_id": registry["theorem_id"],
    "registry_denominator_sha256": denominator, "nodes": nodes, "graphs": graphs,
    "closure_boundary": {"candidate_composition_elaborated": True, "root_closed": False, "theorem_complete": False,
                         "minimal_open_root_cut": ["M0085-W-RELEASE"]},
}
recipes = [{"recipe_id": "VAL-" + oid, "obligation_id": oid,
            "command": "python3 Stage1_Instances/THM-M-0085/check_obligation_tree.py"} for oid in ids]
dump("obligation-registry.json", registry)
dump("typed-graphs.json", bundle)
dump("validation-specs.json", {"schema_version": "stage1-validation-specs/1.0", "item_id": registry["item_id"],
                               "theorem_id": registry["theorem_id"], "recipes": recipes})
print(denominator)
