#!/usr/bin/env python3
"""Build or verify the frozen THM-M-0063 obligation registry and graph bundle."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ITEM_ID = "S56-M-0063-OBLIGATION_TREE"
THEOREM_ID = "THM-M-0063"
PREFIX = "M0063"
FROZEN_AT = "2026-07-13T00:00:00+08:00"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def row(
    suffix: str,
    kind: str,
    human: str,
    formal: str,
    output: str,
    risk: str,
    machine: str = "M3",
    machine_required: bool = True,
    source_required: bool = False,
    terminal_body: str | None = None,
    budget: int = 20,
    premises: str = "The frozen formal context and incoming typed proof premises.",
    inference: str | None = None,
    source_anchors: list[str] | None = None,
    outgoing: str = "Supplies the node's exact output only along its typed outgoing edges.",
) -> dict:
    obligation_id = f"{PREFIX}-{suffix}"
    return {
        "obligation_id": obligation_id,
        "kind": kind,
        "human": human,
        "formal": formal,
        "output": output,
        "risk": risk,
        "machine": machine,
        "machine_required": machine_required,
        "source_required": source_required,
        "terminal_body": terminal_body,
        "budget": budget,
        "premises": premises,
        "inference": inference or human,
        "source_anchors": source_anchors or [],
        "outgoing": outgoing,
    }


ROWS = [
    row("ROOT", "root", "Every universe-polymorphic group is multiplicatively equivalent to the range of its left-regular permutation representation.", "Stage1Instances.THM_M_0063.CayleyTheoremTarget", "The exact canonical Cayley proposition.", "critical", source_required=True, budget=8, premises="M0063-T-ASSEMBLE with the exact statement context.", inference="Apply the exact checked assembly certificate without changing binders, universes, or subgroup carrier.", source_anchors=["Statement.lean#CayleyTheoremTarget"]),
    row("S-EXACT", "definition", "Freeze the arbitrary-group binder and range-subgroup conclusion without a finiteness or nontriviality premise.", "Stage1Instances.THM_M_0063.CayleyTheoremTarget", "The canonical statement interface and expression fingerprint.", "critical", machine_required=False, budget=6, premises="The statement-gate expression fingerprint and its two minimal imports.", inference="Read the exact elaborated proposition; create no second proof obligation for its presentation alias.", source_anchors=["statement.json#canonical_formal_target"]),
    row("S-DOMAIN", "definition", "Fix one carrier G : Type u, its Group instance, the inferred left action, and the range inside Equiv.Perm G.", "forall (G : Type u) [Group G], Nonempty (G ≃* (MulAction.toPermHom G G).range)", "Universe, typeclass, coercion, action-orientation, and subgroup-carrier contract.", "high", machine_required=False, budget=8, premises="M0063-S-EXACT and the statement's ordered binder record.", inference="Resolve the regular left action and the codomain subgroup on the same carrier without adding instances.", source_anchors=["statement.json#domain_and_universes"]),
    row("S-BOUNDARY", "branch", "Retain the trivial, finite, and infinite group boundaries; no mathematical case split is used by the proof route.", "Statement.trivialGroupBoundary; Statement.infiniteCarrierBoundary", "Boundary inclusion and an explicit no-case-split decision.", "high", machine_required=False, budget=8, premises="M0063-S-DOMAIN and both checked statement boundary surfaces.", inference="Confirm the same target elaborates at the recorded boundary carriers and that none is excluded.", source_anchors=["Statement.lean#trivialGroupBoundary", "Statement.lean#infiniteCarrierBoundary"]),
    row("S-TRANSPORT", "transport", "Map the canonical range formulation in the proved direction to existence of a permutation subgroup.", "Stage1Instances.THM_M_0063.cayleyTheoremTarget_implies_permutationSubgroupExistenceTarget", "The catalog wording, only as a checked canonical-to-existential implication.", "high", machine_required=False, terminal_body="repo:Statement.lean#cayleyTheoremTarget_implies_permutationSubgroupExistenceTarget", budget=8, premises="M0063-S-EXACT.", inference="Choose the range of the regular permutation homomorphism as the existential subgroup.", source_anchors=["Statement.lean#cayleyTheoremTarget_implies_permutationSubgroupExistenceTarget"]),
    row("S-FOUNDATION", "certificate", "Account for extensionality, quotient soundness, classical choice, kernel, and computation policy used by the eventual proof route.", "planned exact transitive axiom and TCB report", "A reviewed foundation/TCB decision; no theorem premise.", "critical", budget=20, premises="The frozen foundation profile and machine-derived axiom reports for every terminal body.", inference="Compare the transitive axiom set against the selected foundation profile and reject unknown trust.", source_anchors=["anchor-audit.json#candidates/0/axioms"]),
    row("N-REGULAR", "normalization", "Specialize the generalized faithful-action construction to H = G with the inferred left-regular action and faithful instance.", "ObligationTree.exactTarget_of_generalFaithfulAction", "The exact regular-action Cayley target.", "critical", source_required=True, terminal_body="repo:ObligationTree.lean#exactTarget_of_generalFaithfulAction", budget=8, premises="M0063-L-REGULAR-FAITHFUL and the Group G typeclass context.", inference="Install the explicit regular-action faithfulness child and instantiate H with G.", source_anchors=["ObligationTree.lean#exactTarget_of_generalFaithfulAction"]),
    row("C-PERM-HOM", "construction", "Construct MulAction.toPermHom G H from a group action and preserve multiplication into Equiv.Perm H.", "MulAction.toPermHom", "The permutation-valued monoid homomorphism used by injectivity and range construction.", "high", source_required=True, terminal_body="mathlib:8a178386#MulAction.toPermHom", budget=30, premises="Group G and MulAction G H.", inference="Package each action map as a permutation and prove the identity and multiplication laws.", source_anchors=["Mathlib.Algebra.Group.Action.End#MulAction.toPermHom"]),
    row("L-POINTWISE", "core_lemma", "A faithful action separates group elements when their action agrees at every point.", "ObligationTree.PointwiseFaithfulness", "Pointwise action equality implies equality in G.", "critical", source_required=True, terminal_body="mathlib:8a178386#FaithfulSMul", budget=20, premises="Group G, MulAction G H, FaithfulSMul G H, and pointwise equality for g and h.", inference="Use the faithful scalar-action interface to conclude g = h.", source_anchors=["Mathlib.Algebra.Group.Action.Faithful"]),
    row("L-REGULAR-FAITHFUL", "core_lemma", "The left-regular action of every group on its carrier is faithful.", "ObligationTree.RegularFaithfulness", "FaithfulSMul G G for the inferred left multiplication action.", "critical", source_required=True, terminal_body="mathlib:8a178386#instFaithfulSMul", budget=8, premises="Group G and equality of the left multiplications by g and h.", inference="Evaluate the pointwise equality at 1; the right identity reduces it to g = h.", source_anchors=["Mathlib.Algebra.Group.Action.Faithful#instFaithfulSMul"]),
    row("L-INJECTIVE", "core_lemma", "The faithful action's permutation homomorphism is injective.", "ObligationTree.GenericToPermInjectivity", "Function.Injective (MulAction.toPermHom G H).", "critical", source_required=True, terminal_body="mathlib:8a178386#MulAction.toPerm_injective", budget=12, premises="M0063-L-POINTWISE and equality of the two output permutations.", inference="Evaluate equal permutations at every x, then apply pointwise faithfulness.", source_anchors=["ObligationTree.lean#genericInjectivity_of_pointwiseFaithfulness", "Mathlib.Algebra.Group.Action.Basic#MulAction.toPerm_injective"]),
    row("C-LEFT-INVERSE", "construction", "Choose a left inverse for an injective permutation homomorphism and record the choice boundary.", "ObligationTree.LeftInverseConstructor", "A nonempty subtype containing a left inverse and its defining equation.", "critical", source_required=True, terminal_body="mathlib:8a178386#Function.Injective.hasLeftInverse", budget=35, premises="An injective homomorphism f and the accepted classical-choice boundary.", inference="Obtain a left-inverse witness from injectivity and project its defining equation with Classical.choose_spec.", source_anchors=["Mathlib.GroupTheory.Perm.Subgroup#Equiv.Perm.subgroupOfMulAction/body"]),
    row("C-MRANGE-EQUIV", "construction", "Use a specified left inverse to build a multiplicative equivalence with the monoid range.", "ObligationTree.MRangeEquivFromLeftInverse", "Nonempty (G ≃* MonoidHom.mrange f).", "critical", source_required=True, terminal_body="mathlib:8a178386#MulEquiv.ofLeftInverse'", budget=40, premises="A homomorphism f, a function g, and a proof that g is a left inverse of f.", inference="Apply the exact constructor used by the audited Cayley body.", source_anchors=["Mathlib.GroupTheory.Perm.Subgroup#Equiv.Perm.subgroupOfMulAction/body"]),
    row("N-MRANGE-RANGE", "transport", "Transport the monoid-range equivalence to the subgroup range of the same group homomorphism.", "ObligationTree.MRangeToRangeTransport", "Nonempty (G ≃* f.range).", "critical", source_required=True, terminal_body="mathlib:8a178386#MonoidHom.mrange-to-range-definitional-transport", budget=15, premises="M0063-C-MRANGE-EQUIV and the group structure on source and codomain.", inference="Use the definitional/coercion alignment by which the audited body has the subgroup-range conclusion.", source_anchors=["Mathlib.GroupTheory.Perm.Subgroup#Equiv.Perm.subgroupOfMulAction/type-and-body"]),
    row("T-GENERAL", "terminal", "For every faithful action, identify G with the range of its permutation representation.", "ObligationTree.GeneralFaithfulActionPackage", "Nonempty (G ≃* (MulAction.toPermHom G H).range).", "critical", source_required=True, terminal_body="mathlib:8a178386#Equiv.Perm.subgroupOfMulAction", budget=12, premises="M0063-C-PERM-HOM, M0063-L-INJECTIVE, M0063-C-LEFT-INVERSE, M0063-C-MRANGE-EQUIV, and M0063-N-MRANGE-RANGE.", inference="Construct the exact permutation homomorphism, choose its left inverse, build the mrange equivalence, and transport to subgroup range.", source_anchors=["ObligationTree.lean#generalPackage_of_components", "Mathlib.GroupTheory.Perm.Subgroup#Equiv.Perm.subgroupOfMulAction"]),
    row("T-ASSEMBLE", "terminal", "Compose the generalized package and regular specialization into the literal canonical root.", "ObligationTree.exactAssembly_of_components", "ObligationTree.ExactAssembly, definitionally the actual statement declaration.", "critical", source_required=True, terminal_body="repo:ObligationTree.lean#exactAssembly_of_components", budget=6, premises="M0063-N-REGULAR and M0063-T-GENERAL.", inference="Apply the checked regular-specialization interface to the generalized package.", source_anchors=["ObligationTree.lean#exactAssembly_of_components"]),
    row("X-UPSTREAM", "bridge", "Bind the exact pinned mathlib Cayley declaration and deduplicate instructional wrappers to its terminal body.", "Equiv.Perm.subgroupOfMulAction", "Immutable upstream declaration, source body, revision, license, and duplicate-family classification.", "critical", machine_required=False, source_required=True, terminal_body="mathlib:8a178386#Equiv.Perm.subgroupOfMulAction", budget=35, premises="The bounded anchor inventory and immutable mathlib source snapshot.", inference="Resolve wrapper, terminal declaration, proof body, and duplicate candidates without granting proof-phase acceptance.", source_anchors=["anchor-audit.json#M0063-C01-MATHLIB-CAYLEY"]),
    row("X-SOURCE", "terminal", "Map every root-relevant mathematical node to a pinpoint primary human proof source and definition transport.", "not a Lean proof premise", "An independently reviewed H0 source crosswalk.", "high", machine_required=False, source_required=True, budget=100, premises="The 1854 primary-paper lead plus a preserved edition, pinpoint passage, assumptions, errata, and modern-definition transport.", inference="Reconstruct and independently review the source-to-node map; citations alone do not close it.", source_anchors=["source-statement-crosswalk.md"]),
    row("X-PROVENANCE", "certificate", "Resolve wrapper, terminal body, direct and transitive declarations, origins, source hashes, and license.", "planned transitive provenance packet", "Accepted provenance for every root-critical formal body.", "critical", machine_required=False, budget=100, premises="Pinned source bodies for M0063-L-INJECTIVE, M0063-C-MRANGE-EQUIV, M0063-N-MRANGE-RANGE, M0063-T-GENERAL, and all transitive dependencies.", inference="Traverse actual declaration bodies and deduplicate all aliases by terminal proof-body identity.", source_anchors=["anchor-audit.json#candidate_inventory"]),
    row("X-TRUST", "certificate", "Close the transitive axiom, compiled-artifact, executable, computation, and TCB inventory.", "planned machine-derived trust closure", "Accepted trust closure under the selected foundation profile.", "critical", machine_required=False, budget=100, premises="M0063-S-FOUNDATION and the transitive provenance closure.", inference="Hash and classify every trusted element; unknown or undeclared trust fails closed.", source_anchors=["anchor-audit-receipt.json#candidate_result/axioms"]),
    row("X-DOCUMENTATION", "terminal", "Provide unique reader-facing entries for every required readable obligation.", "obligation-tree.md plus future readable reconstruction", "Stable path#anchor mappings and independent R0 review receipts.", "high", machine_required=False, budget=100, premises="The frozen registry, typed graphs, source map, and accepted formal provenance.", inference="Reconstruct each proof step in domain language without turning architecture prose into proof credit.", source_anchors=["obligation-tree.md"]),
    row("X-WORKFLOW", "terminal", "Enforce prerequisite legality from obligation freeze through proof, validation, release, and revocation.", "task-dag.json plus node-scoped receipts", "Dependency-legal provisional and accepted execution states.", "critical", machine_required=False, budget=30, premises="The master-owned task DAG and content-addressed node receipts.", inference="Permit proof work only after this freeze is accepted and permit release only after every later gate closes.", source_anchors=["task-dag.json#S56-M-0063-OBLIGATION_TREE"]),
]

FIELDS = (
    "obligation_id",
    "statement_fingerprint",
    "kind",
    "root_relevant",
    "machine_eligibility",
    "human_source_eligibility",
    "readable_eligibility",
    "risk_class",
    "exclusion_reason",
    "terminal_proof_body_id",
)


def build() -> tuple[dict, dict, dict]:
    statement_hash = sha256(HERE / "Statement.lean")
    anchor_hash = sha256(HERE / "anchor-audit.json")
    execution_dag_path = ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json"
    execution_dag = json.loads(execution_dag_path.read_text())
    authoritative_tasks = [
        task for task in execution_dag["items"] if task["theorem_id"] == THEOREM_ID
    ]
    assert len(authoritative_tasks) == 7
    obligations = []
    nodes = []
    for entry in ROWS:
        fingerprint_payload = "\0".join(
            (entry["obligation_id"], entry["human"], entry["formal"], entry["output"])
        ).encode()
        if entry["obligation_id"] in {f"{PREFIX}-ROOT", f"{PREFIX}-S-EXACT"}:
            fingerprint = "lean-expression-sha256:40929846f1d1d1ff4479e5be6a989358a65ecebec5a2646f6e2dab508c641a1a"
        else:
            fingerprint = "architecture:v1:sha256:" + hashlib.sha256(fingerprint_payload).hexdigest()
        machine_eligibility = "required" if entry["machine_required"] else "informational"
        exclusion = None if entry["machine_required"] else "typed_overlay_or_statement_interface_no_duplicate_machine_proof_credit"
        obligations.append(
            {
                "obligation_id": entry["obligation_id"],
                "statement_fingerprint": fingerprint,
                "kind": entry["kind"],
                "root_relevant": True,
                "machine_eligibility": machine_eligibility,
                "human_source_eligibility": "required" if entry["source_required"] else "not_applicable",
                "readable_eligibility": "required",
                "risk_class": entry["risk"],
                "exclusion_reason": exclusion,
                "terminal_proof_body_id": entry["terminal_body"],
            }
        )
        oid = entry["obligation_id"]
        anchor = oid.lower()
        nodes.append(
            {
                "node_id": f"{THEOREM_ID}-{oid.removeprefix(PREFIX + '-')}",
                "obligation_id": oid,
                "kind": entry["kind"],
                "human_statement": entry["human"],
                "formal_target": entry["formal"],
                "output": entry["output"],
                "human_debt": "H1",
                "machine_debt": "M3",
                "readability_debt": "R4",
                "evidence_ids": [],
                "source_crosswalk_id": "source-statement-crosswalk.md#component-crosswalk" if entry["source_required"] else "not_applicable",
                "provenance_id": "anchor-audit:M0063-C01-pending-proof-phase-acceptance" if entry["terminal_body"] else "none",
                "foundation_profile": "lean4-foundation-planned/1.0; transitive acceptance remains open",
                "tcb_profile": "lean4-mathlib-tcb-planned/1.0; Lean 4.29.0 + mathlib 8a178386; full closure remains open",
                "computation_record": "not_applicable_pending_independent_approval; no computation, oracle, native evaluation, or certificate is part of this symbolic construction",
                "step_budget": entry["budget"],
                "semantic_step_ledger": {
                    "premises": entry["premises"],
                    "inference": entry["inference"],
                    "output": entry["output"],
                    "source_anchors": entry["source_anchors"],
                    "outgoing_use": entry["outgoing"],
                    "steps": [
                        {
                            "step_id": f"{oid}-STEP-01",
                            "premise_ids": re.findall(r"M0063-[A-Z][A-Z0-9-]*", entry["premises"]),
                            "inference": entry["inference"],
                            "output": entry["output"],
                            "source_anchors": entry["source_anchors"],
                            "outgoing_use": entry["outgoing"],
                        }
                    ],
                },
                "public_readable_target": f"Stage1_Instances/THM-M-0063/obligation-tree.md#{anchor}",
                "validation_spec_id": "VAL-" + oid,
                "status_boundary": "Frozen architecture only; proof-phase acceptance, H0, R0, full trust, AUDIT-Z, and theorem completion remain open.",
                "task_ids": [ITEM_ID, "S56-M-0063-PROOF"],
                "owned_sources": ["Stage1_Instances/THM-M-0063/obligation-registry.json", "Stage1_Instances/THM-M-0063/typed-graphs.json", f"Stage1_Instances/THM-M-0063/obligation-tree.md#{anchor}"],
                "owner": "THM-M-0063 proof lane",
                "reviewer": "unassigned independent Stage1 integration-lane reviewer",
                "validity": {
                    "validated_at": None,
                    "review_due": "before master acceptance of the obligation-tree node",
                    "invalidation_inputs": ["Statement.lean", "statement.json", "anchor-audit.json", "registry", "typed graphs", "toolchain", "dependency pin", "assurance profile"],
                    "revocation_state": "open",
                },
            }
        )

    projection = [{key: obligation[key] for key in FIELDS} for obligation in obligations]
    denominator = hashlib.sha256(
        json.dumps(projection, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    ids = [entry["obligation_id"] for entry in ROWS]
    registry = {
        "schema_version": "stage1-obligation-registry/1.0",
        "item_id": ITEM_ID,
        "theorem_id": THEOREM_ID,
        "registry_id": "THM-M-0063-OBLIGATIONS-v1",
        "registry_version": 1,
        "frozen_at": FROZEN_AT,
        "freeze_basis": "The exact elaborated statement and bounded immutable anchor audit determine the faithful-action, injectivity, chosen-left-inverse, range-equivalence, regular-specialization, source, provenance, trust, documentation, and workflow obligations. Eligibility is architectural and was fixed without accepting candidate closure.",
        "frozen_against_statement_sha256": statement_hash,
        "frozen_against_anchor_audit_sha256": anchor_hash,
        "root_obligation_id": f"{PREFIX}-ROOT",
        "denominator_sha256": denominator,
        "frozen_denominators": {
            "inventory": ids,
            "required_machine": [o["obligation_id"] for o in obligations if o["machine_eligibility"] == "required"],
            "required_human_source": [o["obligation_id"] for o in obligations if o["human_source_eligibility"] == "required"],
            "required_readable": ids,
            "informational_overlays": [o["obligation_id"] for o in obligations if o["machine_eligibility"] == "informational"],
            "required_unique_logical_leaves": [f"{PREFIX}-L-POINTWISE", f"{PREFIX}-L-REGULAR-FAITHFUL", f"{PREFIX}-C-LEFT-INVERSE"],
            "required_interface_transport": [f"{PREFIX}-S-TRANSPORT", f"{PREFIX}-N-REGULAR", f"{PREFIX}-T-ASSEMBLE"],
        },
        "layer_applicability": {
            "S_statement_foundation": {"state": "required", "obligation_ids": [f"{PREFIX}-S-EXACT", f"{PREFIX}-S-DOMAIN", f"{PREFIX}-S-BOUNDARY", f"{PREFIX}-S-TRANSPORT", f"{PREFIX}-S-FOUNDATION"]},
            "N_normalization": {"state": "required", "obligation_ids": [f"{PREFIX}-N-REGULAR"]},
            "B_mathematical_branch": {"state": "not_applicable_pending_independent_approval", "reason": "The construction is uniform for every group; trivial, finite, and infinite carriers are statement boundaries but induce no proof case split.", "reviewer": "unassigned independent group-theory reviewer"},
            "C_construction": {"state": "required", "obligation_ids": [f"{PREFIX}-C-PERM-HOM", f"{PREFIX}-C-LEFT-INVERSE", f"{PREFIX}-C-MRANGE-EQUIV"]},
            "L_core_lemma": {"state": "required", "obligation_ids": [f"{PREFIX}-L-POINTWISE", f"{PREFIX}-L-REGULAR-FAITHFUL", f"{PREFIX}-L-INJECTIVE"]},
            "X_external_computation": {"state": "required_external_boundary_and_not_applicable_computation_pending_independent_approval", "reason": "Pinned imports, terminal bodies, provenance, trust, source, documentation, and workflow are material. No finite computation, automation oracle, certificate, or experimental result occurs.", "obligation_ids": [f"{PREFIX}-X-UPSTREAM", f"{PREFIX}-X-SOURCE", f"{PREFIX}-X-PROVENANCE", f"{PREFIX}-X-TRUST", f"{PREFIX}-X-DOCUMENTATION", f"{PREFIX}-X-WORKFLOW"], "reviewer": "unassigned independent Lean/TCB reviewer"},
            "T_terminal": {"state": "required", "obligation_ids": [f"{PREFIX}-T-GENERAL", f"{PREFIX}-T-ASSEMBLE", f"{PREFIX}-ROOT"]},
        },
        "deduplication_policy": "The direct pinned Cayley declaration owns one terminal body. MonoidHom.ofInjective and teaching wrappers are component or alias routes and cannot add root or body credit. Statement transports and presentation nodes are informational overlays.",
        "delta_policy": "Any target correction, split, merge, exclusion, eligibility, risk, or terminal-body-identity change requires registry v2 with an append-only old/new ID delta; v1 denominators remain reportable.",
        "append_only_delta": [],
        "obligations": obligations,
        "status_observed_after_freeze": {
            "checked_conditional_interfaces": [f"{PREFIX}-L-INJECTIVE", f"{PREFIX}-T-GENERAL", f"{PREFIX}-N-REGULAR", f"{PREFIX}-T-ASSEMBLE", f"{PREFIX}-ROOT"],
            "audited_candidate_obligation": f"{PREFIX}-X-UPSTREAM",
            "audited_candidate_classification": "M0-W_candidate_pending_proof_phase_and_master_acceptance",
            "accepted_closed_obligations": [],
            "root_machine_debt": "M3",
        },
        "status_boundary": "Registry scope and denominators only. The exact candidate is not installed or accepted; H0, root M0, R0, audit completion, validation, release, and theorem completion remain open.",
    }

    graph_names = ("proof", "refinement", "provenance", "evidence", "trust", "documentation", "workflow")
    graphs = {
        name: {"edges": [], "out": {oid: [] for oid in ids}, "in": {oid: [] for oid in ids}}
        for name in graph_names
    }

    def add_edge(graph: str, edge_id: str, edge_type: str, src: str, dst: str, reciprocal: str | None = None) -> None:
        edge = {"edge_id": edge_id, "type": edge_type, "from": src, "to": dst}
        if reciprocal is not None:
            edge["reciprocal_edge_id"] = reciprocal
        graphs[graph]["edges"].append(edge)
        graphs[graph]["out"][src].append(edge_id)
        graphs[graph]["in"][dst].append(edge_id)

    proof_pairs = [
        (f"{PREFIX}-ROOT", f"{PREFIX}-T-ASSEMBLE"),
        (f"{PREFIX}-T-ASSEMBLE", f"{PREFIX}-N-REGULAR"),
        (f"{PREFIX}-T-ASSEMBLE", f"{PREFIX}-T-GENERAL"),
        (f"{PREFIX}-N-REGULAR", f"{PREFIX}-L-REGULAR-FAITHFUL"),
        (f"{PREFIX}-T-GENERAL", f"{PREFIX}-L-INJECTIVE"),
        (f"{PREFIX}-T-GENERAL", f"{PREFIX}-C-PERM-HOM"),
        (f"{PREFIX}-T-GENERAL", f"{PREFIX}-C-LEFT-INVERSE"),
        (f"{PREFIX}-T-GENERAL", f"{PREFIX}-C-MRANGE-EQUIV"),
        (f"{PREFIX}-T-GENERAL", f"{PREFIX}-N-MRANGE-RANGE"),
        (f"{PREFIX}-L-INJECTIVE", f"{PREFIX}-L-POINTWISE"),
    ]
    for index, (parent, child) in enumerate(proof_pairs, 1):
        req = f"P{index:02d}-REQ"
        comp = f"P{index:02d}-COMP"
        add_edge("proof", req, "proof_requires", parent, child, comp)
        add_edge("proof", comp, "composes", child, parent, req)

    refinement_pairs = [
        (f"{PREFIX}-ROOT", f"{PREFIX}-S-EXACT"),
        (f"{PREFIX}-ROOT", f"{PREFIX}-S-DOMAIN"),
        (f"{PREFIX}-ROOT", f"{PREFIX}-S-BOUNDARY"),
        (f"{PREFIX}-ROOT", f"{PREFIX}-S-TRANSPORT"),
        (f"{PREFIX}-ROOT", f"{PREFIX}-S-FOUNDATION"),
    ]
    for index, (parent, child) in enumerate(refinement_pairs, 1):
        add_edge("refinement", f"R{index:02d}", "expository_decomposition", parent, child)

    provenance_pairs = [
        (f"{PREFIX}-X-SOURCE", f"{PREFIX}-ROOT", "source_map"),
        (f"{PREFIX}-X-UPSTREAM", f"{PREFIX}-T-GENERAL", "provenance_of"),
        (f"{PREFIX}-X-PROVENANCE", f"{PREFIX}-T-GENERAL", "provenance_of"),
        (f"{PREFIX}-X-PROVENANCE", f"{PREFIX}-L-INJECTIVE", "provenance_of"),
        (f"{PREFIX}-X-PROVENANCE", f"{PREFIX}-C-MRANGE-EQUIV", "provenance_of"),
    ]
    for index, (src, dst, edge_type) in enumerate(provenance_pairs, 1):
        add_edge("provenance", f"V{index:02d}", edge_type, src, dst)

    for index, src in enumerate((f"{PREFIX}-ROOT", f"{PREFIX}-T-GENERAL", f"{PREFIX}-L-INJECTIVE", f"{PREFIX}-C-MRANGE-EQUIV"), 1):
        add_edge("trust", f"T{index:02d}", "trusts", src, f"{PREFIX}-X-TRUST")
    add_edge("trust", "T05", "trusts", f"{PREFIX}-X-TRUST", f"{PREFIX}-S-FOUNDATION")

    for index, src in enumerate(ids, 1):
        if src != f"{PREFIX}-X-DOCUMENTATION":
            add_edge("documentation", f"D{index:02d}", "documents", f"{PREFIX}-X-DOCUMENTATION", src)

    workflow_dependencies = [
        f"{PREFIX}-T-GENERAL",
        f"{PREFIX}-X-SOURCE",
        f"{PREFIX}-X-PROVENANCE",
        f"{PREFIX}-X-TRUST",
        f"{PREFIX}-X-DOCUMENTATION",
    ]
    for index, dependency in enumerate(workflow_dependencies, 1):
        add_edge("workflow", f"W{index:02d}", "workflow_depends_on", f"{PREFIX}-X-WORKFLOW", dependency)

    bundle = {
        "schema_version": "stage1-typed-graphs/1.0",
        "item_id": ITEM_ID,
        "theorem_id": THEOREM_ID,
        "registry_id": registry["registry_id"],
        "registry_denominator_sha256": denominator,
        "frozen_against_execution_dag_sha256": sha256(execution_dag_path),
        "local_task_dag_projection_sha256": sha256(HERE / "task-dag.json"),
        "root_node_id": f"{PREFIX}-ROOT",
        "edge_direction": "proof_requires is parent-to-child and composes child-to-parent; source/provenance/evidence/documentation object-to-subject; trusts subject-to-trust-boundary; workflow dependent-to-prerequisite. Non-proof graphs grant no proof credit.",
        "nodes": nodes,
        "graphs": graphs,
        "evidence_endpoint_policy": "Evidence receipts are external typed objects, not canonical obligations. The evidence graph remains empty in this freeze; node evidence_ids bind later content-addressed receipts.",
        "composition_certificates": [
            {"certificate_id": "M0063-CERT-INJECTIVITY", "declaration": "Stage1Instances.THM_M_0063.ObligationTree.genericInjectivity_of_pointwiseFaithfulness", "parent_id": f"{PREFIX}-L-INJECTIVE", "required_child_ids": [f"{PREFIX}-L-POINTWISE"], "conditional": True, "accepted": False},
            {"certificate_id": "M0063-CERT-MRANGE-RANGE", "declaration": "Stage1Instances.THM_M_0063.ObligationTree.mrangeToRangeTransport", "parent_id": f"{PREFIX}-N-MRANGE-RANGE", "required_child_ids": [], "conditional": False, "accepted": False},
            {"certificate_id": "M0063-CERT-GENERAL", "declaration": "Stage1Instances.THM_M_0063.ObligationTree.generalPackage_of_components", "parent_id": f"{PREFIX}-T-GENERAL", "required_child_ids": [f"{PREFIX}-L-INJECTIVE", f"{PREFIX}-C-PERM-HOM", f"{PREFIX}-C-LEFT-INVERSE", f"{PREFIX}-C-MRANGE-EQUIV", f"{PREFIX}-N-MRANGE-RANGE"], "conditional": True, "accepted": False},
            {"certificate_id": "M0063-CERT-REGULAR", "declaration": "Stage1Instances.THM_M_0063.ObligationTree.exactTarget_of_generalFaithfulAction", "parent_id": f"{PREFIX}-N-REGULAR", "required_child_ids": [f"{PREFIX}-L-REGULAR-FAITHFUL"], "conditional": True, "accepted": False, "modeling_note": "This local interface consumes regular-action faithfulness but still proves only the implication from an explicit generalized package to the exact target."},
            {"certificate_id": "M0063-CERT-ASSEMBLE", "declaration": "Stage1Instances.THM_M_0063.ObligationTree.exactAssembly_of_components", "parent_id": f"{PREFIX}-T-ASSEMBLE", "required_child_ids": [f"{PREFIX}-N-REGULAR", f"{PREFIX}-T-GENERAL"], "conditional": True, "accepted": False},
            {"certificate_id": "M0063-CERT-ROOT", "declaration": "Stage1Instances.THM_M_0063.ObligationTree.root_of_exactAssembly", "parent_id": f"{PREFIX}-ROOT", "required_child_ids": [f"{PREFIX}-T-ASSEMBLE"], "conditional": True, "accepted": False},
        ],
        "closure_boundary": {
            "root_closed": False,
            "root_machine_classification": "M3",
            "accepted_closed_obligations": [],
            "checked_conditional_interfaces": [f"{PREFIX}-L-INJECTIVE", f"{PREFIX}-T-GENERAL", f"{PREFIX}-N-REGULAR", f"{PREFIX}-T-ASSEMBLE", f"{PREFIX}-ROOT"],
            "remaining_root_cut_set": [f"{PREFIX}-C-PERM-HOM", f"{PREFIX}-L-POINTWISE", f"{PREFIX}-L-REGULAR-FAITHFUL", f"{PREFIX}-C-LEFT-INVERSE", f"{PREFIX}-C-MRANGE-EQUIV", f"{PREFIX}-N-MRANGE-RANGE"],
            "remaining_root_critical_nonproof_gates": [f"{PREFIX}-S-FOUNDATION", f"{PREFIX}-X-SOURCE", f"{PREFIX}-X-PROVENANCE", f"{PREFIX}-X-TRUST", f"{PREFIX}-X-DOCUMENTATION", f"{PREFIX}-X-WORKFLOW"],
            "audit_complete": False,
            "theorem_complete": False,
            "reason": "The exact pinned candidate is inventoried, but proof-node acceptance, full provenance/trust, H0 source mapping, R0 reconstruction, validation, release, and master acceptance are later gates.",
        },
    }

    task_nodes = [
        {"task_id": task["id"], "phase": task["phase"], "layer": task["layer"]}
        for task in authoritative_tasks
    ]
    task_edges = [
        {"edge_id": f"TASK-{index:02d}", "type": "workflow_depends_on", "from": task["id"], "to": dependency}
        for index, task in enumerate(authoritative_tasks, 1)
        for dependency in task["depends_on"]
    ]
    bundle["workflow_task_graph"] = {
        "authority": "Docs/Stage1_Execution_DAG_rev-5.6.json",
        "authority_sha256": sha256(execution_dag_path),
        "local_projection_boundary": "task-dag.json omits the intake task and remains an open planned projection; it is hashed but does not override the authoritative seven-item workflow graph.",
        "nodes": task_nodes,
        "edges": task_edges,
        "task_obligation_links": [
            {"task_id": ITEM_ID, "obligation_id": oid} for oid in ids
        ] + [
            {"task_id": "S56-M-0063-PROOF", "obligation_id": oid}
            for oid in registry["frozen_denominators"]["required_machine"]
        ] + [
            {"task_id": task, "obligation_id": oid}
            for task in ("S56-M-0063-VALIDATION", "S56-M-0063-RELEASE")
            for oid in (f"{PREFIX}-S-FOUNDATION", f"{PREFIX}-X-SOURCE", f"{PREFIX}-X-PROVENANCE", f"{PREFIX}-X-TRUST", f"{PREFIX}-X-DOCUMENTATION", f"{PREFIX}-X-WORKFLOW")
        ],
    }

    recipes = []
    for oid in ids:
        recipes.append({
            "recipe_id": "VAL-" + oid,
            "cwd": ".",
            "argv": ["python3", "-B", "Stage1_Instances/THM-M-0063/check_obligation_tree.py"],
            "env_allowlist": {},
            "timeout_seconds": 180,
            "network_policy": "denied",
            "expected_exit": 0,
            "expected_outputs": [{"path_or_stream": "stdout", "semantic_hash_policy": "contains PASS THM-M-0063 obligation tree"}],
            "covered_obligation_ids": [oid],
            "covered_declarations": [],
            "coverage_semantics": "provisional_interface_and_architecture_validation" if oid not in {f"{PREFIX}-S-FOUNDATION", f"{PREFIX}-X-SOURCE", f"{PREFIX}-X-PROVENANCE", f"{PREFIX}-X-TRUST", f"{PREFIX}-X-DOCUMENTATION", f"{PREFIX}-X-WORKFLOW"} else "open_state_classification_only",
            "closure_credit": False,
        })
    recipes.extend([
        {
            "recipe_id": "S56-M-0063-OBLIGATION-TREE-GENERATOR-CHECK",
            "cwd": ".",
            "argv": ["python3", "-B", "Stage1_Instances/THM-M-0063/build_obligation_artifacts.py", "--check"],
            "env_allowlist": {},
            "timeout_seconds": 60,
            "network_policy": "denied",
            "expected_exit": 0,
            "expected_outputs": [{"path_or_stream": "stdout", "semantic_hash_policy": "reports deterministic equality for obligation-registry.json, typed-graphs.json, and validation-specs.json"}],
            "covered_obligation_ids": ids,
            "covered_declarations": [], "coverage_semantics": "generator_drift_check", "closure_credit": False,
        },
        {
            "recipe_id": "S56-M-0063-OBLIGATION-TREE-STRUCTURE",
            "cwd": ".",
            "argv": ["python3", "-B", "Stage1_Instances/THM-M-0063/check_obligation_tree.py"],
            "env_allowlist": {},
            "timeout_seconds": 60,
            "network_policy": "denied",
            "expected_exit": 0,
            "expected_outputs": [{"path_or_stream": "stdout", "semantic_hash_policy": "reports 22 obligations, all seven typed graphs plus the seven-task workflow DAG, reciprocal proof edges, the frozen denominator, and an open M3 root"}],
            "covered_obligation_ids": ids,
            "covered_declarations": [], "coverage_semantics": "whole_bundle_structure_check", "closure_credit": False,
        },
        {
            "recipe_id": "S56-M-0063-OBLIGATION-TREE-LEAN",
            "cwd": ".",
            "argv": ["python3", "-B", "Stage1_Instances/THM-M-0063/check_obligation_tree.py"],
            "env_allowlist": {},
            "timeout_seconds": 180,
            "network_policy": "denied",
            "expected_exit": 0,
            "expected_outputs": [{"path_or_stream": "stdout", "semantic_hash_policy": "reports Lean output sha256 after compiling Statement.lean to a temporary olean and checking ObligationTree.lean against the actual canonical declaration"}],
            "covered_obligation_ids": [f"{PREFIX}-ROOT", f"{PREFIX}-N-REGULAR", f"{PREFIX}-L-POINTWISE", f"{PREFIX}-L-REGULAR-FAITHFUL", f"{PREFIX}-L-INJECTIVE", f"{PREFIX}-C-PERM-HOM", f"{PREFIX}-C-LEFT-INVERSE", f"{PREFIX}-C-MRANGE-EQUIV", f"{PREFIX}-N-MRANGE-RANGE", f"{PREFIX}-T-GENERAL", f"{PREFIX}-T-ASSEMBLE"],
            "covered_declarations": ["Stage1Instances.THM_M_0063.ObligationTree.genericInjectivity_of_pointwiseFaithfulness", "Stage1Instances.THM_M_0063.ObligationTree.mrangeToRangeTransport", "Stage1Instances.THM_M_0063.ObligationTree.generalPackage_of_components", "Stage1Instances.THM_M_0063.ObligationTree.exactTarget_of_generalFaithfulAction", "Stage1Instances.THM_M_0063.ObligationTree.exactAssembly_of_components", "Stage1Instances.THM_M_0063.ObligationTree.root_of_exactAssembly"],
            "coverage_semantics": "conditional_composition_and_actual_root_identity_only", "closure_credit": False,
        },
    ])
    specs = {
        "schema_version": "stage1-validation-specs/1.0",
        "item_id": ITEM_ID,
        "theorem_id": THEOREM_ID,
        "recipes": recipes,
    }
    return registry, bundle, specs


def serialized(value: dict) -> str:
    return json.dumps(value, ensure_ascii=True, indent=2) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true", help="write deterministic generated artifacts")
    mode.add_argument("--check", action="store_true", help="verify generated artifacts byte-for-byte")
    args = parser.parse_args()
    artifacts = dict(zip(("obligation-registry.json", "typed-graphs.json", "validation-specs.json"), build()))
    if args.write:
        for name, value in artifacts.items():
            (HERE / name).write_text(serialized(value))
        registry, bundle, _ = artifacts.values()
        edge_count = sum(len(graph["edges"]) for graph in bundle["graphs"].values())
        print(f"wrote {len(registry['obligations'])} obligations and {edge_count} typed edges")
        print(registry["denominator_sha256"])
        return
    for name, value in artifacts.items():
        assert (HERE / name).read_text() == serialized(value), f"generated artifact drift: {name}"
    registry, bundle, _ = artifacts.values()
    edge_count = sum(len(graph["edges"]) for graph in bundle["graphs"].values())
    print(f"PASS deterministic artifacts: {len(registry['obligations'])} obligations, {edge_count} typed edges")
    print(f"registry denominator sha256: {registry['denominator_sha256']}")


if __name__ == "__main__":
    main()
