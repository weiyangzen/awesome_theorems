#!/usr/bin/env python3
"""Build or verify the frozen THM-M-0079 obligation registry and graph bundle."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ITEM = "S56-M-0079-OBLIGATION_TREE"
THEOREM = "THM-M-0079"
PREFIX = "M0079"
ROOT_EXPRESSION = "bb109f77dcbd6884a4ac90b32230cc213c08f19df6bc797ad04afac1a10da553"
MATHLIB = "8a178386ffc0f5fef0b77738bb5449d50efeea95"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def row(suffix: str, kind: str, human: str, formal: str, output: str, risk: str,
        *, required: bool = True, source: bool = True, body: str | None = None,
        budget: int = 30, premises: str = "The exact typed incoming premises.",
        inference: str | None = None, anchors: list[str] | None = None) -> dict:
    canonical_kind = {
        "normalization": "reduction", "core_lemma": "lemma",
        "bridge": "terminal", "certificate": "terminal",
    }.get(kind, kind)
    return {
        "id": f"{PREFIX}-{suffix}", "kind": canonical_kind, "human": human, "formal": formal,
        "output": output, "risk": risk, "required": required, "source": source,
        "body": body, "budget": budget, "premises": premises,
        "inference": inference or human, "anchors": anchors or [formal],
    }


# The central action-groupoid and spanning-tree bodies are intentionally expanded. A one-line call
# to endIsFreeOfConnectedFree would hide most of the Nielsen-Schreier proof architecture.
ROWS = [
    row("ROOT", "root", "Every subgroup of every universe-polymorphic free group is free.",
        "Stage1Instances.THM_M_0079.NielsenSchreierTarget", "The exact canonical proposition.",
        "critical", budget=8, premises="M0079-T-ASSEMBLE in the exact statement context."),
    row("S-EXACT", "definition", "Freeze G, Group G, IsFreeGroup G, arbitrary H : Subgroup G, and IsFreeGroup H.",
        "Stage1Instances.THM_M_0079.NielsenSchreierTarget", "The expression-fingerprinted statement interface.",
        "critical", required=False, source=False, budget=8),
    row("S-DOMAIN", "definition", "Fix the universe, binder order, inherited subgroup group, and same-universe free basis.",
        "statement.json#domain_and_universes", "The exact universe and typeclass contract.", "high",
        required=False, source=False, budget=10),
    row("S-BOUNDARY", "branch", "Include bottom, top, trivial ambient, and infinite-rank subgroup cases without a proof case split.",
        "Statement.trivialAmbientBottomBoundary; genericTopBoundary; infiniteRankBoundary",
        "The complete degenerate-case policy.", "high", required=False, source=False, budget=12),
    row("S-LITERAL-TRANSPORT", "transport", "Relate the generic target bidirectionally to subgroups of a literal FreeGroup X.",
        "Stage1Instances.THM_M_0079.nielsenSchreierTarget_iff_literalFreeGroupTarget",
        "A checked equivalence with no duplicate root credit.", "high", required=False, source=False,
        body="repo:Statement.lean#nielsenSchreierTarget_iff_literalFreeGroupTarget", budget=18),
    row("S-BASIS-TRANSPORT", "transport", "Expand IsFreeGroup H to existence of a same-universe FreeGroupBasis.",
        "Stage1Instances.THM_M_0079.nielsenSchreierTarget_iff_basisExistenceTarget",
        "A checked definition-level equivalence.", "high", required=False, source=False,
        body="repo:Statement.lean#nielsenSchreierTarget_iff_basisExistenceTarget", budget=12),
    row("S-FOUNDATION", "certificate", "Account for propext, Classical.choice, Quot.sound, kernel, and symbolic computation policy.",
        "planned transitive axiom and TCB report", "A reviewed foundation boundary, not a proof premise.",
        "critical", source=False, budget=60),
    row("L-QUOTIENT-PRETRANSITIVE", "core_lemma", "The left action of G on G/H is pretransitive.",
        "forall (G : Type u) [Group G] (H : Subgroup G), MulAction.IsPretransitive G (G ⧸ H)", "Any two quotient vertices differ by a group action.",
        "high", body=f"mathlib:{MATHLIB}:MulAction.isPretransitive_quotient", budget=24),
    row("C-QUOTIENT-NONEMPTY", "construction", "Choose the identity coset as an object of G/H.",
        "forall (G : Type u) [Group G] (H : Subgroup G), Nonempty (G ⧸ H)", "A nonempty quotient action carrier.", "normal",
        body=f"mathlib:{MATHLIB}:Mathlib/GroupTheory/Coset/Defs.lean:194:QuotientGroup.instInhabitedQuotient", budget=8),
    row("C-ACTION-CONNECTED", "construction", "Build a connected action groupoid from a pretransitive nonempty action.",
        "Stage1Instances.THM_M_0079.ObligationTree.QuotientActionConnected",
        "IsConnected (ActionCategory G (G ⧸ H)).", "critical",
        body=f"mathlib:{MATHLIB}:Mathlib/CategoryTheory/Action.lean:128:ActionCategory.connected-instance", budget=12,
        premises="M0079-L-QUOTIENT-PRETRANSITIVE, M0079-C-QUOTIENT-NONEMPTY, and the pinned generic ActionCategory connectedness constructor."),
    row("C-ACTION-GENERATORS", "construction", "Define action-groupoid generators from ambient free generators and endpoint action equations.",
        "planned-signature-v1: for G, A, Group G, IsFreeGroup G, and MulAction G A, return the generating quiver whose a-to-b arrows are ambient free generators e with IsFreeGroup.of e acting on a as b, plus their interpretation in ActionCategory G A",
        "The generating quiver and its interpretation functor.", "critical",
        body=f"mathlib:{MATHLIB}:IsFreeGroupoid.actionGroupoidIsFree", budget=30),
    row("C-SEMIDIRECT-LABELLING", "construction", "Encode a target labelling as a semidirect-product label on ambient free generators.",
        "planned-signature-v1: for G, A, X, their group/action structures, and a labelling f of the frozen action generator quiver in X, return f' : IsFreeGroup.Generators G → SemidirectProduct (A → X) G with right component IsFreeGroup.of",
        "A labelling into (A → X) semidirect G.",
        "critical", body=f"mathlib:{MATHLIB}:IsFreeGroupoid.actionGroupoidIsFree", budget=28),
    row("L-AMBIENT-UNIQUE-LIFT", "core_lemma", "Extend the semidirect labelling uniquely using the ambient free-group universal property.",
        "planned-signature-v1: for a semidirect labelling f', return exists unique F' : G →* SemidirectProduct (A → X) G such that every IsFreeGroup.of generator maps to f'",
        "A unique group homomorphism F' extending all generator labels.",
        "critical", body=f"mathlib:{MATHLIB}:IsFreeGroup.unique_lift", budget=50),
    row("C-CURRY-UNCURRY", "construction", "Convert F' into an action-groupoid functor and prove the projection compatibility.",
        "planned-signature-v1: an F' : G →* SemidirectProduct (A → X) G whose right projection is identity yields ActionCategory.uncurry F' and ActionCategory.curry recovers F'",
        "A functor whose generator maps match the input labelling.",
        "critical", body=f"mathlib:{MATHLIB}:ActionCategory.uncurry", budget=60),
    row("L-FUNCTOR-UNIQUENESS", "core_lemma", "Prove uniqueness of the action-groupoid lift by curry equality and functor extensionality.",
        "planned-signature-v1: for functors F and E from ActionCategory G A to SingleObj X, equality of ActionCategory.curry F and ActionCategory.curry E implies F = E",
        "The uniqueness clause of the free-groupoid universal property.", "critical",
        body=f"mathlib:{MATHLIB}:IsFreeGroupoid.actionGroupoidIsFree", budget=60),
    row("C-ACTION-GROUPOID-FREE", "construction", "Assemble the generators, lift, agreement, and uniqueness into freeness of the action groupoid.",
        "IsFreeGroupoid.actionGroupoidIsFree", "IsFreeGroupoid (ActionCategory G (G ⧸ H)).",
        "critical", body=f"mathlib:{MATHLIB}:IsFreeGroupoid.actionGroupoidIsFree", budget=15,
        premises="M0079-C-ACTION-GENERATORS, M0079-C-SEMIDIRECT-LABELLING, M0079-L-AMBIENT-UNIQUE-LIFT, M0079-C-CURRY-UNCURRY, and M0079-L-FUNCTOR-UNIQUENESS."),
    row("L-HOM-PATH", "core_lemma", "Turn existence of a groupoid morphism into a path in the generating quiver.",
        "forall {G} [Groupoid G] [IsFreeGroupoid G] {a b : G}, Nonempty (a ⟶ b) → Nonempty (Path (symgen a) (symgen b))",
        "A nonempty generating-quiver path.", "critical",
        body=f"mathlib:{MATHLIB}:IsFreeGroupoid.path_nonempty_of_hom", budget=55),
    row("C-ROOTED-CONNECTED", "construction", "Use groupoid connectedness and hom-to-path to root the generating quiver.",
        "IsFreeGroupoid.generators_connected", "RootedConnected at the selected vertex.", "critical",
        body=f"mathlib:{MATHLIB}:IsFreeGroupoid.generators_connected", budget=18,
        premises="M0079-L-HOM-PATH and the connected action groupoid."),
    row("C-GEODESIC-TREE", "construction", "Choose the geodesic subtree of the rooted generating quiver and its arborescence invariant.",
        "Quiver.geodesicSubtree", "A spanning arborescence rooted at the selected quotient vertex.",
        "critical", body=f"mathlib:{MATHLIB}:Quiver.geodesicSubtree", budget=45,
        premises="M0079-C-ROOTED-CONNECTED."),
    row("L-GEODESIC-ARBORESCENCE", "core_lemma", "Prove that the chosen geodesic subtree carries the required arborescence instance.",
        "Quiver.geodesicArborescence", "Arborescence (geodesicSubtree root).",
        "critical", body=f"mathlib:{MATHLIB}:Quiver.geodesicArborescence", budget=40,
        premises="M0079-C-ROOTED-CONNECTED."),
    row("C-TREE-PATHS", "construction", "Compose a unique tree path into a canonical groupoid morphism from the root.",
        "planned-signature-v1: for free groupoid G and spanning arborescence T, every vertex a has treeHom T a : root'(T) ⟶ a, obtained by composing the unique tree path",
        "Canonical root-to-vertex morphisms with root identity.", "high",
        body=f"mathlib:{MATHLIB}:IsFreeGroupoid.SpanningTree.treeHom", budget=50),
    row("C-TREE-LOOPS", "construction", "Conjugate each groupoid morphism along tree paths to obtain a loop at the root.",
        "IsFreeGroupoid.SpanningTree.loopOfHom", "A root endomorphism for every arrow.", "critical",
        body=f"mathlib:{MATHLIB}:IsFreeGroupoid.SpanningTree.loopOfHom", budget=25,
        premises="M0079-C-TREE-PATHS."),
    row("L-TREE-EDGE-IDENTITY", "core_lemma", "Show a generator edge lying in the tree produces the identity loop.",
        "IsFreeGroupoid.SpanningTree.loopOfHom_eq_id", "Tree edges contribute no free generator.",
        "critical", body=f"mathlib:{MATHLIB}:IsFreeGroupoid.SpanningTree.loopOfHom_eq_id", budget=45,
        premises="M0079-C-TREE-PATHS and M0079-C-TREE-LOOPS."),
    row("C-FUNCTOR-END-HOM", "construction", "Extend a monoid homomorphism on the root end group to a functor on the groupoid.",
        "IsFreeGroupoid.SpanningTree.functorOfMonoidHom", "A functor respecting identities and composition.",
        "critical", body=f"mathlib:{MATHLIB}:IsFreeGroupoid.SpanningTree.functorOfMonoidHom", budget=45,
        premises="M0079-C-TREE-LOOPS."),
    row("C-COMPLEMENT-GENERATORS", "construction", "Use generating arrows outside the tree as a free basis for the root end group.",
        "IsFreeGroupoid.SpanningTree.endIsFree#complement-generators",
        "The generator set and universal-property labelling for the root end group.", "critical",
        body=f"mathlib:{MATHLIB}:IsFreeGroupoid.SpanningTree.endIsFree", budget=75,
        premises="The selected spanning tree and the complement of its symmetrified wide subquiver."),
    row("L-SPANNING-END-FREE", "core_lemma", "Prove the root end group of a free groupoid with spanning tree is free.",
        "IsFreeGroupoid.SpanningTree.endIsFree", "IsFreeGroup (End root).", "critical",
        body=f"mathlib:{MATHLIB}:IsFreeGroupoid.SpanningTree.endIsFree", budget=25,
        premises="M0079-C-TREE-PATHS, M0079-C-TREE-LOOPS, M0079-L-TREE-EDGE-IDENTITY, M0079-C-FUNCTOR-END-HOM, and M0079-C-COMPLEMENT-GENERATORS."),
    row("L-CONNECTED-END-FREE", "core_lemma", "Apply the geodesic spanning-tree theorem at the identity-coset vertex of the connected free action groupoid.",
        "IsFreeGroupoid.endIsFreeOfConnectedFree", "Freeness of any selected vertex group in a connected free groupoid.",
        "critical", body=f"mathlib:{MATHLIB}:IsFreeGroupoid.endIsFreeOfConnectedFree", budget=18,
        premises="M0079-C-GEODESIC-TREE and M0079-L-SPANNING-END-FREE."),
    row("N-QUOTIENT-END-FREE", "normalization", "Specialize connected-free-groupoid end freeness to the identity coset in the quotient action groupoid.",
        "Stage1Instances.THM_M_0079.ObligationTree.QuotientVertexEndFree",
        "Freeness of End at the identity-coset object.", "critical",
        body="repo:ObligationTree.lean#quotientVertexEndFree_of_components", budget=12,
        premises="M0079-C-ACTION-GROUPOID-FREE, M0079-C-ACTION-CONNECTED, and M0079-L-CONNECTED-END-FREE."),
    row("C-STABILIZER-END", "construction", "Identify the stabilizer of the identity coset with the end group of its action-groupoid object.",
        "forall (G : Type u) [Group G] (H : Subgroup G), MulAction.stabilizerSubmonoid G ((1 : G) : G ⧸ H) ≃* End (objEquiv G (G ⧸ H) 1)",
        "A multiplicative equivalence between stabilizer and End.",
        "high", body=f"mathlib:{MATHLIB}:ActionCategory.stabilizerIsoEnd", budget=20),
    row("L-QUOTIENT-STABILIZER", "core_lemma", "Identify the stabilizer of the identity coset with H.",
        "forall (G : Type u) [Group G] (H : Subgroup G), MulAction.stabilizer G ((1 : G) : G ⧸ H) = H",
        "Equality of the quotient-action stabilizer and H.",
        "critical", body=f"mathlib:{MATHLIB}:stabilizer_quotient", budget=35),
    row("C-END-SUBGROUP-EQUIV", "construction", "Compose stabilizer equivalences to identify the selected end group with H.",
        "ActionCategory.endMulEquivSubgroup", "End(identity coset) is multiplicatively equivalent to H.",
        "critical", body=f"mathlib:{MATHLIB}:ActionCategory.endMulEquivSubgroup", budget=12,
        premises="M0079-C-STABILIZER-END and M0079-L-QUOTIENT-STABILIZER."),
    row("T-MULEQUIV-FREENESS", "transport", "Transport a free basis along the exact end-to-subgroup multiplicative equivalence.",
        "forall (A B : Type u) [Group A] [Group B] [IsFreeGroup A], (A ≃* B) → IsFreeGroup B",
        "IsFreeGroup H from end-group freeness.", "critical",
        body=f"mathlib:{MATHLIB}:IsFreeGroup.ofMulEquiv", budget=30),
    row("T-ASSEMBLE", "terminal", "Compose end-group freeness, end-to-H equivalence, and freeness transport into the exact root.",
        "Stage1Instances.THM_M_0079.ObligationTree.exactAssembly_of_end_packages",
        "The binder-complete NielsenSchreierTarget.", "critical",
        body="repo:ObligationTree.lean#exactAssembly_of_end_packages", budget=10,
        premises="M0079-N-QUOTIENT-END-FREE, M0079-C-END-SUBGROUP-EQUIV, and M0079-T-MULEQUIV-FREENESS."),
    row("A-DIRECT", "bridge", "Bind the exact pinned subgroupIsFreeOfIsFree wrapper to the same terminal bodies without duplicate proof credit.",
        "subgroupIsFreeOfIsFree", "An audited M0-W candidate for the later proof phase.", "critical",
        required=False, body=f"mathlib:{MATHLIB}:subgroupIsFreeOfIsFree", budget=20),
    row("X-SOURCE", "terminal", "Map every mathematical node to primary human sources, assumptions, corrections, and definition transports.",
        "primary source crosswalk pending", "An independently reviewed H0 packet.", "high",
        required=False, budget=100),
    row("X-PROVENANCE", "certificate", "Close wrapper, body, declaration, revision, source-hash, origin, and license provenance transitively.",
        "planned transitive provenance packet", "Accepted provenance for every root-critical body.",
        "critical", required=False, source=False, budget=100),
    row("X-TRUST", "certificate", "Close transitive axioms, compiled artifacts, executables, TCB, and supply-chain trust.",
        "planned trust packet", "Accepted trust closure under the selected foundation profile.",
        "critical", required=False, source=False, budget=100),
    row("X-DOCUMENTATION", "terminal", "Provide a unique readable target for every required readable obligation.",
        "obligation-tree.md plus later reconstruction", "Stable reader paths and independent R0 decisions.",
        "high", required=False, source=False, budget=100),
    row("X-WORKFLOW", "terminal", "Bind obligation freeze, proof, validation, release, freshness, and revocation ordering.",
        "authoritative execution DAG and node receipts", "Dependency-legal execution state.",
        "critical", required=False, source=False, budget=40),
]

FIELDS = ("obligation_id", "statement_fingerprint", "kind", "root_relevant",
          "machine_eligibility", "human_source_eligibility", "readable_eligibility",
          "risk_class", "exclusion_reason", "terminal_proof_body_id")


def build() -> tuple[dict, dict, dict]:
    statement_hash = sha256(HERE / "Statement.lean")
    anchor_hash = sha256(HERE / "anchor-audit.json")
    execution_path = ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json"
    execution = json.loads(execution_path.read_text())
    tasks = [task for task in execution["items"] if task["theorem_id"] == THEOREM]
    assert len(tasks) == 7
    obligations, nodes = [], []
    ids = [entry["id"] for entry in ROWS]
    for entry in ROWS:
        oid = entry["id"]
        fingerprint = ("lean-expression-sha256:" + ROOT_EXPRESSION if oid in {f"{PREFIX}-ROOT", f"{PREFIX}-S-EXACT"}
                       else "planned-signature-v1:sha256:" + hashlib.sha256("\0".join((oid, entry["human"], entry["formal"], entry["output"])).encode()).hexdigest())
        obligations.append({
            "obligation_id": oid, "statement_fingerprint": fingerprint, "kind": entry["kind"],
            "root_relevant": True, "machine_eligibility": "required" if entry["required"] else "informational",
            "human_source_eligibility": "required" if entry["source"] else "not_applicable",
            "readable_eligibility": "required", "risk_class": entry["risk"],
            "exclusion_reason": (
                None if entry["required"]
                else "governance_assurance_overlay_no_mathematical_machine_denominator_credit"
                if "-X-" in oid
                else "deduplicated_exact_candidate_bridge_no_independent_machine_credit"
                if oid == f"{PREFIX}-A-DIRECT"
                else "typed_statement_overlay_no_independent_machine_credit"
            ),
            "terminal_proof_body_id": entry["body"],
        })
        premise_ids = re.findall(r"M0079-[A-Z][A-Z0-9-]*", entry["premises"])
        nodes.append({
            "node_id": f"{THEOREM}-{oid.removeprefix(PREFIX + '-')}", "obligation_id": oid,
            "kind": entry["kind"], "human_statement": entry["human"], "formal_target": entry["formal"],
            "output": entry["output"], "human_debt": "H1", "machine_debt": "M3",
            "readability_debt": "R4", "evidence_ids": [],
            "source_crosswalk_id": "source-statement-crosswalk.md#component-crosswalk" if entry["source"] else "not_applicable",
            "provenance_id": (
                "repo-local:" + entry["body"].removeprefix("repo:")
                if entry["body"] and entry["body"].startswith("repo:")
                else "anchor-audit.json#/candidates/1:proof-substrate-pending-node-specific-provenance"
                if entry["body"]
                else "none"
            ),
            "foundation_profile": "lean4-foundation-planned/1.0; transitive acceptance open",
            "tcb_profile": "lean4-mathlib-tcb-planned/1.0; Lean 4.29.0 + mathlib 8a178386; full closure open",
            "computation_record": "not_applicable_pending_independent_approval; symbolic kernel route with no solver, oracle, native evaluation, or unchecked certificate",
            "step_budget": entry["budget"],
            "semantic_step_ledger": {
                "premises": entry["premises"], "inference": entry["inference"], "output": entry["output"],
                "source_anchors": entry["anchors"], "outgoing_use": "Only typed outgoing graph edges may consume this exact output.",
                "steps": [{"step_id": oid + "-STEP-01", "premise_ids": premise_ids,
                           "inference": entry["inference"], "output": entry["output"],
                           "source_anchors": entry["anchors"],
                           "outgoing_use": "Supplies this node's exact typed output; no alias or wrapper earns duplicate credit."}],
            },
            "public_readable_target": f"Stage1_Instances/THM-M-0079/obligation-tree.md#{oid.lower()}",
            "validation_spec_id": "VAL-" + oid,
            "status_boundary": "Frozen architecture only; proof acceptance, H0, R0, full trust, AUDIT-Z, and theorem completion remain open.",
            "task_ids": [ITEM, "S56-M-0079-PROOF"],
            "owned_sources": ([entry["body"]] if entry["body"] else []) + [
                "Stage1_Instances/THM-M-0079/obligation-registry.json",
                "Stage1_Instances/THM-M-0079/typed-graphs.json",
                f"Stage1_Instances/THM-M-0079/obligation-tree.md#{oid.lower()}",
            ],
            "owner": "THM-M-0079 proof lane", "reviewer": "unassigned independent Stage1 reviewer",
            "validity": {"validated_at": None, "review_due": "before master acceptance",
                         "invalidation_inputs": ["Statement.lean", "anchor-audit.json", "registry", "graphs", "toolchain", "dependency pin", "assurance profile"],
                         "revocation_state": "open"},
        })
        nodes[-1]["semantic_step_ledger"]["ledger_state"] = (
            "semantic_architecture_step_frozen_not_R0_reconstruction"
        )
        nodes[-1]["semantic_step_ledger"]["budget_semantics"] = (
            "Architecture split threshold only, not a verified logical-step count; later R0 reconstruction must supply and independently review a substantive <=100-step ledger without changing the frozen obligation."
        )
    projection = [{key: item[key] for key in FIELDS} for item in obligations]
    denominator = hashlib.sha256(json.dumps(projection, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    required = [o["obligation_id"] for o in obligations if o["machine_eligibility"] == "required"]
    registry = {
        "schema_version": "stage1-obligation-registry/1.0", "item_id": ITEM, "theorem_id": THEOREM,
        "registry_id": "THM-M-0079-OBLIGATIONS-v1", "registry_version": 1,
        "freeze_date": "2026-07-13",
        "freeze_timestamp": None,
        "freeze_timestamp_boundary": "Exact freeze time was not captured; a date-only value is not promoted to a synthetic instant.",
        "freeze_basis": "The exact target and bounded anchor audit fix a quotient-action, free-action-groupoid, connected spanning-tree, end-group, stabilizer-equivalence, transport, source, trust, documentation, and workflow architecture before proof credit.",
        "frozen_against_statement_sha256": statement_hash, "frozen_against_anchor_audit_sha256": anchor_hash,
        "root_obligation_id": f"{PREFIX}-ROOT", "denominator_sha256": denominator,
        "frozen_denominators": {
            "inventory": ids, "required_machine": required,
            "required_human_source": [o["obligation_id"] for o in obligations if o["human_source_eligibility"] == "required"],
            "required_readable": ids,
            "informational_overlays": [o["obligation_id"] for o in obligations if o["machine_eligibility"] == "informational"],
            "required_unique_architecture_frontier": [],
            "required_interface_transport": [f"{PREFIX}-S-LITERAL-TRANSPORT", f"{PREFIX}-S-BASIS-TRANSPORT", f"{PREFIX}-C-END-SUBGROUP-EQUIV", f"{PREFIX}-T-ASSEMBLE"],
        },
        "layer_applicability": {
            "S_statement_foundation": {"state": "required", "obligation_ids": ids[1:7]},
            "N_normalization": {"state": "required", "obligation_ids": [f"{PREFIX}-L-QUOTIENT-PRETRANSITIVE", f"{PREFIX}-C-ACTION-CONNECTED", f"{PREFIX}-C-ROOTED-CONNECTED", f"{PREFIX}-N-QUOTIENT-END-FREE"]},
            "B_mathematical_branch": {"state": "not_applicable_pending_independent_approval", "reason": "The theorem-level route is uniform; checked boundary cases do not create proof branches. Internal source conditionals are represented in their owning construction ledgers.", "reviewer": "unassigned independent group-theory reviewer"},
            "C_construction": {"state": "required", "obligation_ids": [oid for oid in required if "-C-" in oid]},
            "L_core_lemma": {"state": "required", "obligation_ids": [oid for oid in required if "-L-" in oid]},
            "X_external_computation": {"state": "required_external_boundary_and_not_applicable_computation_pending_independent_approval", "reason": "Pinned bodies and TCB are material; no finite computation, oracle, or unchecked certificate is credited.", "obligation_ids": ids[-6:], "reviewer": "unassigned independent Lean/TCB reviewer"},
            "T_terminal": {"state": "required", "obligation_ids": [f"{PREFIX}-T-MULEQUIV-FREENESS", f"{PREFIX}-T-ASSEMBLE", f"{PREFIX}-ROOT"]},
        },
        "deduplication_policy": "subgroupIsFreeOfIsFree and the local root adapter share the audited endMulEquivSubgroup/ofMulEquiv terminal chain. Statement transports, wrappers, and presentation nodes cannot add semantic or proof-body credit.",
        "delta_policy": "Any statement, split, merge, eligibility, risk, exclusion, or body-identity change requires v2 plus an append-only delta; v1 denominators remain reportable.",
        "append_only_delta": [], "obligations": obligations,
        "status_observed_after_freeze": {"checked_conditional_interfaces": [f"{PREFIX}-C-ACTION-CONNECTED", f"{PREFIX}-N-QUOTIENT-END-FREE", f"{PREFIX}-C-END-SUBGROUP-EQUIV", f"{PREFIX}-T-ASSEMBLE", f"{PREFIX}-ROOT"], "audited_candidate_obligation": f"{PREFIX}-A-DIRECT", "audited_candidate_classification": "M0-W_candidate_pending_proof_phase_and_master_acceptance", "accepted_closed_obligations": [], "root_machine_debt": "M3"},
        "status_boundary": "Registry and denominators only. No candidate is installed or accepted; H0, root M0, R0, validation, release, AUDIT-Z, and theorem completion remain open.",
    }
    graph_names = ("proof", "refinement", "provenance", "evidence", "trust", "documentation", "workflow")
    graphs = {name: {"edges": [], "out": {oid: [] for oid in ids}, "in": {oid: [] for oid in ids}} for name in graph_names}
    def edge(graph: str, eid: str, kind: str, src: str, dst: str, reciprocal: str | None = None) -> None:
        value = {"edge_id": eid, "type": kind, "from": src, "to": dst}
        if reciprocal: value["reciprocal_edge_id"] = reciprocal
        graphs[graph]["edges"].append(value); graphs[graph]["out"][src].append(eid); graphs[graph]["in"][dst].append(eid)
    proof_pairs = [
        ("ROOT", "T-ASSEMBLE"), ("T-ASSEMBLE", "N-QUOTIENT-END-FREE"), ("T-ASSEMBLE", "C-END-SUBGROUP-EQUIV"), ("T-ASSEMBLE", "T-MULEQUIV-FREENESS"),
        ("N-QUOTIENT-END-FREE", "C-ACTION-GROUPOID-FREE"), ("N-QUOTIENT-END-FREE", "C-ACTION-CONNECTED"), ("N-QUOTIENT-END-FREE", "L-CONNECTED-END-FREE"),
        ("C-ACTION-CONNECTED", "L-QUOTIENT-PRETRANSITIVE"), ("C-ACTION-CONNECTED", "C-QUOTIENT-NONEMPTY"),
        ("C-ACTION-GROUPOID-FREE", "C-ACTION-GENERATORS"), ("C-ACTION-GROUPOID-FREE", "C-SEMIDIRECT-LABELLING"), ("C-ACTION-GROUPOID-FREE", "L-AMBIENT-UNIQUE-LIFT"), ("C-ACTION-GROUPOID-FREE", "C-CURRY-UNCURRY"), ("C-ACTION-GROUPOID-FREE", "L-FUNCTOR-UNIQUENESS"),
        ("C-ROOTED-CONNECTED", "L-HOM-PATH"), ("C-ROOTED-CONNECTED", "C-ACTION-CONNECTED"), ("C-ROOTED-CONNECTED", "C-ACTION-GROUPOID-FREE"),
        ("C-GEODESIC-TREE", "C-ROOTED-CONNECTED"), ("L-GEODESIC-ARBORESCENCE", "C-ROOTED-CONNECTED"),
        ("C-TREE-LOOPS", "C-TREE-PATHS"), ("L-TREE-EDGE-IDENTITY", "C-TREE-LOOPS"), ("C-FUNCTOR-END-HOM", "C-TREE-LOOPS"),
        ("L-SPANNING-END-FREE", "L-TREE-EDGE-IDENTITY"), ("L-SPANNING-END-FREE", "C-FUNCTOR-END-HOM"), ("L-SPANNING-END-FREE", "C-COMPLEMENT-GENERATORS"),
        ("L-CONNECTED-END-FREE", "C-GEODESIC-TREE"), ("L-CONNECTED-END-FREE", "L-GEODESIC-ARBORESCENCE"), ("L-CONNECTED-END-FREE", "L-SPANNING-END-FREE"),
        ("C-END-SUBGROUP-EQUIV", "C-STABILIZER-END"), ("C-END-SUBGROUP-EQUIV", "L-QUOTIENT-STABILIZER"),
    ]
    # Every ledger premise is an exact proof child. Context instances that are not separate
    # semantic claims stay in the formal target rather than becoming hidden graph dependencies.
    row_by_id = {entry["id"]: entry for entry in ROWS}
    child_suffixes: dict[str, list[str]] = {}
    for parent, child in proof_pairs:
        child_suffixes.setdefault(f"{PREFIX}-{parent}", []).append(f"{PREFIX}-{child}")
    for parent, child_ids in child_suffixes.items():
        entry = row_by_id[parent]
        entry["premises"] = ", ".join(child_ids) + "."
        node = next(node for node in nodes if node["obligation_id"] == parent)
        node["semantic_step_ledger"]["premises"] = entry["premises"]
        node["semantic_step_ledger"]["steps"][0]["premise_ids"] = child_ids
    for i, (parent, child) in enumerate(proof_pairs, 1):
        req, comp = f"P{i:02d}-REQ", f"P{i:02d}-COMP"
        edge("proof", req, "proof_requires", f"{PREFIX}-{parent}", f"{PREFIX}-{child}", comp)
        edge("proof", comp, "composes", f"{PREFIX}-{child}", f"{PREFIX}-{parent}", req)
    proof_parents = {f"{PREFIX}-{parent}" for parent, _ in proof_pairs}
    registry["frozen_denominators"]["required_unique_architecture_frontier"] = [
        oid for oid in required if oid not in proof_parents and oid != f"{PREFIX}-S-FOUNDATION"
    ]
    for i, child in enumerate(("S-EXACT", "S-DOMAIN", "S-BOUNDARY", "S-FOUNDATION"), 1):
        edge("refinement", f"R{i:02d}", "expository_decomposition", f"{PREFIX}-ROOT", f"{PREFIX}-{child}")
    edge("refinement", "R05-FWD", "transports", f"{PREFIX}-ROOT", f"{PREFIX}-S-LITERAL-TRANSPORT", "R05-BACK")
    edge("refinement", "R05-BACK", "equivalent_to", f"{PREFIX}-S-LITERAL-TRANSPORT", f"{PREFIX}-ROOT", "R05-FWD")
    edge("refinement", "R06-FWD", "transports", f"{PREFIX}-ROOT", f"{PREFIX}-S-BASIS-TRANSPORT", "R06-BACK")
    edge("refinement", "R06-BACK", "equivalent_to", f"{PREFIX}-S-BASIS-TRANSPORT", f"{PREFIX}-ROOT", "R06-FWD")
    provenance = [("X-SOURCE", "ROOT", "source_map"), ("A-DIRECT", "T-ASSEMBLE", "provenance_of")]
    provenance += [
        ("X-PROVENANCE", entry["id"].removeprefix(PREFIX + "-"), "provenance_of")
        for entry in ROWS
        if entry["body"] and entry["id"] not in {f"{PREFIX}-A-DIRECT"}
    ]
    for i, (src, dst, kind) in enumerate(provenance, 1): edge("provenance", f"V{i:02d}", kind, f"{PREFIX}-{src}", f"{PREFIX}-{dst}")
    for i, src in enumerate(("ROOT", "C-ACTION-GROUPOID-FREE", "L-SPANNING-END-FREE", "C-END-SUBGROUP-EQUIV", "T-MULEQUIV-FREENESS"), 1): edge("trust", f"T{i:02d}", "trusts", f"{PREFIX}-{src}", f"{PREFIX}-X-TRUST")
    edge("trust", "T06", "trusts", f"{PREFIX}-X-TRUST", f"{PREFIX}-S-FOUNDATION")
    for i, oid in enumerate(ids, 1):
        if oid != f"{PREFIX}-X-DOCUMENTATION": edge("documentation", f"D{i:02d}", "documents", f"{PREFIX}-X-DOCUMENTATION", oid)
    for i, dep in enumerate(("T-ASSEMBLE", "X-SOURCE", "X-PROVENANCE", "X-TRUST", "X-DOCUMENTATION"), 1): edge("workflow", f"W{i:02d}", "workflow_depends_on", f"{PREFIX}-X-WORKFLOW", f"{PREFIX}-{dep}")
    children: dict[str, list[str]] = {}
    for parent, child in proof_pairs: children.setdefault(f"{PREFIX}-{parent}", []).append(f"{PREFIX}-{child}")
    local_decls = {
        f"{PREFIX}-C-ACTION-CONNECTED": "quotientActionConnected_of_components",
        f"{PREFIX}-N-QUOTIENT-END-FREE": "quotientVertexEndFree_of_components",
        f"{PREFIX}-C-END-SUBGROUP-EQUIV": "endSubgroupEquiv_of_components",
        f"{PREFIX}-T-ASSEMBLE": "exactAssembly_of_end_packages",
        f"{PREFIX}-ROOT": "root_of_exactAssembly",
    }
    certificates = []
    for parent, child_ids in children.items():
        suffix = parent.removeprefix(PREFIX + "-")
        declaration = ("Stage1Instances.THM_M_0079.ObligationTree." + local_decls[parent]) if parent in local_decls else next(row["formal"] for row in ROWS if row["id"] == parent)
        fingerprints = {row["obligation_id"]: row["statement_fingerprint"] for row in obligations}
        checked = parent in local_decls
        certificates.append({
            "certificate_id": f"M0079-CERT-{suffix}", "declaration": declaration,
            "parent_id": parent, "parent_statement_fingerprint": fingerprints[parent],
            "required_child_ids": child_ids,
            "required_child_statement_fingerprints": {child: fingerprints[child] for child in child_ids},
            "conditional": True, "kernel_checked_interface": checked, "accepted": False,
            "status": "conditional_kernel_checked" if checked else "planned_source_composition_pending_exact_child_harness",
            "statement_fingerprint_binding": (
                "The exact root uses its elaborated-expression hash. Non-root values are frozen "
                "planned-signature-v1 hashes of NUL-joined obligation ID, human statement, formal "
                "target label, and output; they are architecture identities, not elaborated Lean "
                "expression hashes. Checked local declarations additionally have exact Lean type "
                "ascriptions in ObligationTree.lean. Accepted proof-phase dependency inspection "
                "remains open."
            ),
        })
    bundle = {
        "schema_version": "stage1-typed-graphs/1.0", "item_id": ITEM, "theorem_id": THEOREM,
        "registry_id": registry["registry_id"], "registry_denominator_sha256": denominator,
        "frozen_against_execution_dag_sha256": sha256(execution_path), "local_task_dag_projection_sha256": sha256(HERE / "task-dag.json"),
        "root_node_id": f"{PREFIX}-ROOT", "edge_direction": "proof_requires parent-to-child and reciprocal composes child-to-parent; non-proof graphs never grant proof closure.",
        "nodes": nodes, "graphs": graphs,
        "evidence_endpoint_policy": "Receipts are external typed objects. The evidence graph is empty until content-addressed accepted evidence exists; node evidence_ids binds it later.",
        "composition_certificates": certificates,
        "closure_boundary": {"root_closed": False, "root_machine_classification": "M3", "accepted_closed_obligations": [],
            "checked_conditional_interfaces": list(local_decls),
            "remaining_root_cut_set": registry["frozen_denominators"]["required_unique_architecture_frontier"],
            "remaining_required_machine_assurance_frontier": [f"{PREFIX}-S-FOUNDATION"],
            "remaining_root_critical_nonproof_gates": [f"{PREFIX}-S-FOUNDATION", f"{PREFIX}-X-SOURCE", f"{PREFIX}-X-PROVENANCE", f"{PREFIX}-X-TRUST", f"{PREFIX}-X-DOCUMENTATION", f"{PREFIX}-X-WORKFLOW"],
            "audit_complete": False, "theorem_complete": False,
            "reason": "Conditional composition elaborates, but candidate installation, proof-body acceptance, H0/R0, transitive provenance/trust, validation, release, and master acceptance are later gates."},
    }
    task_links = ([{"task_id": ITEM, "obligation_id": oid} for oid in ids] +
        [{"task_id": "S56-M-0079-PROOF", "obligation_id": oid} for oid in required] +
        [{"task_id": task, "obligation_id": oid} for task in ("S56-M-0079-VALIDATION", "S56-M-0079-RELEASE") for oid in (f"{PREFIX}-S-FOUNDATION", f"{PREFIX}-X-SOURCE", f"{PREFIX}-X-PROVENANCE", f"{PREFIX}-X-TRUST", f"{PREFIX}-X-DOCUMENTATION", f"{PREFIX}-X-WORKFLOW")])
    task_ids_by_obligation = {oid: [] for oid in ids}
    for link in task_links:
        task_ids_by_obligation[link["obligation_id"]].append(link["task_id"])
    for node in nodes:
        node["task_ids"] = task_ids_by_obligation[node["obligation_id"]]
    bundle["workflow_task_graph"] = {
        "authority": "Docs/Stage1_Execution_DAG_rev-5.6.json", "authority_sha256": sha256(execution_path),
        "local_projection_boundary": "task-dag.json omits intake and does not override the seven-item authority.",
        "nodes": [{"task_id": t["id"], "phase": t["phase"], "layer": t["layer"]} for t in tasks],
        "edges": [{"edge_id": f"TASK-{i:02d}", "type": "workflow_depends_on", "from": t["id"], "to": dep} for i, t in enumerate(tasks, 1) for dep in t["depends_on"]],
        "task_obligation_links": task_links,
    }
    architecture_recipe_id = "S56-M-0079-OBLIGATION-TREE-GENERATOR-CHECK"
    lean_recipe_id = "S56-M-0079-OBLIGATION-TREE-LEAN"
    for node in nodes:
        node["validation_spec_id"] = (
            lean_recipe_id if node["obligation_id"] in local_decls else architecture_recipe_id
        )
    recipes = [
        {"recipe_id": "S56-M-0079-OBLIGATION-TREE-GENERATOR-CHECK", "cwd": ".", "argv": ["python3", "-B", "Stage1_Instances/THM-M-0079/build_obligation_artifacts.py", "--check"], "env_allowlist": {}, "timeout_seconds": 60, "network_policy": "denied", "expected_exit": 0, "expected_outputs": [{"path_or_stream": "stdout", "semantic_hash_policy": "deterministic generated artifacts match"}], "covered_obligation_ids": ids, "covered_declarations": [], "coverage_semantics": "generator drift check", "closure_credit": False},
        {"recipe_id": "S56-M-0079-OBLIGATION-TREE-LEAN", "cwd": ".", "argv": ["python3", "-B", "Stage1_Instances/THM-M-0079/check_obligation_tree.py"], "env_allowlist": {}, "timeout_seconds": 180, "network_policy": "denied", "expected_exit": 0, "expected_outputs": [{"path_or_stream": "stdout", "semantic_hash_policy": "reports conditional Lean output sha256"}], "covered_obligation_ids": [f"{PREFIX}-ROOT", f"{PREFIX}-C-ACTION-CONNECTED", f"{PREFIX}-N-QUOTIENT-END-FREE", f"{PREFIX}-C-END-SUBGROUP-EQUIV", f"{PREFIX}-T-ASSEMBLE"], "covered_declarations": ["Stage1Instances.THM_M_0079.ObligationTree.quotientActionConnected_of_components", "Stage1Instances.THM_M_0079.ObligationTree.endSubgroupEquiv_of_components", "Stage1Instances.THM_M_0079.ObligationTree.quotientVertexEndFree_of_components", "Stage1Instances.THM_M_0079.ObligationTree.exactAssembly_of_end_packages", "Stage1Instances.THM_M_0079.ObligationTree.root_of_exactAssembly"], "coverage_semantics": "conditional composition and exact-root identity only", "closure_credit": False},
    ]
    return registry, bundle, {"schema_version": "stage1-validation-specs/1.0", "item_id": ITEM, "theorem_id": THEOREM, "recipes": recipes}


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
        for name, value in artifacts.items(): (HERE / name).write_text(serialized(value))
    else:
        for name, value in artifacts.items(): assert (HERE / name).read_text() == serialized(value), f"generated artifact drift: {name}"
    registry, bundle, _ = artifacts.values()
    count = sum(len(g["edges"]) for g in bundle["graphs"].values())
    print(f"PASS deterministic artifacts: {len(registry['obligations'])} obligations, {count} typed edges")
    print(f"registry denominator sha256: {registry['denominator_sha256']}")


if __name__ == "__main__":
    main()
