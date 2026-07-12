#!/usr/bin/env python3
"""Build the frozen THM-M-0667 obligation registry and typed graphs."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
STATEMENT_HASH = "5e34e0af4e8fd26edeebd02c2494f0efa7e14d4b340b23004e479c186815e7ab"


def sha(text):
    return hashlib.sha256(text.encode()).hexdigest()


# id, kind, statement, formal target, output, machine eligibility, source eligibility, risk, budget
SPECS = [
    ("M0667-ROOT", "root", "The frozen binary Ackermann function is not primitive recursive.",
     "Stage1Instances.THM_M_0667.AckermannNondefinabilityTarget", "Not (Primrec2 Nat.ack)", "required", "required", "critical", 7),
    ("M0667-S-NORMALIZATION", "definition", "Fix mathlib's two-variable Ackermann-Peter recursion and all zero/successor boundaries.",
     "Nat.ack with ack_zero, ack_succ_zero, ack_succ_succ", "The exact selected function normalization.", "required", "required", "high", 8),
    ("M0667-S-ENCODING", "transport", "Relate Primrec2 to uncurried and Nat.unpaired unary encodings.",
     "ackermannNondefinabilityTarget_iff_expandedTarget and _iff_unpairedNat", "Checked representation equivalences.", "required", "not_applicable", "high", 5),
    ("M0667-N-DIAGONAL", "reduction", "Restrict a hypothetical binary primitive-recursive Ackermann function to its diagonal.",
     "Primrec2 ack -> Primrec (fun n => ack n n)", "Primitive recursiveness of the diagonal.", "required", "required", "critical", 4),
    ("M0667-T-NAT-BRIDGE", "transport", "Move the diagonal predicate through Primrec.nat_iff.",
     "Primrec (fun n => ack n n) -> Nat.Primrec (fun n => ack n n)", "The inductive Nat.Primrec representation.", "required", "not_applicable", "high", 2),
    ("M0667-N-DOMINATION", "core_lemma", "Every unary Nat.Primrec function is pointwise dominated by one fixed Ackermann level.",
     "Stage1Instances.THM_M_0667.DominationPackage", "A level m dominating f at every input.", "required", "required", "critical", "split-required"),
    ("M0667-B-CONSTRUCTORS", "branch", "Prove domination by induction over all Nat.Primrec constructors.",
     "zero/succ/left/right/pair/comp/prec cases", "Constructor-complete domination proof.", "required", "required", "critical", "split-required"),
    ("M0667-L-BASE", "case_split", "Discharge zero, successor, and projection constructor cases.",
     "Nat.Primrec.zero/succ/left/right domination cases", "Base constructor bounds.", "required", "required", "normal", 18),
    ("M0667-L-PAIR-COMP", "case_split", "Close pairing and composition using maximum levels and Ackermann growth bounds.",
     "Nat.Primrec.pair and Nat.Primrec.comp domination cases", "Closure under pair and composition.", "required", "required", "high", 28),
    ("M0667-L-PREC", "case_split", "Close primitive recursion by induction on the recursion counter and pairing estimates.",
     "Nat.Primrec.prec domination case", "Closure under primitive recursion.", "required", "required", "critical", "split-required"),
    ("M0667-L-GROWTH", "lemma_family", "Supply monotonicity, pairing, nesting, square, and level-shift Ackermann estimates.",
     "ack_pair_lt; ack_ack_lt_ack_max_add_two; ack_add_one_sq_lt_ack_add_three/four", "The growth inequality toolkit.", "required", "required", "critical", "split-required"),
    ("M0667-T-CONTRADICTION", "terminal", "Instantiate the domination bound for the diagonal at its witnessing level.",
     "exists m, forall n, ack n n < ack m n; specialize n = m", "The impossible strict self-inequality.", "required", "required", "high", 3),
    ("M0667-T-ASSEMBLE", "terminal", "Compose diagonalization, Nat encoding, domination, and contradiction into the root.",
     "Stage1Instances.THM_M_0667.root_of_domination", "Conditional kernel-checked root composition.", "required", "required", "critical", 7),
    ("M0667-X-SOURCE", "source_boundary", "Pinpoint the historical normalization and domination proof against primary editions and errata.",
     "Primary-source edition/theorem/page crosswalk", "Accepted human-source fidelity record.", "not_applicable", "required", "high", 10),
    ("M0667-X-FOUNDATION", "certificate", "Audit terminal bodies, axioms, transitive declarations, toolchain, and TCB.",
     "Trust and provenance certificate for pinned mathlib and local wrapper", "Accepted machine trust boundary.", "required", "not_applicable", "critical", 10),
    ("M0667-X-PROVENANCE", "certificate", "Trace the local wrapper to the unique pinned mathlib terminal body without duplicate credit.",
     "not_primrec2_ack -> not_primrec_ack_self -> not_nat_primrec_ack_self -> exists_lt_ack_of_nat_primrec", "Unique body and conclusion provenance.", "informational", "not_applicable", "critical", 9),
]


def obligation(spec):
    oid, kind, human, formal, output, machine, source, risk, _ = spec
    fp = "lean-expression-sha256:" + STATEMENT_HASH if oid == "M0667-ROOT" else "planned:v1:sha256:" + sha(formal + "\n" + output)
    exclusion = "human_source_boundary_only" if machine == "not_applicable" else ("provenance_overlay_no_independent_proof_credit" if machine == "informational" else None)
    body = "local:Stage1_Instances/THM-M-0667/ObligationTree.lean#root_of_domination" if oid == "M0667-T-ASSEMBLE" else None
    return {"obligation_id": oid, "statement_fingerprint": fp, "kind": kind, "root_relevant": True,
            "machine_eligibility": machine, "human_source_eligibility": source,
            "readable_eligibility": "required", "risk_class": risk,
            "exclusion_reason": exclusion, "terminal_proof_body_id": body}


obligations = [obligation(s) for s in SPECS]
ids = [o["obligation_id"] for o in obligations]
FIELDS = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility",
          "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
projection = [{k: o[k] for k in FIELDS} for o in obligations]
denominator = sha(json.dumps(projection, sort_keys=True, separators=(",", ":")))
registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": "S56-M-0667-OBLIGATION_TREE",
    "theorem_id": "THM-M-0667", "registry_version": 1, "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "Exact elaborated statement plus immutable anchor audit, frozen before proof-phase credit.",
    "frozen_against_statement_expression_sha256": STATEMENT_HASH,
    "frozen_against_anchor_audit_sha256": hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest(),
    "root_obligation_id": "M0667-ROOT", "denominator_sha256": denominator,
    "frozen_denominators": {
        "inventory": ids,
        "required_machine": [o["obligation_id"] for o in obligations if o["machine_eligibility"] == "required"],
        "required_human_source": [o["obligation_id"] for o in obligations if o["human_source_eligibility"] == "required"],
        "required_readable": ids,
        "informational_overlays": [o["obligation_id"] for o in obligations if o["machine_eligibility"] == "informational"]},
    "delta_policy": "Every correction, split, merge, exclusion, or eligibility change requires a new version and append-only ID delta.",
    "obligations": obligations}


def graph(name, edge_type, pairs):
    edges, incoming, outgoing = [], {}, {}
    for i, (a, b) in enumerate(pairs, 1):
        eid = f"E-{name.upper()}-{i:02d}"
        row = {"edge_id": eid, "from": a, "to": b, "type": edge_type}
        edges.append(row); outgoing.setdefault(a, []).append(eid); incoming.setdefault(b, []).append(eid)
    return {"edges": edges, "out": outgoing, "in": incoming}


def proof_graph(pairs):
    edges, incoming, outgoing = [], {}, {}
    for i, (a, b) in enumerate(pairs, 1):
        req, comp = f"E-PROOF-{i:02d}-REQ", f"E-PROOF-{i:02d}-COMPOSE"
        for row in ({"edge_id": req, "from": a, "to": b, "type": "proof_requires", "reciprocal_edge_id": comp},
                    {"edge_id": comp, "from": b, "to": a, "type": "composes", "reciprocal_edge_id": req}):
            edges.append(row); outgoing.setdefault(row["from"], []).append(row["edge_id"]); incoming.setdefault(row["to"], []).append(row["edge_id"])
    return {"edges": edges, "out": outgoing, "in": incoming}


proof_pairs = [("M0667-ROOT", "M0667-T-ASSEMBLE"), ("M0667-T-ASSEMBLE", "M0667-N-DIAGONAL"),
               ("M0667-T-ASSEMBLE", "M0667-T-NAT-BRIDGE"), ("M0667-T-ASSEMBLE", "M0667-N-DOMINATION"),
               ("M0667-T-ASSEMBLE", "M0667-T-CONTRADICTION"), ("M0667-N-DOMINATION", "M0667-B-CONSTRUCTORS"),
               ("M0667-B-CONSTRUCTORS", "M0667-L-BASE"), ("M0667-B-CONSTRUCTORS", "M0667-L-PAIR-COMP"),
               ("M0667-B-CONSTRUCTORS", "M0667-L-PREC"), ("M0667-B-CONSTRUCTORS", "M0667-L-GROWTH")]
proof_children = {b for _, b in proof_pairs}
graphs = {
    "proof": proof_graph(proof_pairs),
    "refinement": graph("refinement", "logical_decomposition", [("M0667-ROOT", x) for x in ids[1:] if x not in proof_children]),
    "provenance": graph("provenance", "provenance_of", [("M0667-X-PROVENANCE", "M0667-T-ASSEMBLE"), ("M0667-X-PROVENANCE", "M0667-N-DOMINATION")]),
    "evidence": graph("evidence", "evidence_for", [("M0667-S-ENCODING", "M0667-S-NORMALIZATION"), ("M0667-T-ASSEMBLE", "M0667-ROOT")]),
    "trust": graph("trust", "trusts", [("M0667-ROOT", "M0667-X-FOUNDATION"), ("M0667-N-DOMINATION", "M0667-X-FOUNDATION")]),
    "documentation": graph("documentation", "documents", [("M0667-X-SOURCE", "M0667-ROOT"), ("M0667-X-PROVENANCE", "M0667-ROOT")]),
    "workflow": graph("workflow", "workflow_depends_on", [("M0667-T-ASSEMBLE", "M0667-N-DOMINATION"), ("M0667-X-PROVENANCE", "M0667-T-ASSEMBLE"), ("M0667-X-FOUNDATION", "M0667-T-ASSEMBLE")])}


def node(spec):
    oid, kind, human, formal, output, machine, source, risk, budget = spec
    debt = "M0-P" if oid in {"M0667-S-NORMALIZATION", "M0667-S-ENCODING", "M0667-N-DIAGONAL", "M0667-T-NAT-BRIDGE", "M0667-T-CONTRADICTION", "M0667-T-ASSEMBLE"} else "M3"
    return {"node_id": "THM-" + oid, "obligation_id": oid, "kind": kind, "human_statement": human,
            "formal_target": formal, "output": output, "human_debt": "H1", "machine_debt": debt,
            "readability_debt": "R3", "evidence_ids": [],
            "source_crosswalk_id": "source_statement_crosswalk" if source == "required" else "not-applicable",
            "provenance_id": "anchor-audit:M0667-CAND-MATHLIB-NOT-PRIMREC2-ACK" if oid in {"M0667-ROOT", "M0667-N-DOMINATION", "M0667-X-PROVENANCE"} else "none",
            "foundation_profile": "lean4-dependent-type-theory/policy-audit-open",
            "tcb_profile": "lean-4.29.0-mathlib-8a178386/transitive-audit-open", "computation_record": "none",
            "step_budget": budget,
            "semantic_step_ledger": {"premises": f"Only typed proof children recorded for {oid}.", "inference": human,
                                     "output": output, "source_anchors": "source_statement_crosswalk" if source == "required" else "not-applicable",
                                     "outgoing_use": "Consumed only by recorded typed edges; no stronger conclusion is credited."},
            "public_readable_target": "Stage1_Instances/THM-M-0667/obligation-tree.md#" + oid.lower(),
            "validation_spec_id": "VAL-" + oid + "-PENDING",
            "status_boundary": "Frozen architecture only; open premises receive no root proof or theorem-completion credit.",
            "task_ids": ["S56-M-0667-OBLIGATION_TREE", "S56-M-0667-PROOF"],
            "owned_sources": ["Stage1_Instances/THM-M-0667/ObligationTree.lean#root_of_domination"] if oid == "M0667-T-ASSEMBLE" else [],
            "owner": "THM-M-0667 proof implementer", "reviewer": "independent Stage1 integration reviewer",
            "validity": "frozen-2026-07-12; review_due=before-proof-acceptance; invalidate_on=statement,registry,toolchain,source,body change; revocation=none"}


bundle = {"schema_version": "stage1-typed-graphs/1.0", "item_id": "S56-M-0667-OBLIGATION_TREE",
          "theorem_id": "THM-M-0667", "registry_denominator_sha256": denominator,
          "nodes": [node(s) for s in SPECS], "graphs": graphs,
          "closure_boundary": {"root_machine_debt": "M3", "theorem_complete": False,
                               "remaining_root_cut_set": ["M0667-N-DOMINATION", "M0667-X-FOUNDATION", "M0667-X-SOURCE"],
                               "conditional_composition": "Stage1Instances.THM_M_0667.root_of_domination"}}

(HERE / "obligation-registry.json").write_text(json.dumps(registry, ensure_ascii=True, indent=2) + "\n")
(HERE / "typed-graphs.json").write_text(json.dumps(bundle, ensure_ascii=True, indent=2) + "\n")
print(f"wrote {len(ids)} obligations; denominator sha256: {denominator}")
