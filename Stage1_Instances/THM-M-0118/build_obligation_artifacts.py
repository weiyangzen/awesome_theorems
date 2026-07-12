#!/usr/bin/env python3
"""Build deterministic typed graphs and validation recipes for THM-M-0118."""

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
REGISTRY_PATH = HERE / "obligation-registry.json"
registry = json.loads(REGISTRY_PATH.read_text())

fields = ("obligation_id", "statement_fingerprint", "kind", "root_relevant",
          "machine_eligibility", "human_source_eligibility", "readable_eligibility",
          "risk_class", "exclusion_reason", "terminal_proof_body_id")
projection = [{key: row[key] for key in fields} for row in registry["obligations"]]
digest = hashlib.sha256(json.dumps(projection, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
registry["denominator_sha256"] = digest
REGISTRY_PATH.write_text(json.dumps(registry, indent=2, ensure_ascii=True) + "\n")

statements = {
    "M0118-ROOT": ("The exact Nakano-positive vector-bundle target frozen in Statement.lean.", "Stage1Instances.THMM0118.NakanoVanishingTarget", "Vanishing in every degree p+q>n."),
    "M0118-S-INTERFACES": ("Transport the abstract data to native compact Kahler, holomorphic Hermitian bundle, curvature, and coefficient-cohomology interfaces.", "planned checked native-interface equivalence", "A native analytic instance matching every abstract field."),
    "M0118-S-VANISHING": ("Identify Subsingleton of an additive cohomology group with equality to the zero group.", "Stage1Instances.THMM0118.NakanoVanishingData.Vanishes", "The frozen conclusion has the standard zero-cohomology meaning."),
    "M0118-G-HERMITIAN": ("Construct the Hermitian metric, Chern connection, curvature operator, and L2 pairing on bundle-valued forms.", "planned analytic construction", "Curvature and adjoint operators on a complete compact analytic setting."),
    "M0118-G-DOLBEAULT": ("Construct the bundle-valued Dolbeault complex and its degree-(p,q) cohomology.", "planned Dolbeault complex", "A complex whose cohomology transports to D.Cohomology p q."),
    "M0118-A-HODGE": ("Prove the compact bundle-valued Dolbeault Hodge theorem.", "planned Hodge isomorphism", "Cohomology classes have unique harmonic representatives."),
    "M0118-A-BOCHNER": ("Prove the Bochner-Kodaira-Nakano identity for E-valued (p,q)-forms.", "planned Bochner-Kodaira-Nakano identity", "The Laplacian norm splits with the curvature commutator term."),
    "M0118-A-CURVATURE": ("Use Nakano positivity and p+q>n to obtain strict positivity of the curvature term on the relevant harmonic forms.", "planned curvature positivity estimate", "A zero-norm conclusion for any harmonic representative."),
    "M0118-A-HARMONIC-ZERO": ("Combine the identity and positivity estimate to prove every relevant harmonic form is zero.", "planned harmonic vanishing lemma", "The degree-(p,q) harmonic space is subsingleton."),
    "M0118-T-COHOMOLOGY": ("Transport harmonic vanishing through Hodge/Dolbeault comparison to coefficient-cohomology vanishing.", "planned checked cohomology transport", "Subsingleton (D.Cohomology p q)."),
    "M0118-T-ASSEMBLE": ("Compose the analytic output with the exact ordered binders of the root.", "Stage1Instances.THMM0118.nakanoVanishingTarget_of_analyticPackage", "The exact NakanoVanishingTarget."),
    "M0118-X-SOURCE": ("Pin a primary theorem/page and map every analytic hypothesis and proof node.", "human primary-source crosswalk", "H0-eligible source evidence after independent review."),
    "M0118-X-PROVENANCE": ("Resolve every terminal declaration and body without duplicate wrapper credit.", "planned terminal-body provenance report", "A unique-body and dependency-closure ledger."),
    "M0118-X-TRUST": ("Audit axioms, transitive declarations, TCB, computation, and no-oracle policy.", "planned trust certificate", "An accepted foundation and trust boundary.")
}

nodes = []
for row in registry["obligations"]:
    oid = row["obligation_id"]
    human, formal, output = statements[oid]
    checked = oid in {"M0118-S-VANISHING", "M0118-T-ASSEMBLE"}
    nodes.append({
        "node_id": "THM-M-0118-" + oid.removeprefix("M0118-"), "obligation_id": oid,
        "kind": row["kind"], "human_statement": human, "formal_target": formal, "output": output,
        "human_debt": "H2", "machine_debt": "M0-L" if checked else ("M3" if oid == "M0118-ROOT" else "M4"),
        "readability_debt": "R3", "evidence_ids": [],
        "source_crosswalk_id": "primary-source-node-map-pending" if row["human_source_eligibility"] == "required" else "not-applicable",
        "provenance_id": "local-transparent-body" if checked else "none",
        "foundation_profile": "lean4-kernel; analytic/classical policy audit pending",
        "tcb_profile": "lean-4.29.0+mathlib-8a178386; transitive closure pending",
        "computation_record": "none; computation or oracle output cannot close this node",
        "step_budget": 40 if checked else 100,
        "semantic_step_ledger": {"premises": "Only declared incoming proof requirements and the frozen formal context.", "inference": human, "output": output, "outgoing_use": "Only a declared typed parent or support edge may consume this output."},
        "public_readable_target": "Stage1_Instances/THM-M-0118/obligation-tree.md#" + oid.lower(),
        "validation_spec_id": "VAL-" + oid, "status_boundary": "Architecture only unless a named local declaration is marked M0-L; no open analytic premise receives proof credit.",
        "task_ids": ["S56-M-0118-OBLIGATION_TREE", "S56-M-0118-PROOF"], "owned_sources": [],
        "owner": "THM-M-0118 proof lane", "reviewer": "independent Stage1 integration lane",
        "validity": {"validated_at": "2026-07-12" if checked else None, "review_due": "before proof acceptance", "invalidation_inputs": ["statement", "registry", "source map", "toolchain"], "revocation_state": "provisional" if checked else "open"}
    })

graphs = {name: {"edges": [], "out": {row["obligation_id"]: [] for row in registry["obligations"]}, "in": {row["obligation_id"]: [] for row in registry["obligations"]}} for name in ("proof", "refinement", "provenance", "evidence", "trust", "documentation", "workflow")}

def edge(graph, eid, typ, source, target, reciprocal=None):
    row = {"edge_id": eid, "type": typ, "from": source, "to": target}
    if reciprocal:
        row["reciprocal_edge_id"] = reciprocal
    graphs[graph]["edges"].append(row)
    graphs[graph]["out"][source].append(eid)
    graphs[graph]["in"][target].append(eid)

requirements = [
    ("M0118-ROOT", "M0118-T-ASSEMBLE"), ("M0118-T-ASSEMBLE", "M0118-S-INTERFACES"),
    ("M0118-T-ASSEMBLE", "M0118-S-VANISHING"), ("M0118-T-ASSEMBLE", "M0118-T-COHOMOLOGY"),
    ("M0118-T-COHOMOLOGY", "M0118-G-DOLBEAULT"), ("M0118-T-COHOMOLOGY", "M0118-A-HODGE"),
    ("M0118-T-COHOMOLOGY", "M0118-A-HARMONIC-ZERO"), ("M0118-A-HARMONIC-ZERO", "M0118-G-HERMITIAN"),
    ("M0118-A-HARMONIC-ZERO", "M0118-A-BOCHNER"), ("M0118-A-HARMONIC-ZERO", "M0118-A-CURVATURE")]
for index, (parent, child) in enumerate(requirements, 1):
    req, comp = f"P{index:02d}-REQ", f"P{index:02d}-COMP"
    edge("proof", req, "proof_requires", parent, child, comp)
    edge("proof", comp, "composes", child, parent, req)

for index, oid in enumerate(("M0118-G-HERMITIAN", "M0118-G-DOLBEAULT", "M0118-A-HODGE", "M0118-A-BOCHNER", "M0118-A-CURVATURE", "M0118-A-HARMONIC-ZERO", "M0118-T-COHOMOLOGY"), 1):
    edge("refinement", f"R{index:02d}", "logical_decomposition", "M0118-ROOT", oid)
    edge("provenance", f"V{index:02d}", "provenance_of", "M0118-X-PROVENANCE", oid)
    edge("evidence", f"E{index:02d}", "source_map", "M0118-X-SOURCE", oid)
    edge("documentation", f"D{index:02d}", "documents", oid, "M0118-ROOT")
for index, oid in enumerate(("M0118-ROOT", "M0118-T-ASSEMBLE", "M0118-T-COHOMOLOGY", "M0118-A-HARMONIC-ZERO"), 1):
    edge("trust", f"T{index:02d}", "trusts", "M0118-X-TRUST", oid)
for index, (parent, child) in enumerate(requirements, 1):
    edge("workflow", f"W{index:02d}", "workflow_depends_on", parent, child)

bundle = {"schema_version":"stage1-typed-graphs/1.0", "item_id":registry["item_id"], "theorem_id":registry["theorem_id"],
          "registry_id":"THM-M-0118-OBLIGATIONS-v1", "registry_denominator_sha256":digest,
          "root_node_id":"M0118-ROOT", "edge_direction":"Proof requirements run parent to child; composes edges run child to parent.",
          "nodes":nodes, "graphs":graphs,
          "closure_boundary":{"root_closed":False,"theorem_complete":False,"remaining_root_cut_set":["M0118-T-COHOMOLOGY"],"machine_debt":"M3","reason":"No native analytic interfaces or checked Dolbeault-Hodge/Nakano proof package exists in the pinned closure."}}
(HERE / "typed-graphs.json").write_text(json.dumps(bundle, indent=2, ensure_ascii=True) + "\n")

recipes = []
for row in registry["obligations"]:
    oid = row["obligation_id"]
    recipes.append({"recipe_id":"VAL-"+oid,"cwd":".","argv":["python3","Stage1_Instances/THM-M-0118/check_obligation_tree.py"],"env_allowlist":{},"timeout_seconds":30,"network_policy":"denied","expected_exit":0,"expected_outputs":[{"path_or_stream":"stdout","semantic_hash_policy":"contains PASS THM-M-0118 obligation tree"}],"covered_obligation_ids":[oid],"covered_declarations":["Stage1Instances.THMM0118.nakanoVanishingTarget_of_analyticPackage"] if oid == "M0118-T-ASSEMBLE" else []})
(HERE / "validation-specs.json").write_text(json.dumps({"schema_version":"stage1-validation-specs/1.0","item_id":registry["item_id"],"theorem_id":registry["theorem_id"],"recipes":recipes}, indent=2) + "\n")
print(digest)
