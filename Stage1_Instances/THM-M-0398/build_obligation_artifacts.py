#!/usr/bin/env python3
"""Generate the frozen THM-M-0398 registry and typed graph bundle."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-0398-OBLIGATION_TREE"
THEOREM = "THM-M-0398"


def digest(value):
    raw = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


def planned(row):
    value = {key: row[key] for key in ("id", "kind", "claim", "target", "output")}
    return "planned:v1:sha256:" + digest(value)


rows = [
    dict(id="M0398-ROOT", kind="root", risk="critical",
         claim="For every irrational algebraic real alpha and epsilon > 0, the reduced rationals r satisfying |alpha-r| < den(r)^(-(2+epsilon)) form a finite set.",
         target="Stage1Instances.THMM0398.ThueSiegelRoth",
         output="The unchanged canonical Thue-Siegel-Roth proposition."),
    dict(id="M0398-S", kind="definition", risk="high",
         claim="Freeze the statement, rational representation, boundary cases, and logical profiles used by the root.",
         target="Statement/foundation interface for Stage1Instances.THMM0398.ThueSiegelRoth",
         output="An exact, reviewable interface for every later proof package."),
    dict(id="M0398-S1", kind="transport", risk="high", checked=True,
         claim="The named root expands to the quantified finite set of exceptional reduced rationals with real exponent 2+epsilon.",
         target="Stage1Instances.THMM0398.thueSiegelRoth_iff",
         output="Checked definitional expansion of the exact root."),
    dict(id="M0398-S2", kind="normalization", risk="normal", checked=True,
         claim="Rat.den is a strictly positive normalized denominator, so zero denominators and duplicate fraction representatives do not enter the root carrier.",
         target="Stage1Instances.THMM0398.denominator_pos",
         output="Positive-denominator and canonical-representative boundary."),
    dict(id="M0398-S3", kind="certificate", risk="high",
         claim="Fix the Lean foundation, axiom, noncomputable-proposition, and no-oracle policy for every future terminal body.",
         target="planned: exact axiom and TCB policy certificate for the terminal declaration closure",
         output="Accepted/disallowed trust boundary without mathematical proof credit."),
    dict(id="M0398-T", kind="bridge", risk="critical", checked=True,
         claim="A uniform positive-constant exceptional-set theorem specializes at C=1 to the exact canonical root.",
         target="Stage1Instances.THMM0398.root_of_finiteExceptionalWithConstant",
         output="The exact canonical root, conditional on M0398-L4."),
    dict(id="M0398-N1", kind="reduction", risk="high",
         claim="If an exceptional rational set for fixed alpha, epsilon, and C is infinite, extract distinct reduced rationals with strictly growing denominators and the same approximation inequality.",
         target="planned: Infinite exceptional set -> growing-denominator reduced rational sequence",
         output="A denominator-divergent sequence of exceptional approximants."),
    dict(id="M0398-C1", kind="construction", risk="critical", split=True,
         claim="Choose Roth parameters and construct a nonzero multivariate integer auxiliary polynomial with controlled multidegree, height, and high index at the algebraic diagonal.",
         target="planned: auxiliary polynomial existence with explicit degree/height/index invariants",
         output="An auxiliary polynomial and all size and vanishing invariants."),
    dict(id="M0398-C2", kind="core_lemma", risk="critical", split=True,
         claim="Apply the Roth index lemma to separated rational approximation points, preserving a positive index after the required differentiations and nonvanishing choice.",
         target="planned: multivariate Roth index/nonvanishing lemma",
         output="A derivative evaluation that is nonzero while retaining a quantitative index bound."),
    dict(id="M0398-L1", kind="lemma", risk="high",
         claim="Bound the selected auxiliary-polynomial derivative evaluation above using its index, coefficient height, and the exceptional approximation inequalities.",
         target="planned: analytic upper estimate for the selected derivative evaluation",
         output="An upper bound decreasing with the separated denominators."),
    dict(id="M0398-L2", kind="lemma", risk="critical",
         claim="After clearing reduced rational denominators, use algebraicity, conjugates, and the product formula to give a nonzero arithmetic lower bound for the same evaluation.",
         target="planned: denominator-clearing/product-formula lower estimate",
         output="A positive lower bound in the same height and denominator parameters."),
    dict(id="M0398-L3", kind="lemma", risk="high",
         claim="Choose the auxiliary degrees and a sufficiently separated subsequence so that the upper estimate is strictly smaller than the arithmetic lower estimate.",
         target="planned: parameter optimization and upper/lower contradiction",
         output="Contradiction to infinitude for each fixed positive constant C."),
    dict(id="M0398-L4", kind="terminal", risk="critical",
         claim="Recompose sequence extraction, auxiliary construction, index, and estimates into finiteness for every positive constant C.",
         target="Stage1Instances.THMM0398.FiniteExceptionalWithConstant",
         output="The exact premise consumed by M0398-T."),
    dict(id="M0398-X1", kind="terminal", risk="high", machine="not_applicable",
         claim="Pinpoint Roth's 1955 proof, hypotheses, conventions, errata, and source passages for every substantive proof node.",
         target="non-machine: reviewed node-specific primary-source crosswalk",
         output="Human-source coverage for the frozen mathematical route."),
    dict(id="M0398-X2", kind="certificate", risk="critical", machine="informational", human="not_applicable",
         claim="Audit the eventual terminal declaration, transitive proof-body provenance, axioms, imported artifacts, TCB, and reproducible validation receipts.",
         target="non-proof: release trust and provenance certificate",
         output="Release-gate trust classification, not a mathematical premise."),
]

ids = [row["id"] for row in rows]
obligations = []
nodes = []
for row in rows:
    machine = row.get("machine", "required")
    human = row.get("human", "required")
    fingerprint = (
        "lean-source-sha256:" + hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
        if row["id"] in {"M0398-ROOT", "M0398-S1"} else planned(row)
    )
    obligations.append({
        "obligation_id": row["id"], "statement_fingerprint": fingerprint,
        "kind": row["kind"], "root_relevant": True,
        "machine_eligibility": machine, "human_source_eligibility": human,
        "readable_eligibility": "required", "risk_class": row["risk"],
        "exclusion_reason": ({"not_applicable": "human_source_boundary_only",
                              "informational": "release_trust_overlay_no_proof_credit"}.get(machine)),
        "terminal_proof_body_id": ("local:Stage1_Instances/THM-M-0398/ObligationTree.lean#root_of_finiteExceptionalWithConstant"
                                   if row["id"] == "M0398-T" else None),
    })
    ledger = {
        "premises": "Use only the frozen incoming typed edges and the hypotheses stated here.",
        "inference": row["claim"], "output": row["output"],
        "outgoing_use": "Supply only this output to its declared parent or non-proof graph edge.",
    }
    nodes.append({
        "node_id": f"THM-M-0398-{row['id'].removeprefix('M0398-')}",
        "obligation_id": row["id"], "kind": row["kind"],
        "human_statement": row["claim"], "formal_target": row["target"], "output": row["output"],
        "human_debt": "H1", "machine_debt": "M0-L" if row.get("checked") else ("M3" if row["id"] == "M0398-ROOT" else "M4"),
        "readability_debt": "R4", "evidence_ids": [],
        "source_crosswalk_id": "roth-1955-node-map-pending" if human == "required" else "not-applicable",
        "provenance_id": "local-conditional-composition" if row["id"] == "M0398-T" else "none",
        "foundation_profile": "lean4-dependent-type-theory/policy-audit-pending",
        "tcb_profile": "lean-4.29.0+mathlib-8a178386/transitive-closure-pending",
        "computation_record": "none; no oracle or external computation planned",
        "step_budget": "split-required" if row.get("split") else 12,
        "semantic_step_ledger": ledger,
        "public_readable_target": f"Stage1_Instances/THM-M-0398/obligation-tree.md#{row['id'].lower()}",
        "validation_spec_id": f"VAL-{row['id']}",
        "status_boundary": "Architecture or conditional-interface record only; it does not close any unlisted premise or the theorem root.",
        "task_ids": [ITEM, "S56-M-0398-PROOF"], "owned_sources": [],
        "owner": "THM-M-0398 proof implementer", "reviewer": "independent Stage1 integration reviewer",
        "validity": "frozen-2026-07-12; review_due=before-proof-acceptance; invalidate_on=statement,registry,source-map,toolchain change; revocation=none",
    })

projection_fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant",
                     "machine_eligibility", "human_source_eligibility", "readable_eligibility",
                     "risk_class", "exclusion_reason", "terminal_proof_body_id")
denominator_hash = digest([{key: row[key] for key in projection_fields} for row in obligations])
registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_version": 1,
    "freeze_basis": "Exact Statement.lean plus the bounded anchor audit and the classical auxiliary-polynomial proof architecture; eligibility assigned before proof execution.",
    "frozen_against_statement_sha256": hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest(),
    "frozen_against_anchor_audit_sha256": hashlib.sha256((HERE / "anchor-audit.md").read_bytes()).hexdigest(),
    "root_obligation_id": "M0398-ROOT",
    "frozen_denominators": {
        "inventory": ids,
        "required_machine": [o["obligation_id"] for o in obligations if o["machine_eligibility"] == "required"],
        "required_human_source": [o["obligation_id"] for o in obligations if o["human_source_eligibility"] == "required"],
        "required_readable": ids,
        "informational_overlays": ["M0398-X2"],
    },
    "denominator_sha256": denominator_hash,
    "delta_policy": "Any target correction, split, merge, exclusion, or eligibility change requires registry version 2 with an append-only old/new ID delta.",
    "obligations": obligations,
}


def edge(edge_id, source, kind, target, reciprocal=None):
    value = {"edge_id": edge_id, "from": source, "type": kind, "to": target}
    if reciprocal:
        value["reciprocal_edge_id"] = reciprocal
    return value


requires = {
    "M0398-ROOT": ["M0398-T"],
    "M0398-L4": ["M0398-N1", "M0398-C1", "M0398-C2", "M0398-L1", "M0398-L2", "M0398-L3"],
}
proof = []
for parent, children in requires.items():
    for child in children:
        a, b = f"REQ-{parent}-{child}", f"CMP-{child}-{parent}"
        proof += [edge(a, parent, "proof_requires", child, b), edge(b, child, "composes", parent, a)]
proof += [edge("REQ-T-L4", "M0398-T", "proof_requires", "M0398-L4", "CMP-L4-T"),
          edge("CMP-L4-T", "M0398-L4", "composes", "M0398-T", "REQ-T-L4")]

graph_edges = {
    "proof": proof,
    "refinement": [edge("REF-ROOT-S", "M0398-ROOT", "logical_decomposition", "M0398-S")] +
                  [edge(f"REF-S-{x}", "M0398-S", "logical_decomposition", x) for x in ("M0398-S1", "M0398-S2", "M0398-S3")],
    "provenance": [edge("PROV-ROOT-S1", "M0398-ROOT", "provenance_of", "M0398-S1"),
                   edge("SOURCE-ROUTE-X1", "M0398-L4", "source_map", "M0398-X1")],
    "evidence": [edge("EVID-T-S1", "M0398-T", "evidence_for", "M0398-S1")],
    "trust": [edge("TRUST-ROOT-X2", "M0398-ROOT", "trusts", "M0398-X2"),
              edge("TRUST-T-S3", "M0398-T", "trusts", "M0398-S3")],
    "documentation": [edge("DOC-ROOT-S", "M0398-S", "documents", "M0398-ROOT"),
                      edge("DOC-L4-X1", "M0398-X1", "documents", "M0398-L4")],
    "workflow": [edge("FLOW-T-X1", "M0398-T", "workflow_depends_on", "M0398-X1"),
                 edge("FLOW-X2-T", "M0398-X2", "workflow_depends_on", "M0398-T")],
}
graphs = {}
for name, edges in graph_edges.items():
    incoming, outgoing = {}, {}
    for item in edges:
        outgoing.setdefault(item["from"], []).append(item["edge_id"])
        incoming.setdefault(item["to"], []).append(item["edge_id"])
    graphs[name] = {"edges": edges, "out": outgoing, "in": incoming}

bundle = {
    "schema_version": "stage1-typed-graphs/1.0", "item_id": ITEM, "theorem_id": THEOREM,
    "registry_denominator_sha256": denominator_hash, "root_node_id": "M0398-ROOT",
    "nodes": nodes, "graphs": graphs,
    "closure_boundary": {
        "closed_obligations": ["M0398-S1", "M0398-S2", "M0398-T"],
        "root_closed": False, "audit_complete": False, "theorem_complete": False,
        "remaining_root_cut_set": ["M0398-L4"],
        "reason": "M0398-T is only conditional; the uniform constant-factor Roth engine M0398-L4 has no proof body.",
    },
}

recipes = []
for row in rows:
    lean_checked = row["id"] in {"M0398-S1", "M0398-S2", "M0398-T"}
    recipes.append({
        "recipe_id": f"VAL-{row['id']}", "obligation_id": row["id"],
        "command": ("cd Stage1_Instances/THM-M-0398 && "
                    "LEAN_PATH=$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH) "
                    "/home/sansha-2/.elan/toolchains/leanprover--lean4---v4.29.0/bin/lean -o Statement.olean Statement.lean && "
                    "LEAN_PATH=.:$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH) "
                    "/home/sansha-2/.elan/toolchains/leanprover--lean4---v4.29.0/bin/lean ObligationTree.lean && "
                    "rm Statement.olean") if lean_checked else "python3 Stage1_Instances/THM-M-0398/check_obligation_tree.py",
        "expected_exit": 0, "network_policy": "denied",
        "acceptance": "elaborates checked interface" if lean_checked else "structural architecture validation only; no proof closure",
    })
specs = {"schema_version": "stage1-validation-specs/1.0", "item_id": ITEM,
         "theorem_id": THEOREM, "recipes": recipes}

for name, value in (("obligation-registry.json", registry), ("typed-graphs.json", bundle),
                    ("validation-specs.json", specs)):
    (HERE / name).write_text(json.dumps(value, indent=2) + "\n")
print(f"wrote {len(rows)} obligations and {sum(len(x) for x in graph_edges.values())} typed edges")
