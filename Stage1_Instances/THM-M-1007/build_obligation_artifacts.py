#!/usr/bin/env python3
"""Build the frozen THM-M-1007 obligation registry and typed graphs."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-1007-OBLIGATION_TREE"
THEOREM = "THM-M-1007"
PREFIX = "M1007-"

# short ID, kind, risk, statement, formal target, output, H/M/R, budget
SPECS = [
    ("ROOT", "root", "critical", "For every independent measurable real sequence and fixed c > 0, almost-sure series convergence is equivalent to the three fixed-cutoff conditions.", "Stage1Instances.THM_M_1007.KolmogorovThreeSeriesTarget", "The exact frozen biconditional.", "H1", "M3", "R3", 8),
    ("S-INTERFACE", "definition", "critical", "Preserve the probability space, ordered binders, measurability, mutual independence, positive cutoff, and natural-order convergence predicates.", "Statement.lean:KolmogorovThreeSeriesTarget", "The exact binder and hypothesis interface.", "H1", "M3", "R3", 18),
    ("S-BOUNDARY", "branch", "high", "Retain values at abs X = c in the truncation and exclude them from the strict large-jump event.", "truncate_eq_self_of_abs_le; truncate_eq_zero_of_lt_abs", "An exhaustive inclusive-cutoff policy.", "H1", "M3", "R3", 12),
    ("S-FOUNDATION", "certificate", "high", "Fix the Lean kernel, classical measure-theory, integration, variance, and pinned dependency trust boundary.", "Lean 4.29.0; mathlib 8a178386", "A versioned foundation and TCB decision.", "H1", "M3", "R4", 16),
    ("N-TRUNCATE", "normalization", "critical", "Replace X_n by Y_n = X_n on abs X_n <= c and zero outside, without changing the cutoff convention.", "Stage1Instances.THM_M_1007.truncate", "The bounded truncated sequence Y.", "H1", "M3", "R3", 14),
    ("C-TRUNC-PROPS", "construction", "critical", "Prove each Y_n measurable, integrable, square-integrable, bounded by c, and mutually independent.", "planned: measurable/integrable/MemLp and iIndepFun truncation package", "All analytic and independence invariants needed by the bounded-series engine.", "H1", "M3", "R3", 52),
    ("C-EVENT-INDEP", "construction", "high", "Derive mutual independence and measurability of the large-jump events {c < abs X_n}.", "planned: iIndepSets events derived from iIndepFun", "The independence premise for converse Borel-Cantelli.", "H1", "M3", "R3", 28),
    ("B-LARGE-JUMP-NEC", "bridge", "critical", "From almost-sure convergence of sum X_n, prove summability of P(c < abs X_n) using X_n -> 0 and converse Borel-Cantelli.", "planned: converse Borel-Cantelli bridge", "The first three-series condition in the necessity direction.", "H1", "M3", "R4", 72),
    ("B-LARGE-JUMP-SUFF", "bridge", "critical", "From summability of P(c < abs X_n), prove that large jumps occur only finitely often almost surely by first Borel-Cantelli.", "MeasureTheory.ae_eventually_notMem plus event-series transport", "Almost-sure eventual equality of X and Y.", "H1", "M3", "R4", 46),
    ("T-EVENTUAL", "transport", "critical", "Show that two real series whose terms are eventually equal have equivalent convergence, pointwise and almost everywhere.", "planned: finite-prefix/eventual-equality series convergence transport", "Transfer of almost-sure convergence between X and Y.", "H1", "M3", "R3", 34),
    ("N-CENTER", "normalization", "critical", "Decompose Y_n into the deterministic mean integral Y_n plus the centered variable Z_n and preserve independence and variance.", "planned: Y_n = (Y_n - E Y_n) + E Y_n", "A centered independent bounded sequence and deterministic mean series.", "H1", "M3", "R4", 54),
    ("L-BOUNDED-NEC", "core_lemma", "critical", "For independent uniformly bounded Y_n, almost-sure convergence implies convergence of sum E[Y_n] and summability of Var(Y_n).", "planned: necessity half of bounded independent-series criterion", "The second and third conditions from convergence of the truncated series.", "H1", "M3", "R4", 100),
    ("L-BOUNDED-SUFF", "core_lemma", "critical", "For independent uniformly bounded Y_n, convergence of sum E[Y_n] and summability of Var(Y_n) imply almost-sure convergence of sum Y_n.", "planned: Kolmogorov convergence criterion for centered bounded variables", "Almost-sure convergence of the truncated series.", "H1", "M3", "R4", 100),
    ("T-NECESSITY", "terminal", "critical", "Compose convergence, large-jump necessity, eventual truncation, and bounded-series necessity into all three right-hand conditions.", "Stage1Instances.THM_M_1007.ObligationTree.Necessity", "The forward implication of the exact root.", "H1", "M3", "R3", 24),
    ("T-SUFFICIENCY", "terminal", "critical", "Compose Borel-Cantelli, the bounded-series sufficiency theorem, and eventual equality into almost-sure convergence of sum X_n.", "Stage1Instances.THM_M_1007.ObligationTree.Sufficiency", "The reverse implication of the exact root.", "H1", "M3", "R3", 22),
    ("T-ASSEMBLE", "terminal", "critical", "Consume exactly the necessity and sufficiency implications to assemble the canonical biconditional.", "Stage1Instances.THM_M_1007.ObligationTree.root_of_directions", "The exact root, conditional on both directed obligations.", "H1", "M3", "R3", 6),
    ("X-SOURCE", "terminal", "high", "Pinpoint and independently review a primary proof with assumption, cutoff, and errata mapping to every material node.", "primary-source page and proof crosswalk remains open", "Human-source coverage for the architecture.", "H1", "M5", "R4", 36),
    ("X-PROVENANCE", "certificate", "high", "Record terminal proof bodies for Borel-Cantelli and every future bounded-series bridge, deduplicating wrappers and transports.", "mathlib 8a178386 plus future local bodies", "Body-level provenance for all machine-critical leaves.", "H1", "M3", "R4", 28),
    ("X-TCB", "certificate", "high", "Audit transitive Lean, mathlib, foundation, imported artifacts, axioms, and executable trust closure.", "Lean 4.29.0; mathlib 8a178386; release audit open", "Release-grade trust inventory.", "H1", "M3", "R4", 24),
]


def oid(short):
    return PREFIX + short


statement = json.loads((HERE / "statement.json").read_text())
expression_hash = statement["canonical_formal_target"]["elaborated_expression_sha256"]
overlays = {"X-SOURCE", "X-PROVENANCE", "X-TCB"}
no_human = {"S-INTERFACE", "S-BOUNDARY", "S-FOUNDATION", "X-PROVENANCE", "X-TCB"}
body_ids = {
    "B-LARGE-JUMP-SUFF": "mathlib:8a178386:MeasureTheory.ae_eventually_notMem",
    "T-ASSEMBLE": "repo:Stage1Instances.THM_M_1007.ObligationTree.root_of_directions",
}
rows = []
for short, kind, risk, human, formal, output, hd, md, rd, budget in SPECS:
    fingerprint = ("lean-expression-sha256:" + expression_hash if short == "ROOT" else
                   "planned:v1:sha256:" + hashlib.sha256((human + "\n" + formal).encode()).hexdigest())
    rows.append({
        "obligation_id": oid(short), "statement_fingerprint": fingerprint, "kind": kind,
        "root_relevant": short not in overlays,
        "machine_eligibility": "informational" if short in overlays else "required",
        "human_source_eligibility": "not_applicable" if short in no_human else "required",
        "readable_eligibility": "required", "risk_class": risk,
        "exclusion_reason": "non-proof assurance overlay" if short in overlays else None,
        "terminal_proof_body_id": body_ids.get(short),
    })

FIELDS = ("obligation_id", "statement_fingerprint", "kind", "root_relevant",
          "machine_eligibility", "human_source_eligibility", "readable_eligibility",
          "risk_class", "exclusion_reason", "terminal_proof_body_id")
projection = [{key: row[key] for key in FIELDS} for row in rows]
denominator = hashlib.sha256(json.dumps(projection, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
ids = [row["obligation_id"] for row in rows]
registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM,
    "theorem_id": THEOREM, "registry_version": 1,
    "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "The elaborated exact statement and completed anchor inventory fix the S/N/B/C/L/X/T architecture before proof-phase closure credit. No candidate closure status was used to exclude an obligation.",
    "frozen_against_statement_sha256": hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest(),
    "frozen_against_anchor_audit_sha256": hashlib.sha256((HERE / "anchor_audit.json").read_bytes()).hexdigest(),
    "root_obligation_id": oid("ROOT"), "denominator_sha256": denominator,
    "frozen_denominators": {
        "inventory": ids,
        "required_machine": [r["obligation_id"] for r in rows if r["machine_eligibility"] == "required"],
        "required_human_source": [r["obligation_id"] for r in rows if r["human_source_eligibility"] == "required"],
        "required_readable": ids,
        "informational_overlays": [r["obligation_id"] for r in rows if r["machine_eligibility"] == "informational"],
    },
    "delta_policy": "Any correction, statement or anchor change, split, merge, exclusion, eligibility change, or risk change requires registry v2 and an append-only old/new ID delta.",
    "obligations": rows,
}

nodes = []
for spec, row in zip(SPECS, rows):
    short, kind, risk, human, formal, output, hd, md, rd, budget = spec
    nodes.append({
        "node_id": "THM-M-1007-" + short, "obligation_id": oid(short), "kind": kind,
        "human_statement": human, "formal_target": formal, "output": output,
        "human_debt": hd, "machine_debt": md, "readability_debt": rd,
        "evidence_ids": [],
        "source_crosswalk_id": "SRC-M1007-PRIMARY-OPEN" if row["human_source_eligibility"] == "required" else "not-applicable",
        "provenance_id": "PROV-M1007-BOREL-CANTELLI" if short == "B-LARGE-JUMP-SUFF" else "none",
        "foundation_profile": "Lean 4 kernel plus pinned mathlib classical measure-theory foundations",
        "tcb_profile": "Lean 4.29.0 (98dc76e); mathlib 8a178386; transitive release audit open",
        "computation_record": "none", "step_budget": budget,
        "semantic_step_ledger": {
            "premises": ["typed proof/refinement children"], "inference": formal,
            "output": output, "outgoing_use": "typed parent edge or root result",
        },
        "public_readable_target": "Stage1_Instances/THM-M-1007/obligation-tree.md#" + short.lower(),
        "validation_spec_id": "VAL-M1007-" + short,
        "status_boundary": "Architecture only; no proof closure or acceptance is credited by this phase.",
        "task_ids": [ITEM, "S56-M-1007-PROOF"],
        "owned_sources": ["Stage1_Instances/THM-M-1007/obligation-registry.json", "Stage1_Instances/THM-M-1007/typed-graphs.json"],
        "owner": "Stage1 rev-5.6 execution worker", "reviewer": "independent integration lane",
        "validity": {"validated_at": "2026-07-12", "review_due": "before master acceptance", "invalidation_inputs": ["statement", "anchor audit", "registry", "toolchain", "mathlib revision", "proof-body provenance"], "revocation_state": "not-accepted"},
    })


def graph(edges):
    outgoing, incoming = {}, {}
    for edge in edges:
        outgoing.setdefault(edge["from"], []).append(edge["edge_id"])
        incoming.setdefault(edge["to"], []).append(edge["edge_id"])
    return {"edges": edges, "out": outgoing, "in": incoming}


proof_pairs = [
    ("ROOT", "T-ASSEMBLE"), ("T-ASSEMBLE", "T-NECESSITY"), ("T-ASSEMBLE", "T-SUFFICIENCY"),
    ("T-NECESSITY", "B-LARGE-JUMP-NEC"), ("T-NECESSITY", "T-EVENTUAL"),
    ("T-NECESSITY", "C-TRUNC-PROPS"), ("T-NECESSITY", "C-EVENT-INDEP"),
    ("T-NECESSITY", "L-BOUNDED-NEC"), ("T-SUFFICIENCY", "B-LARGE-JUMP-SUFF"),
    ("T-SUFFICIENCY", "T-EVENTUAL"), ("T-SUFFICIENCY", "C-TRUNC-PROPS"),
    ("T-SUFFICIENCY", "L-BOUNDED-SUFF"), ("L-BOUNDED-NEC", "N-CENTER"),
    ("L-BOUNDED-SUFF", "N-CENTER"), ("C-TRUNC-PROPS", "N-TRUNCATE"),
    ("C-EVENT-INDEP", "N-TRUNCATE"),
]
proof_edges = []
for parent, child in proof_pairs:
    forward, reverse = f"PROOF-{parent}-{child}", f"COMPOSE-{child}-{parent}"
    proof_edges.extend([
        {"edge_id": forward, "from": oid(parent), "type": "proof_requires", "to": oid(child), "reciprocal_edge_id": reverse},
        {"edge_id": reverse, "from": oid(child), "type": "composes", "to": oid(parent), "reciprocal_edge_id": forward},
    ])
refinement_pairs = [
    ("ROOT", "S-INTERFACE"), ("S-INTERFACE", "S-BOUNDARY"),
    ("S-INTERFACE", "S-FOUNDATION"), ("ROOT", "N-TRUNCATE"),
    ("N-TRUNCATE", "C-TRUNC-PROPS"), ("N-TRUNCATE", "C-EVENT-INDEP"),
    ("N-TRUNCATE", "N-CENTER"),
]
graphs = {
    "proof": graph(proof_edges),
    "refinement": graph([{"edge_id": f"REFINE-{a}-{b}", "from": oid(a), "type": "logical_decomposition", "to": oid(b)} for a, b in refinement_pairs]),
    "provenance": graph([{"edge_id": f"PROV-{s}", "from": oid("X-PROVENANCE"), "type": "provenance_of", "to": oid(s)} for s in ("B-LARGE-JUMP-NEC", "B-LARGE-JUMP-SUFF", "L-BOUNDED-NEC", "L-BOUNDED-SUFF")]),
    "evidence": graph([{"edge_id": "EVID-ROOT-PROVENANCE", "from": oid("X-PROVENANCE"), "type": "evidence_for", "to": oid("ROOT")}]),
    "trust": graph([{"edge_id": "TRUST-ROOT-TCB", "from": oid("ROOT"), "type": "trusts", "to": oid("X-TCB")}]),
    "documentation": graph([{"edge_id": f"DOC-{s}", "from": oid("X-SOURCE"), "type": "documents", "to": oid(s)} for s in ("ROOT", "B-LARGE-JUMP-NEC", "B-LARGE-JUMP-SUFF", "L-BOUNDED-NEC", "L-BOUNDED-SUFF")]),
    "workflow": graph([
        {"edge_id": "FLOW-ASSEMBLE-DIRECTIONS", "from": oid("T-ASSEMBLE"), "type": "workflow_depends_on", "to": oid("T-NECESSITY")},
        {"edge_id": "FLOW-SUFF-BOUNDED", "from": oid("T-SUFFICIENCY"), "type": "workflow_depends_on", "to": oid("L-BOUNDED-SUFF")},
        {"edge_id": "FLOW-NEC-BOUNDED", "from": oid("T-NECESSITY"), "type": "workflow_depends_on", "to": oid("L-BOUNDED-NEC")},
        {"edge_id": "FLOW-PROVENANCE-PROOF", "from": oid("X-PROVENANCE"), "type": "workflow_depends_on", "to": oid("T-ASSEMBLE")},
    ]),
}
cut_set = [oid(s) for s in ("C-TRUNC-PROPS", "C-EVENT-INDEP", "B-LARGE-JUMP-NEC", "B-LARGE-JUMP-SUFF", "T-EVENTUAL", "L-BOUNDED-NEC", "L-BOUNDED-SUFF")]
bundle = {
    "schema_version": "stage1-typed-graphs/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_denominator_sha256": denominator, "nodes": nodes, "graphs": graphs,
    "closure_boundary": {
        "closed_obligations": [], "root_closed": False, "root_machine_debt": "M3",
        "remaining_root_cut_set": cut_set,
        "composition_certificates_checked": ["Stage1Instances.THM_M_1007.ObligationTree.root_of_directions"],
        "audit_complete": False, "theorem_complete": False,
        "reason": "The exact iff composition is checked only from two explicit implication premises; all mathematical leaves remain open for the proof phase.",
    },
}
recipes = [{
    "recipe_id": "VAL-M1007-" + spec[0], "cwd": "Formalizations/Lean",
    "argv": ["lake", "env", "lean", "../../Stage1_Instances/THM-M-1007/ObligationTree.lean"],
    "env": {}, "timeout_seconds": 120, "network": "forbidden", "covered_ids": [oid(spec[0])],
} for spec in SPECS]
validation = {"schema_version": "stage1-validation-specs/1.0", "item_id": ITEM, "theorem_id": THEOREM, "recipes": recipes}

for name, value in (("obligation-registry.json", registry), ("typed-graphs.json", bundle), ("validation-specs.json", validation)):
    (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n")

lines = ["# THM-M-1007 frozen obligation architecture", "", "Registry version 1 freezes the exact fixed-cutoff proof architecture before any proof-phase closure credit. Every node has a stable obligation ID and a substantive-step budget at most 100.", ""]
for node in nodes:
    short = node["obligation_id"].removeprefix(PREFIX)
    lines += [f"## {short.lower()}", "", f"**Claim:** {node['human_statement']}", "", f"**Role and output:** {node['output']}", "", f"**Formal map:** `{node['formal_target']}`", "", f"**Ledger and boundary:** Inputs are the typed proof/refinement children; the planned inference is `{node['formal_target']}`; its exact output feeds the typed parent edge. Budget: {node['step_budget']} substantive steps. No proof closure is credited here.", "", f"**Status:** `[{node['human_debt']}, {node['machine_debt']}, {node['readability_debt']}]`; source, machine, readable-review, and release gates remain as recorded in the structured node.", ""]
lines += ["## closure-boundary", "", "`root_of_directions` kernel-checks only the final iff assembly. The root remains open at `M3`; no obligation is marked closed. The proof-phase cut set is the truncation-invariant package, event independence, both Borel-Cantelli branches, eventual-series transport, and both bounded independent-series directions. Primary-source, provenance, trust, readable-review, hermetic, and independent-validation gates also remain open.", ""]
(HERE / "obligation-tree.md").write_text("\n".join(lines))
print(f"wrote {len(rows)} obligations and {sum(len(g['edges']) for g in graphs.values())} typed edges")
print(f"registry denominator sha256: {denominator}")
