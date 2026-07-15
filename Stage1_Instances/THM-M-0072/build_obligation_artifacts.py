#!/usr/bin/env python3
"""Build the frozen THM-M-0072 obligation registry and typed graph bundle."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
THEOREM_ID = "THM-M-0072"
ITEM_ID = "S56-M-0072-OBLIGATION_TREE"
PREFIX = "M0072"
FROZEN_AT = "2026-07-15T16:00:00+08:00"
ROOT_EXPRESSION = "c8a89538bd8b492ba31ce5d516a0f8fefef70a550e1d2fe74e39a4cba7849051"

FIELDS = (
    "obligation_id", "statement_fingerprint", "kind", "root_relevant",
    "machine_eligibility", "human_source_eligibility", "readable_eligibility",
    "risk_class", "exclusion_reason", "terminal_proof_body_id",
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def architecture_hash(oid: str, statement: str) -> str:
    material = f"THM-M-0072-obligation-v1\n{oid}\n{statement}".encode()
    return "planned-signature-v1:sha256:" + hashlib.sha256(material).hexdigest()


ROWS = [
    ("ROOT", "root", "Exact printed Thompson transfer lemma.", "critical", None),
    ("S-TARGET", "definition", "Preserve the exact canonical binders and conclusion.", "critical", None),
    ("S-DOMAIN", "definition", "Finite even-order group, no index-two subgroup, Sylow 2-subgroup, maximal subgroup, and involution context.", "high", None),
    ("S-BOUNDARY", "branch", "Split involutions already in M from those outside M.", "high", "repo:Statement.lean#insideMaximal_hasConjugate"),
    ("S-TRANSPORT", "transport", "Relate the printed universal target to the outside-maximal target.", "high", "repo:Statement.lean#thompsonTransferLemmaTarget_iff_outsideMaximalTarget"),
    ("S-FOUNDATION", "certificate", "Freeze the Lean foundation, TCB, and noncomputational policy.", "critical", None),
    ("N-OUTSIDE", "reduction", "Reduce the nontrivial proof to an involution u outside M.", "critical", None),
    ("B-MEMBERSHIP", "branch", "Exhaust the cases u in M and u outside M.", "high", "repo:ObligationTree.lean#root_of_assembly"),
    ("T-INSIDE", "terminal", "Produce the inside-M conjugate by self-conjugacy.", "normal", "repo:ObligationTree.lean#insideMaximalConclusion"),
    ("C-NORMAL", "construction", "Show a maximal subgroup of the finite 2-group S is normal.", "critical", None),
    ("L-INDEX-TWO", "core_lemma", "Show the maximal proper subgroup M has index two in S.", "critical", None),
    ("C-QUOTIENT", "construction", "Construct the quotient group S/M and its nontrivial coset.", "critical", None),
    ("C-TRANSFER", "construction", "Construct the transfer homomorphism from G into S/M.", "critical", "mathlib:8a178386#MonoidHom.transfer"),
    ("L-SYLOW-ODD", "core_lemma", "Establish that the Sylow index |G:S| is odd.", "high", "mathlib:8a178386#Sylow.not_dvd_index"),
    ("C-COSET-ACTION", "construction", "Model the action of the involution on the cosets of S in G.", "critical", None),
    ("L-FIXED-PARITY", "core_lemma", "Deduce that the number of fixed cosets is odd.", "critical", None),
    ("L-TRANSFER-FORMULA", "bridge", "Express transfer at u as the product over fixed coset representatives.", "critical", "mathlib:8a178386#MonoidHom.transfer_eq_prod_quotient_orbitRel_zpowers_quot"),
    ("L-FACTOR-DICHOTOMY", "core_lemma", "Identify a fixed-coset factor with the coset of a G-conjugate of u.", "critical", None),
    ("L-ODD-PRODUCT", "core_lemma", "If every conjugate avoids M, the odd product is the nontrivial coset.", "critical", None),
    ("L-NOINDEX-TRANSFER", "core_lemma", "No index-two subgroup forces every homomorphism G to S/M to be trivial.", "critical", None),
    ("B-CONTRADICTION", "branch", "Contradict triviality with the nontrivial transfer value.", "critical", None),
    ("T-OUTSIDE", "terminal", "Produce a G-conjugate of the outside involution in M.", "critical", None),
    ("T-ASSEMBLE", "terminal", "Merge the outside and inside branches into the universal target.", "critical", "repo:ObligationTree.lean#root_of_assembly"),
    ("X-SOURCE", "terminal", "Map every proof transition to Thompson 1968 Lemma 5.38(a)(i).", "high", None),
    ("X-PROVENANCE", "certificate", "Track wrapper, candidate, import, and terminal-body provenance.", "critical", None),
    ("X-TRUST", "certificate", "Track foundation, axiom, dependency, and TCB closure.", "critical", None),
    ("X-READABLE", "terminal", "Own the public readable reconstruction and independent R0 review.", "high", None),
    ("X-WORKFLOW", "terminal", "Bind obligations to the authoritative task workflow and receipts.", "critical", None),
]


def build() -> tuple[dict, dict, dict]:
    statement_hash = sha256(HERE / "Statement.lean")
    anchor_hash = sha256(HERE / "anchor-audit.json")
    execution_dag_path = ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json"
    execution_dag = json.loads(execution_dag_path.read_text())
    authoritative_tasks = [
        item for item in execution_dag["items"] if item["theorem_id"] == THEOREM_ID
    ]

    statement_overlays = {"S-TARGET", "S-DOMAIN", "S-BOUNDARY", "S-TRANSPORT"}
    governance = {"X-PROVENANCE", "X-TRUST", "X-READABLE", "X-WORKFLOW"}
    no_human = statement_overlays | {"S-FOUNDATION"} | governance
    obligations = []
    nodes = []
    readable_path = f"Stage1_Instances/{THEOREM_ID}/obligation-tree.md"
    for suffix, kind, statement, risk, body in ROWS:
        oid = f"{PREFIX}-{suffix}"
        exact = suffix in {"ROOT", "S-TARGET"}
        informational = suffix in statement_overlays or suffix in governance or suffix == "X-SOURCE"
        exclusion = "typed_overlay_or_assurance_boundary_no_duplicate_machine_credit" if informational else None
        fingerprint = (
            "lean-expression-sha256:" + ROOT_EXPRESSION if exact else architecture_hash(oid, statement)
        )
        obligations.append({
            "obligation_id": oid,
            "statement_fingerprint": fingerprint,
            "kind": kind,
            "root_relevant": True,
            "machine_eligibility": "informational" if informational else "required",
            "human_source_eligibility": "not_applicable" if suffix in no_human else "required",
            "readable_eligibility": "required",
            "risk_class": risk,
            "exclusion_reason": exclusion,
            "terminal_proof_body_id": body,
        })
        formal_target = {
            "ROOT": "Stage1Instances.THM_M_0072.ThompsonTransferLemmaTarget",
            "S-TARGET": "Stage1Instances.THM_M_0072.ThompsonTransferLemmaTarget",
            "S-BOUNDARY": "Stage1Instances.THM_M_0072.ObligationTree.InsideMaximalTarget",
            "S-TRANSPORT": "Stage1Instances.THM_M_0072.OutsideMaximalTarget",
            "N-OUTSIDE": "Stage1Instances.THM_M_0072.ObligationTree.TransferOutsideTarget",
            "T-INSIDE": "Stage1Instances.THM_M_0072.ObligationTree.InsideMaximalTarget",
            "T-OUTSIDE": "Stage1Instances.THM_M_0072.ObligationTree.TransferOutsideTarget",
            "T-ASSEMBLE": "Stage1Instances.THM_M_0072.ObligationTree.RootAssemblyTarget",
        }.get(suffix, f"planned exact Lean signature for {oid}: {statement}")
        output = statement
        premise_map = {
            "ROOT": [f"{PREFIX}-T-ASSEMBLE"],
            "B-MEMBERSHIP": [f"{PREFIX}-T-INSIDE", f"{PREFIX}-T-OUTSIDE"],
            "T-ASSEMBLE": [f"{PREFIX}-B-MEMBERSHIP"],
            "T-OUTSIDE": [f"{PREFIX}-B-CONTRADICTION"],
            "B-CONTRADICTION": [f"{PREFIX}-L-ODD-PRODUCT", f"{PREFIX}-L-NOINDEX-TRANSFER"],
            "L-ODD-PRODUCT": [f"{PREFIX}-L-FIXED-PARITY", f"{PREFIX}-L-TRANSFER-FORMULA", f"{PREFIX}-L-FACTOR-DICHOTOMY"],
            "L-FIXED-PARITY": [f"{PREFIX}-L-SYLOW-ODD", f"{PREFIX}-C-COSET-ACTION"],
            "L-FACTOR-DICHOTOMY": [f"{PREFIX}-C-QUOTIENT", f"{PREFIX}-C-TRANSFER"],
            "L-NOINDEX-TRANSFER": [f"{PREFIX}-C-QUOTIENT", f"{PREFIX}-L-INDEX-TWO"],
            "C-TRANSFER": [f"{PREFIX}-C-NORMAL", f"{PREFIX}-C-QUOTIENT"],
            "C-QUOTIENT": [f"{PREFIX}-C-NORMAL", f"{PREFIX}-L-INDEX-TWO"],
            "C-NORMAL": [f"{PREFIX}-N-OUTSIDE"],
            "L-INDEX-TWO": [f"{PREFIX}-N-OUTSIDE"],
            "N-OUTSIDE": [f"{PREFIX}-S-TRANSPORT"],
        }
        premises = premise_map.get(suffix, [])
        source_anchor = (
            "Statement.lean#ThompsonTransferLemmaTarget" if suffix.startswith("S-") or suffix == "ROOT"
            else "source-statement-crosswalk.md#primary-source-lead"
        )
        nodes.append({
            "node_id": f"{THEOREM_ID}-{suffix}",
            "obligation_id": oid,
            "kind": kind,
            "human_statement": statement,
            "formal_target": formal_target,
            "output": output,
            "human_debt": "H1",
            "machine_debt": "M3" if suffix in {"ROOT", "T-ASSEMBLE", "B-MEMBERSHIP", "T-OUTSIDE", "X-SOURCE", "X-PROVENANCE", "X-TRUST", "X-READABLE", "X-WORKFLOW"} else ("M0-L" if suffix in {"S-TARGET", "S-BOUNDARY", "S-TRANSPORT", "T-INSIDE"} else "M4"),
            "readability_debt": "R4",
            "evidence_ids": [],
            "source_crosswalk_id": "source-statement-crosswalk.md#primary-source-lead" if suffix not in no_human else "not-applicable-pending-review",
            "provenance_id": "anchor-audit.json#candidates" if suffix in {"C-TRANSFER", "L-TRANSFER-FORMULA", "X-PROVENANCE"} else "none",
            "foundation_profile": "lean4-dependent-type-theory-planned/1.0; acceptance pending",
            "tcb_profile": "lean-4.29.0+mathlib-8a178386; transitive trust closure pending",
            "computation_record": "none; symbolic transfer argument with no oracle, native computation, experiment, or unchecked certificate",
            "step_budget": 24 if risk == "critical" else 16,
            "semantic_step_ledger": {
                "premises": premises,
                "inference": statement,
                "output": output,
                "source_anchors": [source_anchor],
                "outgoing_use": "Supplies this exact output only along registered typed edges.",
                "steps": [{
                    "step_id": f"{oid}-STEP-01",
                    "premise_ids": premises,
                    "inference": statement,
                    "output": output,
                    "source_anchors": [source_anchor],
                    "outgoing_use": "Supplies this exact output only along registered typed edges.",
                }],
                "ledger_state": "architecture_frozen_not_R0_proof_reconstruction",
            },
            "public_readable_target": f"{readable_path}#{oid.lower()}",
            "validation_spec_id": f"VAL-{oid}",
            "status_boundary": "Frozen architecture or checked conditional interface only; no accepted proof closure, H0, R0, AUDIT-Z, or theorem completion.",
            "task_ids": [ITEM_ID, "S56-M-0072-PROOF"],
            "owned_sources": [f"Stage1_Instances/{THEOREM_ID}/obligation-registry.json", f"Stage1_Instances/{THEOREM_ID}/typed-graphs.json", f"{readable_path}#{oid.lower()}"],
            "owner": "THM-M-0072 proof lane",
            "reviewer": "unassigned independent Stage1 integration-lane reviewer",
            "validity": {
                "validated_at": "2026-07-15" if suffix in {"S-TARGET", "S-BOUNDARY", "S-TRANSPORT", "T-INSIDE", "T-ASSEMBLE", "ROOT"} else None,
                "review_due": "before master acceptance of the obligation-tree node",
                "invalidation_inputs": ["Statement.lean", "statement.json", "anchor-audit.json", "obligation registry", "typed graphs", "toolchain", "dependency pin", "source correction", "assurance profile"],
                "revocation_state": "provisional_interface_check" if suffix in {"S-TARGET", "S-BOUNDARY", "S-TRANSPORT", "T-INSIDE", "T-ASSEMBLE", "ROOT"} else "open",
            },
        })

    projection = [{key: obligation[key] for key in FIELDS} for obligation in obligations]
    denominator = hashlib.sha256(json.dumps(projection, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    ids = [obligation["obligation_id"] for obligation in obligations]
    registry = {
        "schema_version": "stage1-obligation-registry/1.0",
        "normative_profile": "machine-theorem-assurance/1.0",
        "item_id": ITEM_ID,
        "theorem_id": THEOREM_ID,
        "registry_id": "THM-M-0072-OBLIGATIONS-v1",
        "registry_version": 1,
        "frozen_at": FROZEN_AT,
        "freeze_basis": "The exact elaborated statement, the immutable bounded anchor audit, and Thompson's printed page-411 transfer proof determine the inside/outside split, maximal-subgroup quotient, transfer/coset/parity route, contradiction, and assurance boundaries. Eligibility was fixed before observing closure.",
        "frozen_against_statement_sha256": statement_hash,
        "frozen_against_anchor_audit_sha256": anchor_hash,
        "primary_architecture_source": {"source_id": "SRC-THOMPSON-1968-L538", "locator": "Lemma 5.38(a)(i), printed page 411", "pdf_sha256": "93f494417422c31b1bd5a5bd92f3741b7a41bbd8f1581b224d0a5459bc5da83d"},
        "root_obligation_id": f"{PREFIX}-ROOT",
        "denominator_sha256": denominator,
        "frozen_denominators": {
            "inventory": ids,
            "required_machine": [o["obligation_id"] for o in obligations if o["machine_eligibility"] == "required"],
            "required_human_source": [o["obligation_id"] for o in obligations if o["human_source_eligibility"] == "required"],
            "required_readable": ids,
            "informational_overlays": [o["obligation_id"] for o in obligations if o["machine_eligibility"] == "informational"],
            "required_unique_logical_frontier": [f"{PREFIX}-C-NORMAL", f"{PREFIX}-L-INDEX-TWO", f"{PREFIX}-C-TRANSFER", f"{PREFIX}-L-SYLOW-ODD", f"{PREFIX}-C-COSET-ACTION", f"{PREFIX}-L-FIXED-PARITY", f"{PREFIX}-L-TRANSFER-FORMULA", f"{PREFIX}-L-FACTOR-DICHOTOMY", f"{PREFIX}-L-ODD-PRODUCT", f"{PREFIX}-L-NOINDEX-TRANSFER"],
            "required_interface_transport": [f"{PREFIX}-S-TRANSPORT", f"{PREFIX}-T-INSIDE", f"{PREFIX}-T-ASSEMBLE"],
        },
        "layer_applicability": {
            "S_statement_foundation": {"state": "required", "obligation_ids": [f"{PREFIX}-S-TARGET", f"{PREFIX}-S-DOMAIN", f"{PREFIX}-S-BOUNDARY", f"{PREFIX}-S-TRANSPORT", f"{PREFIX}-S-FOUNDATION"]},
            "N_normalization": {"state": "required", "obligation_ids": [f"{PREFIX}-N-OUTSIDE"]},
            "B_mathematical_branch": {"state": "required", "obligation_ids": [f"{PREFIX}-B-MEMBERSHIP", f"{PREFIX}-B-CONTRADICTION"]},
            "C_construction": {"state": "required", "obligation_ids": [f"{PREFIX}-C-NORMAL", f"{PREFIX}-C-QUOTIENT", f"{PREFIX}-C-TRANSFER", f"{PREFIX}-C-COSET-ACTION"]},
            "L_core_lemma": {"state": "required", "obligation_ids": [f"{PREFIX}-L-INDEX-TWO", f"{PREFIX}-L-SYLOW-ODD", f"{PREFIX}-L-FIXED-PARITY", f"{PREFIX}-L-TRANSFER-FORMULA", f"{PREFIX}-L-FACTOR-DICHOTOMY", f"{PREFIX}-L-ODD-PRODUCT", f"{PREFIX}-L-NOINDEX-TRANSFER"]},
            "X_external_computation": {"state": "required_external_boundary_and_not_applicable_computation_pending_independent_approval", "reason": "Pinned transfer declarations, provenance, source, trust, documentation, and workflow are material. No computation, oracle, or unchecked certificate is credited.", "obligation_ids": [f"{PREFIX}-X-SOURCE", f"{PREFIX}-X-PROVENANCE", f"{PREFIX}-X-TRUST", f"{PREFIX}-X-READABLE", f"{PREFIX}-X-WORKFLOW"], "reviewer": "unassigned independent Lean/TCB reviewer"},
            "T_terminal": {"state": "required", "obligation_ids": [f"{PREFIX}-T-INSIDE", f"{PREFIX}-T-OUTSIDE", f"{PREFIX}-T-ASSEMBLE", f"{PREFIX}-ROOT"]},
        },
        "deduplication_policy": "The universal root, outside-form transport, assembly wrapper, and readable projections do not duplicate semantic proof credit. Transfer and focal declarations retain distinct pinned terminal identities and remain substrate only.",
        "delta_policy": "Any target correction, split, merge, exclusion, eligibility, risk, or terminal-body-identity change requires registry v2 with an append-only old/new ID delta; v1 denominators remain reportable.",
        "append_only_delta": [],
        "obligations": obligations,
        "status_observed_after_freeze": {"checked_conditional_interfaces": [f"{PREFIX}-T-INSIDE", f"{PREFIX}-T-ASSEMBLE", f"{PREFIX}-ROOT"], "audited_substrate_obligations": [f"{PREFIX}-C-TRANSFER", f"{PREFIX}-L-TRANSFER-FORMULA"], "accepted_closed_obligations": [], "root_machine_debt": "M3"},
        "status_boundary": "Registry and architecture freeze only. The transfer branch and all internal source packages are open; no exact Lean root proof, accepted closure, H0, R0, audit completion, validation, release, or theorem completion is claimed.",
    }

    graph_names = ("proof", "refinement", "provenance", "evidence", "trust", "documentation", "workflow")
    graphs = {name: {"edges": [], "out": {oid: [] for oid in ids}, "in": {oid: [] for oid in ids}} for name in graph_names}

    def add_edge(graph: str, edge_id: str, edge_type: str, src: str, dst: str, reciprocal: str | None = None) -> None:
        edge = {"edge_id": edge_id, "type": edge_type, "from": src, "to": dst}
        if reciprocal is not None:
            edge["reciprocal_edge_id"] = reciprocal
        graphs[graph]["edges"].append(edge)
        graphs[graph]["out"][src].append(edge_id)
        graphs[graph]["in"][dst].append(edge_id)

    checked_pairs = [(f"{PREFIX}-B-MEMBERSHIP", f"{PREFIX}-T-INSIDE"), (f"{PREFIX}-B-MEMBERSHIP", f"{PREFIX}-T-OUTSIDE")]
    for index, (parent, child) in enumerate(checked_pairs, 1):
        add_edge("proof", f"P{index:02d}-REQ", "proof_requires", parent, child, f"P{index:02d}-COMP")
        add_edge("proof", f"P{index:02d}-COMP", "composes", child, parent, f"P{index:02d}-REQ")

    architecture_pairs = [
        (f"{PREFIX}-ROOT", f"{PREFIX}-T-ASSEMBLE"),
        (f"{PREFIX}-T-ASSEMBLE", f"{PREFIX}-B-MEMBERSHIP"),
        (f"{PREFIX}-T-OUTSIDE", f"{PREFIX}-B-CONTRADICTION"),
        (f"{PREFIX}-B-CONTRADICTION", f"{PREFIX}-L-ODD-PRODUCT"),
        (f"{PREFIX}-B-CONTRADICTION", f"{PREFIX}-L-NOINDEX-TRANSFER"),
        (f"{PREFIX}-L-ODD-PRODUCT", f"{PREFIX}-L-FIXED-PARITY"),
        (f"{PREFIX}-L-ODD-PRODUCT", f"{PREFIX}-L-TRANSFER-FORMULA"),
        (f"{PREFIX}-L-ODD-PRODUCT", f"{PREFIX}-L-FACTOR-DICHOTOMY"),
        (f"{PREFIX}-L-FIXED-PARITY", f"{PREFIX}-L-SYLOW-ODD"),
        (f"{PREFIX}-L-FIXED-PARITY", f"{PREFIX}-C-COSET-ACTION"),
        (f"{PREFIX}-L-FACTOR-DICHOTOMY", f"{PREFIX}-C-QUOTIENT"),
        (f"{PREFIX}-L-FACTOR-DICHOTOMY", f"{PREFIX}-C-TRANSFER"),
        (f"{PREFIX}-L-NOINDEX-TRANSFER", f"{PREFIX}-C-QUOTIENT"),
        (f"{PREFIX}-L-NOINDEX-TRANSFER", f"{PREFIX}-L-INDEX-TWO"),
        (f"{PREFIX}-C-TRANSFER", f"{PREFIX}-C-NORMAL"),
        (f"{PREFIX}-C-TRANSFER", f"{PREFIX}-C-QUOTIENT"),
        (f"{PREFIX}-C-QUOTIENT", f"{PREFIX}-C-NORMAL"),
        (f"{PREFIX}-C-QUOTIENT", f"{PREFIX}-L-INDEX-TWO"),
        (f"{PREFIX}-C-NORMAL", f"{PREFIX}-N-OUTSIDE"),
        (f"{PREFIX}-L-INDEX-TWO", f"{PREFIX}-N-OUTSIDE"),
    ]
    for index, (parent, child) in enumerate(architecture_pairs, 1):
        add_edge("proof", f"U{index:02d}", "logical_decomposition", parent, child)

    for index, child in enumerate((f"{PREFIX}-S-TARGET", f"{PREFIX}-S-DOMAIN", f"{PREFIX}-S-BOUNDARY", f"{PREFIX}-S-TRANSPORT", f"{PREFIX}-S-FOUNDATION"), 1):
        add_edge("refinement", f"R{index:02d}", "expository_decomposition", f"{PREFIX}-ROOT", child)
    add_edge("refinement", "R06", "transports", f"{PREFIX}-S-TRANSPORT", f"{PREFIX}-N-OUTSIDE")

    provenance_pairs = [(f"{PREFIX}-X-SOURCE", oid, "source_map") for oid in ids if oid not in governance and oid != f"{PREFIX}-X-SOURCE"]
    provenance_pairs += [(f"{PREFIX}-X-PROVENANCE", f"{PREFIX}-C-TRANSFER", "provenance_of"), (f"{PREFIX}-X-PROVENANCE", f"{PREFIX}-L-TRANSFER-FORMULA", "provenance_of"), (f"{PREFIX}-X-PROVENANCE", f"{PREFIX}-T-ASSEMBLE", "provenance_of")]
    for index, (src, dst, edge_type) in enumerate(provenance_pairs, 1):
        add_edge("provenance", f"V{index:02d}", edge_type, src, dst)
    for index, src in enumerate((f"{PREFIX}-ROOT", f"{PREFIX}-C-TRANSFER", f"{PREFIX}-L-TRANSFER-FORMULA", f"{PREFIX}-T-ASSEMBLE"), 1):
        add_edge("trust", f"T{index:02d}", "trusts", src, f"{PREFIX}-X-TRUST")
    add_edge("trust", "T05", "trusts", f"{PREFIX}-X-TRUST", f"{PREFIX}-S-FOUNDATION")
    for index, oid in enumerate(ids, 1):
        if oid != f"{PREFIX}-X-READABLE":
            add_edge("documentation", f"D{index:02d}", "documents", f"{PREFIX}-X-READABLE", oid)
    for index, dependency in enumerate((f"{PREFIX}-T-ASSEMBLE", f"{PREFIX}-X-SOURCE", f"{PREFIX}-X-PROVENANCE", f"{PREFIX}-X-TRUST", f"{PREFIX}-X-READABLE"), 1):
        add_edge("workflow", f"W{index:02d}", "workflow_depends_on", f"{PREFIX}-X-WORKFLOW", dependency)

    bundle = {
        "schema_version": "stage1-typed-graphs/1.0",
        "normative_profile": "machine-theorem-assurance/1.0",
        "item_id": ITEM_ID,
        "theorem_id": THEOREM_ID,
        "registry_id": registry["registry_id"],
        "registry_denominator_sha256": denominator,
        "frozen_against_execution_dag_sha256": sha256(execution_dag_path),
        "local_task_dag_projection_sha256": sha256(HERE / "task-dag.json"),
        "root_node_id": f"{PREFIX}-ROOT",
        "edge_endpoint_namespace": "canonical obligation_id except the separate workflow_task_graph task namespace",
        "edge_direction": "proof_requires parent-to-child; composes child-to-parent; logical_decomposition parent-to-unverified child; non-proof graphs grant no proof credit",
        "nodes": nodes,
        "graphs": graphs,
        "evidence_endpoint_policy": "No content-addressed evidence exists for this phase; the evidence graph is empty and node evidence_ids remain empty.",
        "composition_certificates": [
            {"certificate_id": "M0072-CERT-INSIDE", "declaration": "Stage1Instances.THM_M_0072.ObligationTree.insideMaximalConclusion", "parent_id": f"{PREFIX}-T-INSIDE", "required_child_ids": [], "conditional": False, "accepted": False},
            {"certificate_id": "M0072-CERT-MEMBERSHIP", "declaration": "Stage1Instances.THM_M_0072.ObligationTree.assembly_of_outside_and_inside", "parent_id": f"{PREFIX}-B-MEMBERSHIP", "required_child_ids": [f"{PREFIX}-T-INSIDE", f"{PREFIX}-T-OUTSIDE"], "conditional": True, "accepted": False},
            {"certificate_id": "M0072-CERT-ASSEMBLY", "declaration": "Stage1Instances.THM_M_0072.ObligationTree.root_of_assembly", "parent_id": f"{PREFIX}-T-ASSEMBLE", "required_child_ids": [f"{PREFIX}-B-MEMBERSHIP"], "conditional": True, "accepted": False, "certificate_scope": "planned semantic mapping pending a direct exact child-typed wrapper", "modeling_note": "The assembly proposition is definitionally the two branch children; root_of_assembly consumes both through the membership split."},
            {"certificate_id": "M0072-CERT-ROOT", "declaration": "Stage1Instances.THM_M_0072.ObligationTree.root_of_outsideTransfer", "parent_id": f"{PREFIX}-ROOT", "required_child_ids": [f"{PREFIX}-T-ASSEMBLE"], "conditional": True, "accepted": False, "certificate_scope": "planned semantic mapping pending a direct exact child-typed wrapper", "modeling_note": "The concrete Lean harness composes the open outside target with the checked inside branch and then applies root_of_assembly."},
        ],
        "harness_relationships": [
            {"declaration": "Stage1Instances.THM_M_0072.ObligationTree.root_of_assembly", "relationship": "RootAssemblyTarget -> ThompsonTransferLemmaTarget", "registered_graph_path": [f"{PREFIX}-B-MEMBERSHIP", f"{PREFIX}-T-ASSEMBLE", f"{PREFIX}-ROOT"], "graph_edge_state": "logical_decomposition_pending_direct_exact_child_certificate", "closure_credit": False},
            {"declaration": "Stage1Instances.THM_M_0072.ObligationTree.root_of_outsideTransfer", "relationship": "TransferOutsideTarget -> ThompsonTransferLemmaTarget", "registered_graph_path": [f"{PREFIX}-T-OUTSIDE", f"{PREFIX}-B-MEMBERSHIP", f"{PREFIX}-T-ASSEMBLE", f"{PREFIX}-ROOT"], "graph_edge_state": "conditional_harness_only", "closure_credit": False}
        ],
        "unverified_decomposition_count": len(architecture_pairs),
        "closure_boundary": {"root_closed": False, "root_machine_classification": "M3", "accepted_closed_obligations": [], "checked_conditional_interfaces": [f"{PREFIX}-T-INSIDE", f"{PREFIX}-B-MEMBERSHIP", f"{PREFIX}-T-ASSEMBLE", f"{PREFIX}-ROOT"], "remaining_root_cut_set": [f"{PREFIX}-T-OUTSIDE"], "expanded_open_frontier": registry["frozen_denominators"]["required_unique_logical_frontier"], "remaining_root_critical_nonproof_gates": [f"{PREFIX}-S-FOUNDATION", f"{PREFIX}-X-SOURCE", f"{PREFIX}-X-PROVENANCE", f"{PREFIX}-X-TRUST", f"{PREFIX}-X-READABLE", f"{PREFIX}-X-WORKFLOW"], "audit_complete": False, "theorem_complete": False, "reason": "The inside branch and conditional merge elaborate, but the transfer branch and every source-derived internal composition are open."},
    }
    bundle["typed_edge_count"] = sum(len(graph["edges"]) for graph in graphs.values())
    task_nodes = [{"task_id": task["id"], "phase": task["phase"], "layer": task["layer"]} for task in authoritative_tasks]
    task_edges = [{"edge_id": f"TASK-{index:02d}", "type": "workflow_depends_on", "from": task["id"], "to": dependency} for index, task in enumerate(authoritative_tasks, 1) for dependency in task["depends_on"]]
    bundle["workflow_task_graph"] = {"authority": "Docs/Stage1_Execution_DAG_rev-5.6.json", "authority_sha256": sha256(execution_dag_path), "nodes": task_nodes, "edges": task_edges, "task_obligation_links": [{"task_id": ITEM_ID, "obligation_id": oid} for oid in ids] + [{"task_id": "S56-M-0072-PROOF", "obligation_id": oid} for oid in registry["frozen_denominators"]["required_machine"]]}
    bundle["metrics_projection"] = {"inventory_classified": f"{len(ids)}/{len(ids)}", "unique_logical_leaf_closure": "0/10 accepted", "interface_transport_checked_provisional": "3/3", "accepted_machine_closure": "0", "audit_complete": False, "theorem_complete": False}

    recipes = [{"recipe_id": f"VAL-{oid}", "cwd": ".", "argv": ["python3", "-B", f"Stage1_Instances/{THEOREM_ID}/check_obligation_tree.py"], "env_allowlist": {}, "timeout_seconds": 180, "network_policy": "denied", "expected_exit": 0, "expected_outputs": [{"path_or_stream": "stdout", "semantic_hash_policy": "contains PASS THM-M-0072 obligation tree"}], "covered_obligation_ids": [oid], "covered_declarations": [], "coverage_semantics": "architecture_or_conditional_interface_validation_only", "closure_credit": False} for oid in ids]
    recipes += [
        {"recipe_id": "S56-M-0072-OBLIGATION-TREE-GENERATOR-CHECK", "cwd": ".", "argv": ["python3", "-B", f"Stage1_Instances/{THEOREM_ID}/build_obligation_artifacts.py", "--check"], "env_allowlist": {}, "timeout_seconds": 60, "network_policy": "denied", "expected_exit": 0, "expected_outputs": [{"path_or_stream": "stdout", "semantic_hash_policy": "reports deterministic artifact equality"}], "covered_obligation_ids": ids, "covered_declarations": [], "coverage_semantics": "generator_drift_check", "closure_credit": False},
        {"recipe_id": "S56-M-0072-OBLIGATION-TREE-LEAN", "cwd": ".", "argv": ["python3", "-B", f"Stage1_Instances/{THEOREM_ID}/check_obligation_tree.py"], "env_allowlist": {}, "timeout_seconds": 180, "network_policy": "denied", "expected_exit": 0, "expected_outputs": [{"path_or_stream": "stdout", "semantic_hash_policy": "reports temporary Statement olean and ObligationTree elaboration hash"}], "covered_obligation_ids": [f"{PREFIX}-ROOT", f"{PREFIX}-T-INSIDE", f"{PREFIX}-B-MEMBERSHIP", f"{PREFIX}-T-ASSEMBLE", f"{PREFIX}-T-OUTSIDE"], "covered_declarations": ["Stage1Instances.THM_M_0072.ObligationTree.insideMaximalConclusion", "Stage1Instances.THM_M_0072.ObligationTree.assembly_of_outside_and_inside", "Stage1Instances.THM_M_0072.ObligationTree.root_of_assembly", "Stage1Instances.THM_M_0072.ObligationTree.root_of_outsideTransfer"], "coverage_semantics": "conditional_composition_and_exact_root_identity_only", "closure_credit": False},
    ]
    specs = {"schema_version": "stage1-validation-specs/1.0", "normative_profile": "machine-theorem-assurance/1.0", "item_id": ITEM_ID, "theorem_id": THEOREM_ID, "recipes": recipes}
    return registry, bundle, specs


def serialized(value: dict) -> str:
    return json.dumps(value, ensure_ascii=True, indent=2) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()
    artifacts = dict(zip(("obligation-registry.json", "typed-graphs.json", "validation-specs.json"), build()))
    if args.write:
        for name, value in artifacts.items():
            (HERE / name).write_text(serialized(value))
    else:
        for name, value in artifacts.items():
            assert (HERE / name).read_text() == serialized(value), f"generated artifact drift: {name}"
    registry, bundle, _ = artifacts.values()
    print(f"{'wrote' if args.write else 'PASS deterministic artifacts:'} {len(registry['obligations'])} obligations, {bundle['typed_edge_count']} typed edges")
    print(f"registry denominator sha256: {registry['denominator_sha256']}")


if __name__ == "__main__":
    main()
