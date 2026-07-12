#!/usr/bin/env python3
"""Build the frozen THM-M-1146 obligation registry and typed graph bundle."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-1146-OBLIGATION_TREE"
THEOREM = "THM-M-1146"
ROOT_HASH = "14336b88fd9aa11228ee9c7a86cc56a3473702bc2f8d77e266f2b4d37deef53d"

# id, kind, statement, formal target, output, risk, machine, human, budget
SPECS = [
    ("M1146-ROOT", "root", "The exact frozen harmonic Schwarz reflection target.", "Stage1Instances.THM_M_1146.SchwarzReflectionTarget", "Harmonicity on V and agreement on upperPart V.", "critical", "required", "required", 20),
    ("M1146-S-DEFS", "definition", "Freeze upperPart, reflectingPart, and the signed piecewise reflection.", "Stage1Instances.THM_M_1146.{upperPart,reflectingPart,oddReflection}", "The exact sets and reflected function used downstream.", "high", "required", "not_applicable", 20),
    ("M1146-S-DOMAIN", "normalization", "Derive membership of conjugate points and the upper/lower/axis trichotomy inside V.", "planned exact lemmas over V and Complex.im", "An exhaustive reflection-stable partition of V.", "high", "required", "required", 50),
    ("M1146-S-BOUNDARY", "branch", "Handle points with imaginary part zero, including empty reflecting parts and domains without endpoints in V.", "planned exact axis and degenerate-domain lemmas", "Boundary cases matching the canonical quantifiers.", "high", "required", "required", 50),
    ("M1146-S-FOUNDATION", "certificate", "Audit transitive axioms, imports, analytic definitions, and the Lean/mathlib TCB.", "planned transitive axiom and trust report", "An accepted foundation and trust profile.", "critical", "required", "not_applicable", 50),
    ("M1146-N-LOCALITY", "reduction", "Reduce HarmonicOnNhd on V to local upper, lower, and axis obligations.", "planned pointwise/locality reduction for HarmonicOnNhd", "Three local branches whose conclusions cover V.", "critical", "required", "required", 70),
    ("M1146-B-UPPER", "branch", "On positive imaginary part, identify oddReflection u with u on a neighborhood and transfer hu.", "planned upper-branch HarmonicOnNhd theorem", "Harmonicity of oddReflection on upperPart V.", "high", "required", "required", 60),
    ("M1146-B-LOWER", "branch", "On negative imaginary part, identify oddReflection u with -u after conjugation.", "planned lower-branch HarmonicOnNhd theorem", "Harmonicity of oddReflection on the strict lower part of V.", "critical", "required", "required", 80),
    ("M1146-B-AXIS", "branch", "Prove harmonicity at every point of reflectingPart V rather than only on either open side.", "planned axis-neighborhood HarmonicAt theorem", "Harmonicity of oddReflection at reflecting-axis points.", "critical", "required", "required", 100),
    ("M1146-B-MERGE", "terminal", "Recombine the exhaustive upper/lower/axis split into harmonicity on all of V.", "Stage1Instances.THM_M_1146.ReflectedHarmonicPackage (planned body)", "ReflectedHarmonicPackage.", "critical", "required", "required", 40),
    ("M1146-C-REFLECTION", "construction", "Establish branch identities, axis compatibility, and continuity of the odd piecewise construction.", "planned exact construction package for oddReflection", "A continuous, compatible piecewise reflection on V.", "critical", "required", "required", 100),
    ("M1146-L-CONJUGATION", "bridge", "Prove precomposition by complex conjugation preserves real-valued harmonicity on reflected neighborhoods.", "planned HarmonicAt/HarmonicOnNhd conjugation-precomposition theorem", "Harmonicity of u composed with conjugation on reflected lower neighborhoods.", "critical", "required", "required", 100),
    ("M1146-L-GLUING", "core_lemma", "Prove the continuous odd reflection is harmonic across the axis using a checked mean-value or equivalent analytic gluing argument.", "planned boundary harmonic-gluing theorem", "Harmonicity at every reflecting-axis point.", "critical", "required", "required", 100),
    ("M1146-X-ANCHORS", "bridge", "Integrate and type-check the pinned negation, locality, conjugation-map, and mean-value ingredients without crediting them as root closure.", "pinned mathlib supporting declarations recorded in anchor-audit.json", "Checked supporting interfaces for the analytic branches.", "high", "required", "not_applicable", 70),
    ("M1146-T-ASSEMBLE", "transport", "Combine reflected harmonicity with checked upper-branch agreement to yield the exact canonical target.", "Stage1Instances.THM_M_1146.schwarzReflectionTarget_of_reflectedHarmonicPackage", "SchwarzReflectionTarget conditional on ReflectedHarmonicPackage.", "high", "required", "required", 10),
    ("M1146-X-SOURCE", "terminal", "Map Axler-Bourdon-Ramey Theorem 4.12 proof transitions to every material analytic node and obtain independent review.", "human source boundary; no Lean proposition", "Reviewed source crosswalk for the complete proof architecture.", "high", "not_applicable", "required", 70),
    ("M1146-X-PROVENANCE", "certificate", "Classify each local/imported terminal body and its transitive conclusion provenance.", "planned proof-body provenance closure", "Content-addressed terminal-body provenance.", "critical", "informational", "not_applicable", 50),
    ("M1146-X-TRUST", "certificate", "Record automation, computation, executable, artifact, and dependency trust boundaries.", "planned release trust record", "Replayable release trust boundary.", "critical", "informational", "not_applicable", 50),
]


def fingerprint(oid, target):
    if oid == "M1146-ROOT":
        return "lean-expression-sha256:" + ROOT_HASH
    return "planned:v1:sha256:" + hashlib.sha256((oid + "\0" + target).encode()).hexdigest()


obligations = []
nodes = []
for oid, kind, statement, target, output, risk, machine, human, budget in SPECS:
    body = ("local:Stage1_Instances/THM-M-1146/ObligationTree.lean#"
            "schwarzReflectionTarget_of_reflectedHarmonicPackage") if oid == "M1146-T-ASSEMBLE" else None
    obligations.append({
        "obligation_id": oid, "statement_fingerprint": fingerprint(oid, target), "kind": kind,
        "root_relevant": True, "machine_eligibility": machine,
        "human_source_eligibility": human, "readable_eligibility": "required",
        "risk_class": risk,
        "exclusion_reason": ("human_source_boundary_only" if machine == "not_applicable" else
                             "provenance_or_trust_overlay_no_proof_credit" if machine == "informational" else None),
        "terminal_proof_body_id": body,
    })
    closed = oid == "M1146-T-ASSEMBLE"
    nodes.append({
        "node_id": f"THM-M-1146-{oid[6:]}", "obligation_id": oid, "kind": kind,
        "human_statement": statement, "formal_target": target, "output": output,
        "human_debt": "H3", "machine_debt": "M0-L" if closed else ("M3" if oid == "M1146-ROOT" else "M4"),
        "readability_debt": "R3", "evidence_ids": [],
        "source_crosswalk_id": "ABR-HFT-4.12-node-map-pending-review" if human == "required" else "not-applicable",
        "provenance_id": body or "none",
        "foundation_profile": "lean4-mathlib-classical/policy-audit-pending",
        "tcb_profile": "lean-4.29.0+mathlib-8a178386/transitive-closure-pending",
        "computation_record": "none; no oracle, native computation, or experiment is credited",
        "step_budget": budget,
        "semantic_step_ledger": {
            "premises": "Only the exact formal context and incoming proof_requires conclusions.",
            "inference": statement, "output": output,
            "outgoing_use": "Consumed only by a declared reciprocal composition edge or non-proof support edge.",
        },
        "public_readable_target": f"Stage1_Instances/THM-M-1146/obligation-tree.md#{oid.lower()}",
        "validation_spec_id": f"VAL-{oid}",
        "status_boundary": "Frozen architecture or conditional interface only; no undeclared premise and no root proof is supplied.",
        "task_ids": [ITEM, "S56-M-1146-PROOF"], "owned_sources": [],
        "owner": "THM-M-1146 proof lane", "reviewer": "independent Stage1 integration lane",
        "validity": {"validated_at": "2026-07-12" if closed else None,
                     "review_due": "before proof acceptance",
                     "invalidation_inputs": ["Statement.lean", "anchor-audit.json", "registry", "toolchain"],
                     "revocation_state": "provisional" if closed else "open"},
    })

FIELDS = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility",
          "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason",
          "terminal_proof_body_id")
projection = [{key: row[key] for key in FIELDS} for row in obligations]
denominator = hashlib.sha256(json.dumps(projection, sort_keys=True, separators=(",", ":")).encode()).hexdigest()

registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_version": 1, "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "Exact elaborated statement and immutable anchor audit; odd-reflection locality/conjugation/axis-gluing route selected before closure metrics.",
    "frozen_against_statement_sha256": hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest(),
    "frozen_against_anchor_audit_sha256": hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest(),
    "root_obligation_id": "M1146-ROOT", "denominator_sha256": denominator,
    "frozen_denominators": {
        "inventory": [r["obligation_id"] for r in obligations],
        "required_machine": [r["obligation_id"] for r in obligations if r["machine_eligibility"] == "required"],
        "required_human_source": [r["obligation_id"] for r in obligations if r["human_source_eligibility"] == "required"],
        "required_readable": [r["obligation_id"] for r in obligations],
        "informational_overlays": [r["obligation_id"] for r in obligations if r["machine_eligibility"] == "informational"],
    },
    "delta_policy": "Any correction, split, merge, exclusion, or eligibility change creates a new registry version and append-only old/new ID delta.",
    "obligations": obligations, "append_only_delta": [],
    "status_observed_after_freeze": {"closed_obligations": ["M1146-T-ASSEMBLE"], "root_machine_debt": "M3"},
    "status_boundary": "The conditional assembly interface is checked; conjugation preservation and axis gluing remain open, so the root is not proved.",
}

PAIRS = [
    ("M1146-ROOT", "M1146-B-MERGE"), ("M1146-ROOT", "M1146-T-ASSEMBLE"),
    ("M1146-B-MERGE", "M1146-N-LOCALITY"),
    ("M1146-N-LOCALITY", "M1146-B-UPPER"), ("M1146-N-LOCALITY", "M1146-B-LOWER"),
    ("M1146-N-LOCALITY", "M1146-B-AXIS"), ("M1146-B-UPPER", "M1146-S-DEFS"),
    ("M1146-B-UPPER", "M1146-S-DOMAIN"), ("M1146-B-LOWER", "M1146-L-CONJUGATION"),
    ("M1146-B-LOWER", "M1146-C-REFLECTION"), ("M1146-B-AXIS", "M1146-L-GLUING"),
    ("M1146-B-AXIS", "M1146-S-BOUNDARY"), ("M1146-L-GLUING", "M1146-C-REFLECTION"),
    ("M1146-L-CONJUGATION", "M1146-X-ANCHORS"), ("M1146-L-GLUING", "M1146-X-ANCHORS"),
]
proof_edges = []
for parent, child in PAIRS:
    req, cmp = f"REQ-{parent}-{child}", f"CMP-{child}-{parent}"
    proof_edges += [{"edge_id": req, "from": parent, "type": "proof_requires", "to": child, "reciprocal_edge_id": cmp},
                    {"edge_id": cmp, "from": child, "type": "composes", "to": parent, "reciprocal_edge_id": req}]

OTHER = {
    "refinement": [("REF-ROOT-DEFS", "M1146-ROOT", "logical_decomposition", "M1146-S-DEFS")],
    "provenance": [("SRC-GLUE", "M1146-L-GLUING", "source_map", "M1146-X-SOURCE"),
                   ("SRC-CONJ", "M1146-L-CONJUGATION", "source_map", "M1146-X-SOURCE"),
                   ("PROV-ROOT", "M1146-X-PROVENANCE", "provenance_of", "M1146-ROOT")],
    "evidence": [],
    "trust": [("TRUST-FOUND", "M1146-ROOT", "trusts", "M1146-S-FOUNDATION"),
              ("TRUST-RELEASE", "M1146-ROOT", "trusts", "M1146-X-TRUST")],
    "documentation": [("DOC-SOURCE", "M1146-X-SOURCE", "documents", "M1146-ROOT"),
                      ("DOC-BOUNDARY", "M1146-S-BOUNDARY", "documents", "M1146-B-AXIS")],
    "workflow": [("FLOW-PROOF", "M1146-B-MERGE", "workflow_depends_on", "M1146-N-LOCALITY"),
                 ("FLOW-PROV", "M1146-X-PROVENANCE", "workflow_depends_on", "M1146-T-ASSEMBLE")],
}


def graph(edges):
    cooked = edges if not edges or isinstance(edges[0], dict) else [
        {"edge_id": a, "from": b, "type": c, "to": d} for a, b, c, d in edges]
    incoming, outgoing = {}, {}
    for edge in cooked:
        outgoing.setdefault(edge["from"], []).append(edge["edge_id"])
        incoming.setdefault(edge["to"], []).append(edge["edge_id"])
    return {"edges": cooked, "out": outgoing, "in": incoming}


bundle = {
    "schema_version": "stage1-typed-graphs/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_id": "THM-M-1146-OBLIGATIONS-v1", "registry_denominator_sha256": denominator,
    "root_node_id": "M1146-ROOT",
    "edge_direction": "Proof requirements run parent to child; reciprocal composes edges run child to parent.",
    "nodes": nodes, "graphs": {"proof": graph(proof_edges), **{name: graph(edges) for name, edges in OTHER.items()}},
    "closure_boundary": {"closed_obligations": ["M1146-T-ASSEMBLE"], "root_closed": False,
                         "audit_complete": False, "theorem_complete": False,
                         "remaining_root_cut_set": ["M1146-B-MERGE"],
                         "composition_certificates": ["Stage1Instances.THM_M_1146.schwarzReflectionTarget_of_reflectedHarmonicPackage"],
                         "reason": "Exact assembly is checked, but ReflectedHarmonicPackage, especially conjugation and axis gluing, is open."},
}

(HERE / "obligation-registry.json").write_text(json.dumps(registry, indent=2) + "\n")
(HERE / "typed-graphs.json").write_text(json.dumps(bundle, indent=2) + "\n")
print(f"generated {len(obligations)} obligations; denominator {denominator}")
