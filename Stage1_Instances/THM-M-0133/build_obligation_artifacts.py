#!/usr/bin/env python3
"""Generate the frozen THM-M-0133 obligation registry and typed graphs."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-0133-OBLIGATION_TREE"
TID = "THM-M-0133"
PREFIX = "M0133"
ROOT_FP = "lean-expression-sha256:8e0d406e9e5ba4504c1930352fde324a02df4a30cbfd75f796b9a3d2627113c1"

# id, kind, parent, human statement, formal target, output, risk
SPECS = [
    ("ROOT", "root", None, "For n >= 3, no nonzero natural a,b,c satisfy a^n+b^n=c^n.", "Stage1Instances.THM_M_0133.WilesFermatLastTheoremTarget", "The exact frozen Fermat Last Theorem target.", "critical"),
    ("S", "definition", "ROOT", "Freeze the statement, domains, boundary cases, transports, and logic policy.", "Statement and foundation package for the canonical target", "An unambiguous exact root target.", "high"),
    ("S-DEF", "definition", "S", "Expand FermatLastTheorem and its fixed-exponent predicates over Nat.", "FermatLastTheorem; FermatLastTheoremFor", "The fixed-exponent predicate and its universal closure.", "normal"),
    ("S-DOM", "definition", "S", "Fix n,a,b,c in Nat with n >= 3 and all values nonzero.", "n a b c : Nat; 3 <= n; a != 0; b != 0; c != 0", "The exact domain and ordered binder context.", "normal"),
    ("S-BOUNDARY", "branch", "S", "Exclude zero values and exponents 0, 1, and 2; retain n=3 as the first case.", "3 <= n and a != 0 and b != 0 and c != 0", "The complete degenerate-case boundary.", "normal"),
    ("S-TRANSPORT", "transport", "S", "Transport between the frozen nonzero Nat form and the positive-natural source form.", "WilesFermatLastTheoremTarget <-> PositiveNaturalSourceShape", "Both checked transport directions.", "normal"),
    ("S-FOUNDATION", "certificate", "S", "Audit classical logic, quotient, extensionality, and axiom use for admitted bodies.", "Axiom and foundation policy certificate", "An accepted logical boundary with no placeholder axioms.", "high"),
    ("N", "normalization", "ROOT", "Reduce arbitrary exponents n >= 3 to exponent four or an odd-prime exponent.", "FermatLastTheorem.of_odd_primes", "A checked exhaustive exponent reduction and root assembly.", "critical"),
    ("N-ARITH", "core_lemma", "N", "Every n >= 3 is handled through a factor 4 or an odd prime divisor with exponent descent.", "Exponent reduction lemmas used by FermatLastTheorem.of_odd_primes", "The exhaustive arithmetic reduction.", "high"),
    ("N-DESCENT", "transport", "N", "A solution at a composite exponent induces one at the selected divisor exponent.", "Power-factor transport for FermatLastTheoremFor", "Composite-to-prime/four counterexample transport.", "high"),
    ("B", "branch", "ROOT", "Split the normalized proof into exponent four and arbitrary odd-prime branches.", "FermatLastTheoremFor 4 and forall odd prime p, FermatLastTheoremFor p", "Exhaustive branch conclusions supplied to root assembly.", "critical"),
    ("B-FOUR", "terminal", "B", "Rule out nonzero natural solutions at exponent four.", "FermatLastTheoremFor 4", "The exponent-four branch.", "high"),
    ("B-ODD", "branch", "B", "For each odd prime p, rule out nonzero natural solutions at exponent p.", "forall p, Nat.Prime p -> Odd p -> FermatLastTheoremFor p", "The all-odd-prime premise of root assembly.", "critical"),
    ("B-RECOMPOSE", "bridge", "B", "Combine the exponent-four theorem and all odd-prime cases into the exact root.", "FermatLastTheorem.of_odd_primes", "The conditional root theorem with all branch premises consumed.", "critical"),
    ("C", "construction", "B-ODD", "From a primitive odd-prime FLT counterexample construct its Frey elliptic curve.", "Planned Frey-curve construction from a hypothetical FermatLastTheoremFor p counterexample", "A semistable Frey curve with the required discriminant and conductor data.", "critical"),
    ("C-PRIMITIVE", "normalization", "C", "Normalize a counterexample to pairwise-coprime primitive data with controlled parity.", "Planned primitive counterexample structure", "Primitive input for the Frey construction.", "high"),
    ("C-CURVE", "construction", "C", "Define the Frey curve and prove its Weierstrass model is well formed.", "Planned elliptic curve over Rat", "The constructed elliptic curve over Q.", "critical"),
    ("C-INVARIANTS", "core_lemma", "C", "Compute discriminant, conductor, reduction, and semistability invariants of the Frey curve.", "Planned Frey invariant package", "Semistability and conductor facts needed by modularity and lowering.", "critical"),
    ("C-REP", "construction", "C", "Construct the mod-p Galois representation and prove irreducibility and ramification bounds.", "Planned Frey mod-p representation package", "The representation consumed by level lowering.", "critical"),
    ("L", "core_lemma", "B-ODD", "Derive the odd-prime contradiction via semistable modularity and level lowering.", "Planned Wiles--Taylor-Wiles plus Frey--Ribet implication", "FermatLastTheoremFor p for every odd prime p.", "critical"),
    ("L-MOD", "core_lemma", "L", "Every semistable elliptic curve over Q is modular.", "Wiles 1995 Theorem 0.4, formal signature planned", "Modularity of the Frey curve.", "critical"),
    ("L-RESIDUAL", "core_lemma", "L-MOD", "Establish residual modularity and the hypotheses for modularity lifting.", "Planned residual modularity theorem", "A modular residual representation.", "critical"),
    ("L-DEFORM", "construction", "L-MOD", "Define global and local deformation problems and their universal rings.", "Planned deformation-ring package", "The deformation rings and comparison map.", "critical"),
    ("L-HECKE", "construction", "L-MOD", "Define the relevant modular forms and localized Hecke algebras.", "Planned Hecke-algebra package", "The Hecke algebra receiving the deformation map.", "critical"),
    ("L-TW", "construction", "L-MOD", "Choose Taylor-Wiles auxiliary primes and compatible finite-level systems.", "Planned Taylor-Wiles prime system", "Auxiliary levels satisfying patching hypotheses.", "critical"),
    ("L-PATCH", "core_lemma", "L-MOD", "Patch deformation modules and control depth, dimension, and freeness.", "Planned Taylor-Wiles patching theorem", "The numerical criterion needed for R=T.", "critical"),
    ("L-RT", "core_lemma", "L-MOD", "Prove the minimal deformation ring equals the localized Hecke algebra.", "Planned minimal R=T theorem", "Minimal modularity lifting.", "critical"),
    ("L-LIFT", "core_lemma", "L-MOD", "Pass from minimal to non-minimal semistable representations.", "Planned non-minimal modularity lifting theorem", "Semistable modularity over Q.", "critical"),
    ("L-LOWER", "core_lemma", "L", "Apply Ribet level lowering to the Frey representation.", "Planned level-lowering theorem with Frey hypotheses", "A weight-two level-two modular form forced by a counterexample.", "critical"),
    ("L-EMPTY", "computation", "L", "Show the required weight-two level-two cusp-form space is zero.", "Planned certified dimension computation for S_2(Gamma_0(2))", "Nonexistence of the modular form forced by level lowering.", "high"),
    ("L-CONTRA", "terminal", "L", "Contradict the forced modular form with the level-two nonexistence result.", "Planned contradiction theorem", "The arbitrary odd-prime FLT conclusion.", "critical"),
    ("X", "bridge", "ROOT", "Freeze imported theorem bodies, source revisions, automation, computation, and trust boundaries.", "Pinned anchor and trust inventory", "Auditable external boundaries without proof credit inflation.", "high"),
    ("X-ASSEMBLY", "bridge", "X", "Pin the conditional mathlib root assembly theorem.", "FermatLastTheorem.of_odd_primes", "A candidate conditional proof body, not unconditional FLT.", "high"),
    ("X-FOUR", "terminal", "X", "Pin mathlib's exponent-four proof body.", "fermatLastTheoremFour : FermatLastTheoremFor 4", "A candidate fixed-exponent body.", "normal"),
    ("X-REGULAR", "terminal", "X", "Pin flt-regular's theorem for regular prime exponents.", "flt_regular", "A restricted odd-prime family only.", "high"),
    ("X-IMPERIAL", "bridge", "X", "Record the external exact-root candidate whose body transitively contains a proof gap.", "ImperialCollegeLondon/FLT@8884a744...: FLT.Proof.flt", "Rejected provenance boundary with no machine credit.", "critical"),
    ("X-TCB", "certificate", "X", "Audit kernel, elaborator, dependency pins, axioms, and checker reproducibility.", "Lean 4.29.0 transitive trust closure", "The release trust record.", "critical"),
    ("T", "terminal", "ROOT", "Transport the all-branch conclusion back to the exact frozen target.", "Conditional composition certificate in ObligationTree.lean", "The canonical target, provided every root-critical premise closes.", "critical"),
]


def oid(short):
    return f"{PREFIX}-{short}"


def digest(value):
    raw = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


children = {short: [] for short, *_ in SPECS}
for short, _kind, parent, *_rest in SPECS:
    if parent:
        children[parent].append(short)

obligations = []
nodes = []
for short, kind, parent, statement, formal, output, risk in SPECS:
    overlay = short.startswith("X")
    fp = ROOT_FP if short == "ROOT" else "planned:v1:sha256:" + digest({
        "id": oid(short), "kind": kind, "statement": statement, "formal_target": formal,
        "context_parent": oid(parent) if parent else None, "output": output,
    })
    body = {
        "X-ASSEMBLY": "mathlib@8a178386:FermatLastTheorem.of_odd_primes",
        "X-FOUR": "mathlib@8a178386:fermatLastTheoremFour",
        "X-REGULAR": "flt-regular@56161b6e:flt_regular",
    }.get(short)
    obligations.append({
        "obligation_id": oid(short), "statement_fingerprint": fp, "kind": kind,
        "root_relevant": not overlay,
        "machine_eligibility": "informational" if overlay else "required",
        "human_source_eligibility": "not_applicable" if overlay else "required",
        "readable_eligibility": "required", "risk_class": risk,
        "exclusion_reason": "typed_provenance_or_trust_overlay" if overlay else None,
        "terminal_proof_body_id": body,
    })
    leaf = not children[short]
    ledger = [
        {"premises": f"Exact context and hypotheses of {oid(short)}", "inference": "establish the named mathematical or formal transition", "output": output, "outgoing_use": oid(parent) if parent else "canonical theorem decision"},
        {"premises": "node output plus its declared typed edge", "inference": "check exact child-to-parent composition without strengthening", "output": f"validated handoff of {oid(short)}", "outgoing_use": oid(parent) if parent else "THEOREM-Z gate"},
    ]
    nodes.append({
        "node_id": f"{TID}-{short}", "obligation_id": oid(short), "kind": kind,
        "human_statement": statement, "formal_target": formal, "output": output,
        "human_debt": "H1", "machine_debt": "M2" if short == "ROOT" else "M4",
        "readability_debt": "R4", "evidence_ids": [],
        "source_crosswalk_id": "anchor-audit-root-boundary" if short == "ROOT" else "pending-pinpoint-crosswalk",
        "provenance_id": body or "none",
        "foundation_profile": "lean4-dependent-type-theory/policy-audit-pending",
        "tcb_profile": "lean-4.29.0/transitive-closure-pending", "computation_record": "none",
        "step_budget": len(ledger) if leaf else "split-required", "semantic_step_ledger": ledger,
        "public_readable_target": f"Stage1_Instances/THM-M-0133/obligation-tree.md#{oid(short).lower()}",
        "validation_spec_id": f"VAL-{oid(short)}-PENDING",
        "status_boundary": "Architecture only; no proof closure or source/readability acceptance is credited.",
        "task_ids": [ITEM, "S56-M-0133-PROOF"], "owned_sources": [],
        "owner": "THM-M-0133 proof implementer", "reviewer": "independent Stage1 integration reviewer",
        "validity": "frozen-2026-07-12; review_due=before-proof-acceptance; invalidate_on=statement,registry,edge,source,toolchain change; revocation=none",
    })

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility",
          "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
projection = [{key: row[key] for key in fields} for row in obligations]
ids = [row["obligation_id"] for row in obligations]
registry = {
    "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": TID,
    "registry_version": 1,
    "freeze_basis": "Exact statement and immutable anchor audit, followed by the mandatory S/N/B/C/L/X/T architecture; eligibility was assigned before proof closure was inspected.",
    "root_obligation_id": oid("ROOT"),
    "frozen_denominators": {
        "inventory": ids,
        "required_machine": [r["obligation_id"] for r in obligations if r["machine_eligibility"] == "required"],
        "required_human_source": [r["obligation_id"] for r in obligations if r["human_source_eligibility"] == "required"],
        "required_readable": ids,
        "informational_overlays": [r["obligation_id"] for r in obligations if r["machine_eligibility"] == "informational"],
    },
    "denominator_sha256": digest(projection),
    "delta_policy": "Any split, merge, eligibility change, exclusion, or target change requires registry version 2 plus an append-only old/new ID delta.",
    "obligations": obligations,
}

edges = {name: [] for name in ("proof", "refinement", "provenance", "evidence", "trust", "documentation", "workflow")}
for short, _kind, parent, *_ in SPECS:
    if not parent or short.startswith("X"):
        continue
    graph = "refinement" if parent == "S" else "proof"
    etype = "logical_decomposition" if graph == "refinement" else "proof_requires"
    edges[graph].append({"edge_id": f"{graph.upper()}-{parent}-{short}", "from": oid(parent), "type": etype, "to": oid(short)})
edges["trust"] = [{"edge_id": f"TRUST-ROOT-{short}", "from": oid("ROOT"), "type": "trusts", "to": oid(short)} for short in ("X", "X-TCB")]
edges["provenance"] = [
    {"edge_id": "PROV-N-ASSEMBLY", "from": oid("N"), "type": "provenance_of", "to": oid("X-ASSEMBLY")},
    {"edge_id": "PROV-B4-FOUR", "from": oid("B-FOUR"), "type": "provenance_of", "to": oid("X-FOUR")},
    {"edge_id": "PROV-ODD-REGULAR", "from": oid("B-ODD"), "type": "source_map", "to": oid("X-REGULAR")},
    {"edge_id": "PROV-ROOT-IMPERIAL", "from": oid("ROOT"), "type": "provenance_of", "to": oid("X-IMPERIAL")},
]
edges["evidence"] = [{"edge_id": "EVID-ROOT-X", "from": oid("ROOT"), "type": "evidence_for", "to": oid("X")}]
edges["documentation"] = [{"edge_id": "DOC-ROOT-T", "from": oid("ROOT"), "type": "documents", "to": oid("T")}]
edges["workflow"] = [{"edge_id": "FLOW-TREE-PROOF", "from": oid("ROOT"), "type": "workflow_depends_on", "to": oid("T")}]

graphs = {}
for name, rows in edges.items():
    outgoing, incoming = {}, {}
    for row in rows:
        outgoing.setdefault(row["from"], []).append(row["edge_id"])
        incoming.setdefault(row["to"], []).append(row["edge_id"])
    graphs[name] = {"edges": rows, "out": outgoing, "in": incoming}

bundle = {
    "schema_version": "stage1-typed-graphs/1.0", "item_id": ITEM, "theorem_id": TID,
    "nodes": nodes, "graphs": graphs,
    "closure_boundary": {"closed_obligations": [], "root_machine_debt": "M2",
                         "remaining_root_cut_set": [oid("L-MOD"), oid("L-LOWER")],
                         "composition_certificates_checked": ["Stage1Instances.THM_M_0133.ObligationTree.root_compose"],
                         "theorem_complete": False},
}

(HERE / "obligation-registry.json").write_text(json.dumps(registry, indent=2) + "\n")
(HERE / "typed-graphs.json").write_text(json.dumps(bundle, indent=2) + "\n")
print(f"wrote {len(obligations)} obligations and {sum(len(v) for v in edges.values())} typed edges")
