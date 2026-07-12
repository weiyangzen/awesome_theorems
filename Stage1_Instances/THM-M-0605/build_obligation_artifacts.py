#!/usr/bin/env python3
"""Build the frozen THM-M-0605 obligation registry and typed graph bundle."""

import hashlib
import json
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEM = "S56-M-0605-OBLIGATION_TREE"


def sha(path):
    return hashlib.sha256((HERE / path).read_bytes()).hexdigest()


def planned(obligation_id, statement):
    payload = f"THM-M-0605:v1:{obligation_id}:{statement}".encode()
    return "planned:v1:sha256:" + hashlib.sha256(payload).hexdigest()


specs = [
    ("M0605-ROOT", "root", "The exact proposition ExoticSevenSphereExists.", "The canonical proposition.", "critical", "M4", 8),
    ("M0605-S-DEFS", "definition", "Freeze the smooth seven-manifold package, standard embedded sphere, homeomorphism, and diffeomorphism notions.", "The exact definitions used by every proof node.", "high", "M0-L", 20),
    ("M0605-S-DOMAIN", "definition", "Preserve Type 0, real dimension seven, the Fin 7 model, the Fin 8 ambient standard sphere, and smoothness omega.", "The exact universe, dimension, and typeclass context.", "high", "M0-L", 18),
    ("M0605-S-BOUNDARY", "branch", "Audit the dimension-seven and unit-radius boundary choices and reject the zero-dimensional mutation.", "A complete boundary and degeneracy policy.", "normal", "M4", 24),
    ("M0605-S-TRANSPORT", "transport", "Transport the source's manifold homeomorphic to S7 formulation to the packaged canonical target in both checked directions.", "An exact directional transport into the canonical proposition.", "high", "M4", 35),
    ("M0605-S-FOUNDATION", "certificate", "Audit classical principles, quotients, manifold infrastructure, transitive axioms, and the Lean/mathlib trust boundary.", "An accepted foundation and TCB profile.", "critical", "M4", 45),
    ("M0605-C-BUNDLE", "construction", "Select the precise Milnor oriented 3-sphere bundle over the 4-sphere and construct it from its clutching data.", "A specific smooth sphere bundle with the characteristic data needed below.", "critical", "M4", 95),
    ("M0605-C-TOTAL", "construction", "Construct the bundle total space and its smooth seven-manifold structure.", "A value M : SmoothSevenManifold backed by the selected total space.", "critical", "M4", 90),
    ("M0605-L-HOMOTOPY", "core_lemma", "Compute the selected total space's connectivity and homology and obtain the required homotopy-seven-sphere conclusion.", "The exact homotopy-sphere hypotheses required by the topological bridge.", "critical", "M4", 95),
    ("M0605-X-TOPO-PC", "bridge", "Apply the dimension-seven topological generalized Poincare boundary to identify the homotopy sphere with the standard topological sphere.", "Nonempty (M.Carrier ≃ₜ StandardSevenSphere).", "critical", "M4", 70),
    ("M0605-L-BOUNDING", "construction", "Construct the associated bounding eight-manifold and orient it compatibly with the selected sphere bundle.", "A bounding manifold on which the smooth obstruction can be evaluated.", "critical", "M4", 90),
    ("M0605-L-OBSTRUCTION", "computation", "Compute the characteristic-number/signature obstruction of the bounding manifold with all normalization and orientation conventions fixed.", "A certified nonstandard value of the Milnor smooth obstruction.", "critical", "M4", 100),
    ("M0605-L-STANDARD", "core_lemma", "Prove the corresponding obstruction vanishes for the standard smooth seven-sphere and is preserved by a diffeomorphism.", "Any diffeomorphism to the standard sphere forces the standard obstruction value.", "critical", "M4", 90),
    ("M0605-L-NONDIFF", "terminal", "Derive a contradiction from a putative diffeomorphism using the incompatible obstruction values.", "IsEmpty (M.Carrier ≃ₘ StandardSevenSphere) in the canonical models.", "critical", "M4", 45),
    ("M0605-T-WITNESS", "terminal", "Combine the constructed smooth manifold, topological equivalence, and non-diffeomorphism certificate.", "The three exact inputs consumed by terminal assembly.", "critical", "M4", 20),
    ("M0605-T-ASSEMBLE", "transport", "Apply exoticSevenSphereExists_of_witness to the three explicit child conclusions.", "The exact canonical proposition, conditionally on the open witness package.", "high", "M0-L", 4),
    ("M0605-X-SOURCE", "terminal", "Pinpoint every construction and obstruction inference in Milnor 1956, including assumptions, conventions, and errata review.", "An H0-eligible primary-source crosswalk.", "high", "not_applicable", 80),
    ("M0605-X-PROVENANCE", "certificate", "Track every eventual wrapper to its distinct terminal proof body without duplicate credit.", "A complete terminal-body provenance map.", "high", "informational", 45),
    ("M0605-X-TRUST", "certificate", "Bind kernel, toolchain, dependency, computation, and replay evidence for release.", "Release-gate trust evidence.", "critical", "informational", 50),
]

obligations = []
nodes = []
for oid, kind, statement, output, risk, machine, budget in specs:
    is_overlay = oid in {"M0605-X-SOURCE", "M0605-X-PROVENANCE", "M0605-X-TRUST"}
    machine_eligibility = "informational" if machine == "informational" else ("not_applicable" if machine == "not_applicable" else "required")
    source_eligibility = "required" if oid in {"M0605-ROOT", "M0605-C-BUNDLE", "M0605-C-TOTAL", "M0605-L-HOMOTOPY", "M0605-X-TOPO-PC", "M0605-L-BOUNDING", "M0605-L-OBSTRUCTION", "M0605-L-STANDARD", "M0605-L-NONDIFF", "M0605-X-SOURCE"} else "not_applicable"
    obligations.append({
        "obligation_id": oid,
        "statement_fingerprint": "lean-expression-sha256:b45c5a871dc9b5862356b1fd2540c8d770d8b4488230005303cc6b41f7b33469" if oid == "M0605-ROOT" else planned(oid, statement),
        "kind": kind, "root_relevant": True,
        "machine_eligibility": machine_eligibility,
        "human_source_eligibility": source_eligibility,
        "readable_eligibility": "required", "risk_class": risk,
        "exclusion_reason": None,
        "terminal_proof_body_id": "local:ObligationTree.lean#exoticSevenSphereExists_of_witness" if oid == "M0605-T-ASSEMBLE" else None,
    })
    nodes.append({
        "node_id": "THM-M-0605-" + oid.removeprefix("M0605-"), "obligation_id": oid,
        "kind": kind, "human_statement": statement,
        "formal_target": "Stage1.THM_M_0605.ExoticSevenSphereExists" if oid == "M0605-ROOT" else ("Stage1.THM_M_0605.exoticSevenSphereExists_of_witness" if oid == "M0605-T-ASSEMBLE" else "planned exact signature: " + output),
        "output": output, "human_debt": "H1", "machine_debt": machine,
        "readability_debt": "R3", "evidence_ids": [],
        "source_crosswalk_id": "source-statement-crosswalk.md" if source_eligibility == "required" else "not-applicable",
        "provenance_id": "local-composition-body" if oid == "M0605-T-ASSEMBLE" else "none",
        "foundation_profile": "lean4-mathlib-classical/policy-audit-pending",
        "tcb_profile": "lean-4.29.0+mathlib-8a178386/transitive-closure-pending",
        "computation_record": "planned characteristic-number certificate; no result credited" if oid == "M0605-L-OBSTRUCTION" else "none; no oracle or experiment is credited",
        "step_budget": budget,
        "semantic_step_ledger": {"premises": "Exact conclusions of incoming proof_requires edges.", "inference": statement, "output": output, "outgoing_use": "Only through typed edges in typed-graphs.json."},
        "public_readable_target": f"Stage1_Instances/THM-M-0605/obligation-tree.md#{oid.lower()}",
        "validation_spec_id": "VAL-" + oid,
        "status_boundary": "Architecture or conditional interface only; no unresolved geometric or topological claim is asserted." if not is_overlay else "Release/source overlay only; it cannot close a proof premise.",
        "task_ids": [ITEM, "S56-M-0605-PROOF"],
        "owned_sources": ["Stage1_Instances/THM-M-0605/ObligationTree.lean"] if oid == "M0605-T-ASSEMBLE" else [],
        "owner": "THM-M-0605 proof lane", "reviewer": "independent Stage1 integration lane",
        "validity": {"validated_at": str(date.today()) if oid == "M0605-T-ASSEMBLE" else None, "review_due": "before proof acceptance", "invalidation_inputs": ["Statement.lean", "anchor-audit.json", "obligation-registry.json", "toolchain"], "revocation_state": "provisional" if oid == "M0605-T-ASSEMBLE" else "open"},
    })

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant", "machine_eligibility", "human_source_eligibility", "readable_eligibility", "risk_class", "exclusion_reason", "terminal_proof_body_id")
projection = [{k: row[k] for k in fields} for row in obligations]
denom = hashlib.sha256(json.dumps(projection, sort_keys=True, separators=(",", ":")).encode()).hexdigest()

registry = {
    "schema_version": "stage1-obligation-registry/1.0", "registry_id": "THM-M-0605-OBLIGATIONS-v1",
    "item_id": ITEM, "theorem_id": "THM-M-0605", "registry_version": 1,
    "frozen_at": "2026-07-12T00:00:00+08:00",
    "freeze_basis": "Exact statement and the source-faithful Milnor bundle/obstruction architecture; eligibility is independent of discovered machine closure.",
    "frozen_against_statement_sha256": sha("Statement.lean"), "frozen_against_anchor_audit_sha256": sha("anchor-audit.json"),
    "root_obligation_id": "M0605-ROOT", "denominator_sha256": denom,
    "frozen_denominators": {
        "inventory": [r["obligation_id"] for r in obligations],
        "required_machine": [r["obligation_id"] for r in obligations if r["machine_eligibility"] == "required"],
        "required_human_source": [r["obligation_id"] for r in obligations if r["human_source_eligibility"] == "required"],
        "required_readable": [r["obligation_id"] for r in obligations if r["readable_eligibility"] == "required"],
        "informational_overlays": ["M0605-X-PROVENANCE", "M0605-X-TRUST"],
    },
    "delta_policy": "Any correction, split, merge, exclusion, or eligibility change creates a new registry version with an append-only old/new ID delta.",
    "obligations": obligations,
}

proof_pairs = [
    ("M0605-ROOT", "M0605-T-ASSEMBLE"), ("M0605-ROOT", "M0605-S-DEFS"), ("M0605-ROOT", "M0605-S-DOMAIN"), ("M0605-ROOT", "M0605-S-BOUNDARY"), ("M0605-ROOT", "M0605-S-TRANSPORT"),
    ("M0605-T-ASSEMBLE", "M0605-T-WITNESS"), ("M0605-T-WITNESS", "M0605-C-TOTAL"), ("M0605-T-WITNESS", "M0605-X-TOPO-PC"), ("M0605-T-WITNESS", "M0605-L-NONDIFF"),
    ("M0605-C-TOTAL", "M0605-C-BUNDLE"), ("M0605-X-TOPO-PC", "M0605-L-HOMOTOPY"), ("M0605-L-HOMOTOPY", "M0605-C-BUNDLE"),
    ("M0605-L-NONDIFF", "M0605-L-OBSTRUCTION"), ("M0605-L-NONDIFF", "M0605-L-STANDARD"), ("M0605-L-OBSTRUCTION", "M0605-L-BOUNDING"), ("M0605-L-BOUNDING", "M0605-C-BUNDLE"),
]

graph_names = ("proof", "refinement", "provenance", "evidence", "trust", "documentation", "workflow")
graphs = {name: {"edges": [], "out": {r["obligation_id"]: [] for r in obligations}, "in": {r["obligation_id"]: [] for r in obligations}} for name in graph_names}
def edge(graph, frm, to, typ, reciprocal=None):
    eid = f"{graph.upper()}-{len(graphs[graph]['edges'])+1:03d}"
    row = {"edge_id": eid, "from": frm, "to": to, "type": typ}
    if reciprocal: row["reciprocal_edge_id"] = reciprocal
    graphs[graph]["edges"].append(row); graphs[graph]["out"][frm].append(eid); graphs[graph]["in"][to].append(eid)
    return eid
for parent, child in proof_pairs:
    e1 = edge("proof", parent, child, "proof_requires")
    e2 = edge("proof", child, parent, "composes", e1)
    graphs["proof"]["edges"][-2]["reciprocal_edge_id"] = e2
for child in ("M0605-C-BUNDLE", "M0605-C-TOTAL", "M0605-L-HOMOTOPY", "M0605-L-BOUNDING", "M0605-L-OBSTRUCTION", "M0605-L-STANDARD", "M0605-L-NONDIFF"):
    edge("provenance", child, "M0605-X-SOURCE", "source_map")
    edge("provenance", child, "M0605-X-PROVENANCE", "provenance_of")
for oid, *_ in specs:
    edge("documentation", oid, oid, "documents")
    edge("workflow", oid, "M0605-ROOT", "workflow_depends_on") if oid != "M0605-ROOT" else None
for oid in ("M0605-ROOT", "M0605-S-FOUNDATION", "M0605-L-OBSTRUCTION", "M0605-T-ASSEMBLE"):
    edge("trust", oid, "M0605-X-TRUST", "trusts")
for child in ("M0605-L-HOMOTOPY", "M0605-L-OBSTRUCTION", "M0605-L-STANDARD"):
    edge("refinement", "M0605-T-WITNESS", child, "logical_decomposition")

bundle = {
    "schema_version": "stage1-typed-graph-bundle/1.0", "item_id": ITEM, "theorem_id": "THM-M-0605",
    "registry_id": registry["registry_id"], "registry_denominator_sha256": denom,
    "nodes": nodes, "graphs": graphs,
    "closure_boundary": {"root_closed": False, "root_machine_debt": "M4", "theorem_complete": False, "remaining_root_cut_set": ["M0605-T-WITNESS"], "checked_composition": "Stage1.THM_M_0605.exoticSevenSphereExists_of_witness", "boundary": "The checked terminal assembly consumes, but does not construct, the open witness and its two certificates."},
}

recipes = {"schema_version": "stage1-validation-specs/1.0", "item_id": ITEM, "recipes": [{"validation_spec_id": "VAL-" + oid, "cwd": "Formalizations/Lean", "argv": ["lake", "env", "lean", "../../Stage1_Instances/THM-M-0605/ObligationTree.lean"], "env": {}, "timeout_seconds": 120, "network": "forbidden", "covered_ids": [oid], "status": "executable_composition_check" if oid == "M0605-T-ASSEMBLE" else "planned_node_check"} for oid, *_ in specs]}

for name, obj in (("obligation-registry.json", registry), ("typed-graphs.json", bundle), ("validation-specs.json", recipes)):
    (HERE / name).write_text(json.dumps(obj, indent=2, ensure_ascii=True) + "\n")
print(f"generated {len(obligations)} obligations; denominator {denom}; typed edges {sum(len(g['edges']) for g in graphs.values())}")
