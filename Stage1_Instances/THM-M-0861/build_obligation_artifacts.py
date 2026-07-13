#!/usr/bin/env python3
"""Deterministically build the THM-M-0861 obligation freeze."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
THEOREM = "THM-M-0861"
ITEM = "S56-M-0861-OBLIGATION_TREE"
PREFIX = "M0861-"
ROOT_EXPRESSION = "4e7919ed3b44379a42d69ef88cfb5e512248eccfe755392723cb6769c4f8e197"


def oid(short: str) -> str:
    return PREFIX + short


def digest(value: object) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(payload).hexdigest()


def row(short: str, reg_kind: str, node_kind: str, risk: str, claim: str,
        formal: str, output: str, locator: str, budget: int,
        machine: str = "required", human: str = "required",
        body: str | None = None) -> dict:
    return {
        "short": short,
        "id": oid(short),
        "reg_kind": reg_kind,
        "node_kind": node_kind,
        "risk": risk,
        "claim": claim,
        "formal": formal,
        "output": output,
        "locator": locator,
        "budget": budget,
        "machine": machine,
        "human": human,
        "body": body,
    }


ROWS = [
    row("ROOT", "root", "root", "critical",
        "Every finite bipartite multigraph has chromatic index equal to its multiplicity-counted maximum degree.",
        "Stage1Instances.THM_M_0861.KonigEdgeColoringTarget",
        "The exact canonical proposition at universes u and v.",
        "Statement.lean:83-102", 6),
    row("S-TARGET", "definition", "definition", "critical",
        "Freeze arbitrary ambient vertex and edge types, finite actual sets, bipartiteness, maximum degree, and least proper palette.",
        "Stage1Instances.THM_M_0861.KonigEdgeColoringTarget",
        "The exact elaborated root interface.", "Statement.lean:21-102", 16,
        human="not_applicable"),
    row("S-REPRESENTATION", "definition", "definition", "high",
        "Use Graph with separate edge identities, so parallel edges survive and actual vertices and edges are set-valued.",
        "Graph Vertex Edge; Graph.IsLink; Graph.Inc; Graph.incidenceSet",
        "A source-faithful finite multigraph representation.", "Statement.lean:22-49", 12,
        human="not_applicable"),
    row("S-BIPARTITE", "definition", "definition", "high",
        "A Bool side assignment separates the ends of every actual link and therefore excludes loops.",
        "Stage1Instances.THM_M_0861.IsBipartite",
        "The exact bipartite and loop policy.", "Statement.lean:21-37", 10,
        human="not_applicable", body="repo:Stage1Instances.THM_M_0861.IsBipartite.noLoops"),
    row("S-COLORING", "definition", "definition", "critical",
        "Color the subtype of actual edge identities by Fin k and separate every distinct pair incident at a common vertex.",
        "Stage1Instances.THM_M_0861.{EdgeColorable,HasChromaticIndex}",
        "Exact proper-coloring and least-palette interfaces.", "Statement.lean:51-81", 16,
        human="not_applicable"),
    row("S-BOUNDARY", "branch", "branch", "high",
        "Retain empty actual sets, isolated vertices, disconnected graphs, Delta=0, parallel edges, and arbitrary ambient carrier types.",
        "edgeColorable_zero_of_edgeSet_eq_empty; hasChromaticIndex_zero_of_edgeSet_eq_empty",
        "No hidden nonempty, connected, regular, simple, or ambient-Fintype premise.",
        "Statement.lean:60-81; scope-map.md:33-39", 14, human="not_applicable",
        body="repo:Stage1Instances.THM_M_0861.hasChromaticIndex_zero_of_edgeSet_eq_empty"),
    row("S-TRANSPORT", "transport", "transport", "high",
        "Identify the canonical least-palette statement with the exact upper-and-lower conjunction.",
        "Stage1Instances.THM_M_0861_Obligations.RootTransportTarget",
        "A checked bidirectional transport to ExpandedTarget.", "Statement.lean:90-102", 4,
        human="not_applicable",
        body="repo:Stage1Instances.THM_M_0861.konigEdgeColoringTarget_iff_expandedTarget"),
    row("S-FOUNDATION", "terminal", "certificate", "critical",
        "Audit classical choice, propositional extensionality, quotient soundness, finite cardinality, the Lean kernel, and the no-oracle policy.",
        "future transitive axiom and TCB packet for the exact terminal declarations",
        "An accepted foundation and TCB boundary.", "statement.json profiles; anchor-audit.json immutable_environment", 30,
        human="not_applicable"),
    row("N-BOUNDED", "reduction", "normalization", "critical",
        "Use the source-strengthened fixed-k Satz C interface: degree at every actual vertex is at most k, hence k-edge-colorability.",
        "Stage1Instances.THM_M_0861_Obligations.{DegreeBound,BoundedSatzCTarget}",
        "The source-facing fixed-palette proposition.", "ObligationTree.lean:20-32; Koenig 1916 Satz C", 10),
    row("T-ASSEMBLE", "terminal", "terminal", "critical",
        "Consume the exact upper and lower conjuncts and transport their conjunction to the canonical root.",
        "Stage1Instances.THM_M_0861_Obligations.AssemblyTarget",
        "The exact bundled upper and lower packages consumed by root composition.", "ObligationTree.lean:48-75", 5,
        body="repo:Stage1Instances.THM_M_0861_Obligations.assembly_of_upper_and_lower"),
    row("T-UPPER", "terminal", "terminal", "critical",
        "Instantiate fixed-k Satz C at maxDegree after proving every actual vertex degree is bounded by that supremum.",
        "Stage1Instances.THM_M_0861_Obligations.UpperBoundTarget",
        "EdgeColorable G (maxDegree G vertexFinite).", "ObligationTree.lean:34-38", 8),
    row("L-DEGREE-LE-MAX", "lemma", "core_lemma", "high",
        "Every actual vertex has incidence degree at most the finite supremum maxDegree.",
        "planned exact Lean signature over vertexFinite.toFinset.sup",
        "DegreeBound G (maxDegree G vertexFinite).", "Statement.lean:41-49", 24),
    row("T-LOWER", "terminal", "terminal", "critical",
        "Any proper k-edge-coloring forces maxDegree G vertexFinite <= k.",
        "Stage1Instances.THM_M_0861_Obligations.LowerBoundTarget",
        "The exact minimality conjunct of HasChromaticIndex.", "ObligationTree.lean:40-46", 8),
    row("L-INCIDENCE-FIN", "lemma", "core_lemma", "high",
        "Each incidence fiber is finite because it is a subset of the finite actual edge set.",
        "planned: G.edgeSet.Finite -> (G.incidenceSet x).Finite",
        "A finite incidence-edge subtype for cardinal comparison.", "Graph.incidenceSet_subset_edgeSet", 16),
    row("L-COLOR-INJECTIVE", "lemma", "core_lemma", "critical",
        "Restrict a proper edge coloring to one incidence fiber and prove that restriction injective.",
        "planned exact subtype injection into Fin k",
        "degree G x <= k for every actual vertex x.", "Statement.lean:54-58", 28),
    row("L-SUP-LOWER", "lemma", "core_lemma", "high",
        "Lift the pointwise incidence-cardinality bounds through the finite vertex-set supremum.",
        "planned Finset.sup_le composition",
        "maxDegree G vertexFinite <= k.", "Statement.lean:47-49", 18),
    row("B-EDGE-INDUCTION", "branch", "branch", "critical",
        "Prove fixed-k Satz C by strong induction on the finite actual-edge cardinality.",
        "planned Nat strong-induction package over G.edgeSet.ncard",
        "BoundedSatzCTarget.", "Koenig 1916 pp.455-456", 14),
    row("B-EDGE-COUNT-SPLIT", "branch", "branch", "high",
        "Split ncard G.edgeSet <= k from k < ncard G.edgeSet and recombine exhaustively.",
        "planned le_total (G.edgeSet.ncard) k",
        "Either the global-injection base or edge-deletion step applies.", "Koenig 1916 p.455", 8),
    row("B-SMALL-EDGE-COUNT", "branch", "branch", "high",
        "When the total number of actual edges is at most k, color all actual edges injectively into Fin k.",
        "planned global injective coloring of {e // e in G.edgeSet}",
        "A proper k-edge-coloring without incidence analysis.", "Koenig 1916 p.455", 12),
    row("L-SMALL-PALETTE-EMBED", "lemma", "core_lemma", "high",
        "Embed the finite actual-edge subtype into Fin k from its cardinal bound.",
        "planned finite subtype cardinal embedding",
        "An injective palette assignment on every actual edge.", "Koenig 1916 p.455", 22),
    row("B-LARGE-EDGE-COUNT", "branch", "branch", "critical",
        "When k is smaller than the edge count, choose an actual edge, delete it, recolor, and insert it again.",
        "planned large-edge-count induction branch",
        "A proper k-edge-coloring of the original graph.", "Koenig 1916 pp.455-456", 18),
    row("L-CHOOSE-ACTUAL-EDGE", "lemma", "core_lemma", "high",
        "Extract an actual edge and its two distinct endpoints from nonempty edgeSet and bipartiteness.",
        "planned exists e a b, e in G.edgeSet and G.IsLink e a b and a != b",
        "The edge and endpoint data used by deletion and insertion.", "Graph.exists_isLink_of_mem_edgeSet; IsBipartite.noLoops", 24),
    row("C-ERASE-EDGE", "construction", "construction", "critical",
        "Construct a graph on the same ambient vertex and edge types whose actual edge set is G.edgeSet minus the chosen identity.",
        "planned Graph value with edgeSet = G.edgeSet \\ {e}",
        "The induction subgraph with parallel identities otherwise unchanged.", "Mathlib.Combinatorics.Graph.Basic", 32),
    row("L-ERASE-SETS", "lemma", "core_lemma", "high",
        "Prove the deletion graph has the same actual vertex set, the expected edge set, and inherited links for every retained edge.",
        "planned deletion graph simp interface",
        "Exact set and link transports for later subtype conversions.", "planned local construction", 30),
    row("L-ERASE-CARD", "lemma", "core_lemma", "critical",
        "Prove deletion removes exactly one actual edge and strictly decreases ncard.",
        "planned ncard (G.edgeSet \\ {e}) = G.edgeSet.ncard - 1",
        "The strong-induction decrease certificate.", "Koenig 1916 p.455", 24),
    row("L-ERASE-BIPARTITE", "lemma", "core_lemma", "high",
        "Reuse the original Bool side map for every retained link.",
        "planned IsBipartite deletionGraph",
        "Bipartiteness of the induction graph.", "Statement.lean:22-29", 12),
    row("L-ERASE-DEGREE", "lemma", "core_lemma", "critical",
        "Show deletion never increases a degree and drops it at both chosen endpoints.",
        "planned incidence-set deletion cardinal equalities and inequalities",
        "DegreeBound for the deletion graph and strict endpoint palette slack.", "Koenig 1916 p.455", 32),
    row("C-IH-COLORING", "construction", "construction", "critical",
        "Apply the induction hypothesis to the deletion graph and transport its actual-edge-subtype coloring.",
        "planned EdgeColorable deletionGraph k plus retained-edge subtype transport",
        "A proper k-coloring on every original edge except the chosen one.", "Koenig 1916 p.455", 26),
    row("L-ACTUAL-EDGE-TRANSPORT", "transport", "transport", "high",
        "Relate deletion-graph actual edge subtypes to original actual edge identities different from the erased edge.",
        "planned checked subtype equivalence and coloring transport",
        "A coloring usable with original Graph.Inc facts.", "planned deletion interface", 24),
    row("L-K-POSITIVE-OF-EDGE", "lemma", "core_lemma", "high",
        "An actual edge under DegreeBound G k forces 0 < k.",
        "planned contradiction from endpoint incidence when k = 0",
        "A nonempty Fin k palette in the large branch.", "Koenig 1916 p.455", 18),
    row("C-MISSING-COLORS", "construction", "construction", "critical",
        "Choose a missing palette color at each endpoint after the incident deleted edge creates strict slack.",
        "planned endpoint incident-color finite sets and complement witnesses",
        "Colors alpha and beta absent at the two endpoints.", "Koenig 1916 p.455", 28),
    row("L-PALETTE-PIGEONHOLE", "lemma", "core_lemma", "critical",
        "A proper coloring of fewer than k incident edges omits some element of Fin k.",
        "planned finite-cardinality non-surjectivity argument",
        "One missing color at each endpoint.", "Koenig 1916 p.455", 32),
    row("B-MISSING-SPLIT", "branch", "branch", "high",
        "Split whether the two endpoints share a missing color and prove the alternatives exhaustive.",
        "planned Decidable split on common missing palette value",
        "Either direct insertion or the alternating-color route.", "Koenig 1916 p.455", 8),
    row("B-COMMON-MISSING", "branch", "branch", "normal",
        "If one color is missing at both endpoints, give it to the erased edge.",
        "planned direct extension branch",
        "A proper k-coloring of the original graph.", "Koenig 1916 p.455", 10),
    row("B-DISTINCT-MISSING", "branch", "branch", "critical",
        "For distinct endpoint-missing colors, build and swap the maximal alternating component before insertion.",
        "planned Kempe recoloring branch",
        "A proper k-coloring of the original graph.", "Koenig 1916 pp.455-456", 14),
    row("L-CROSS-COLOR-PRESENT", "lemma", "core_lemma", "high",
        "With no common missing color, the color missing at one endpoint occurs at the other, and conversely.",
        "planned negation-of-common-missing specialization",
        "The first alternating edge at each relevant endpoint.", "Koenig 1916 p.455", 18),
    row("C-ALT-STATE", "construction", "construction", "critical",
        "Define a finite state carrying a vertex, a retained incident edge, and the next expected one of the two colors.",
        "planned local multigraph alternating-trail state",
        "A representation that preserves edge identity without SimpleGraph substitution.", "source-shaped local interface", 28),
    row("L-COLOR-UNIQUENESS", "lemma", "core_lemma", "critical",
        "At a vertex, properness permits at most one incident edge of each selected color.",
        "planned consequence of EdgeColorable properness",
        "Determinism of alternating continuation.", "Statement.lean:54-58", 20),
    row("C-ALTERNATING-TRAIL", "construction", "construction", "critical",
        "Starting at the first endpoint, repeatedly follow the unique next incident edge of the alternating color when it exists.",
        "planned finite alternating trail construction",
        "A maximal two-color trail from the first endpoint.", "Koenig 1916 pp.455-456", 48),
    row("L-TRAIL-NOREPEAT", "lemma", "core_lemma", "critical",
        "The alternating construction does not revisit a vertex or reuse an edge.",
        "planned contradiction using color uniqueness and bipartiteness",
        "A simple finite alternating trail.", "Koenig 1916 p.456", 36),
    row("L-TRAIL-TERMINATES", "lemma", "core_lemma", "critical",
        "Finiteness of the actual edge set makes the no-repeat continuation terminate at a maximal endpoint.",
        "planned finite-state termination measure",
        "A maximal finite alternating trail.", "Koenig 1916 p.456", 36),
    row("L-TRAIL-ALTERNATES", "lemma", "core_lemma", "high",
        "Successive trail edges alternate the two selected palette values with the chosen initial color.",
        "planned induction over the alternating trail",
        "The exact parity-to-color relation at both ends.", "Koenig 1916 p.456", 24),
    row("L-ENDPOINT-PARITY", "lemma", "core_lemma", "critical",
        "A hypothetical trail from the first endpoint to the second has even length from its endpoint colors but odd length from their opposite Bool sides.",
        "planned parity contradiction using IsBipartiteWith",
        "The second endpoint cannot lie on the alternating trail.", "Koenig 1916 p.456", 42),
    row("L-B-NOT-REACHED", "lemma", "core_lemma", "critical",
        "Conclude that the alternating component starting at the first endpoint avoids the second endpoint.",
        "planned consequence of endpoint parity",
        "A safe component on which to exchange the two colors.", "Koenig 1916 p.456", 12),
    row("C-SWAP", "construction", "construction", "critical",
        "Exchange the two selected colors exactly on edges of the alternating component.",
        "planned recoloring function on retained actual edges",
        "A recolored deletion graph.", "Koenig 1916 p.456", 26),
    row("L-SWAP-PROPER", "lemma", "core_lemma", "critical",
        "The color exchange preserves properness at internal, boundary, and outside vertices.",
        "planned incidence case split using maximality and color uniqueness",
        "EdgeColorable deletionGraph k after the swap.", "Koenig 1916 p.456", 44),
    row("L-SWAP-MISSING", "lemma", "core_lemma", "critical",
        "After the swap, one selected color is missing at both endpoints because the second endpoint was not reached.",
        "planned endpoint incidence analysis",
        "A common missing color for the erased edge.", "Koenig 1916 p.456", 24),
    row("C-EXTEND-EDGE", "construction", "construction", "critical",
        "Extend the retained-edge coloring to the erased edge using a color missing at both endpoints.",
        "planned actual-edge subtype extension",
        "A proper k-edge-coloring of G.", "Koenig 1916 pp.455-456", 30),
    row("T-SATZ-C", "terminal", "terminal", "critical",
        "Compose the edge-count induction, deletion, missing-color, alternating-trail, swap, and insertion packages.",
        "planned inhabitant of BoundedSatzCTarget",
        "The source-strengthened fixed-k upper theorem.", "Koenig 1916 Satz C, pp.455-456", 18),
    row("X-SOURCE", "terminal", "terminal", "critical",
        "Map every material node to admitted primary sources, exact locators, assumptions, translation, equality bridge, errata, and independent review.",
        "node-specific Koenig 1916 plus lower-bound source packet pending",
        "Human-source coverage without machine proof credit.", "source-statement-crosswalk.md", 80,
        machine="not_applicable"),
    row("X-PROVENANCE", "terminal", "certificate", "critical",
        "Bind statement, support interfaces, future terminal bodies, immutable origins, licenses, aliases, and revocations without duplicate credit.",
        "anchor-audit.json plus future terminal-body closure",
        "Proof-body provenance without mathematical proof credit.", "anchor-audit.json", 45,
        machine="informational", human="not_applicable"),
    row("X-TRUST", "terminal", "certificate", "critical",
        "Audit transitive declarations, axioms, compiled artifacts, executables, unsafe or oracle boundaries, and independent replay.",
        "Lean 4.29.0 and mathlib 8a178386 transitive closure pending",
        "Release-grade trust coverage without mathematical proof credit.", "anchor-audit.json immutable_environment", 45,
        machine="informational", human="not_applicable"),
    row("X-READABLE", "terminal", "terminal", "high",
        "Produce and independently review the complete node-specific proof outline and long reconstruction.",
        "future proof outline, process surface, and reader receipt",
        "Readable coverage without machine proof credit.", "obligation-tree.md is architecture only", 80,
        machine="not_applicable"),
    row("X-WORKFLOW", "terminal", "terminal", "critical",
        "Bind proof, composition, validation, source, readability, freshness, revocation, independent verification, and release tasks.",
        "Stage1 execution and receipt closure pending",
        "Workflow acceptance without mathematical proof credit.", "rev-5.6 task chain", 30,
        machine="informational", human="not_applicable"),
]


REQUIRES = {
    oid("ROOT"): [oid("S-TRANSPORT"), oid("T-ASSEMBLE")],
    oid("T-ASSEMBLE"): [oid("T-UPPER"), oid("T-LOWER")],
    oid("T-UPPER"): [oid("L-DEGREE-LE-MAX"), oid("T-SATZ-C")],
    oid("T-LOWER"): [oid("L-INCIDENCE-FIN"), oid("L-COLOR-INJECTIVE"), oid("L-SUP-LOWER")],
    oid("T-SATZ-C"): [oid("B-EDGE-INDUCTION")],
    oid("B-EDGE-INDUCTION"): [oid("B-EDGE-COUNT-SPLIT")],
    oid("B-EDGE-COUNT-SPLIT"): [oid("B-SMALL-EDGE-COUNT"), oid("B-LARGE-EDGE-COUNT")],
    oid("B-SMALL-EDGE-COUNT"): [oid("L-SMALL-PALETTE-EMBED")],
    oid("B-LARGE-EDGE-COUNT"): [
        oid("L-CHOOSE-ACTUAL-EDGE"), oid("C-ERASE-EDGE"), oid("L-ERASE-SETS"),
        oid("L-ERASE-CARD"), oid("L-ERASE-BIPARTITE"), oid("L-ERASE-DEGREE"),
        oid("C-IH-COLORING"), oid("L-ACTUAL-EDGE-TRANSPORT"),
        oid("L-K-POSITIVE-OF-EDGE"), oid("C-MISSING-COLORS"), oid("B-MISSING-SPLIT"),
    ],
    oid("C-IH-COLORING"): [
        oid("L-ERASE-CARD"), oid("L-ERASE-BIPARTITE"), oid("L-ERASE-DEGREE"),
        oid("L-ACTUAL-EDGE-TRANSPORT"),
    ],
    oid("C-MISSING-COLORS"): [oid("L-ERASE-DEGREE"), oid("L-PALETTE-PIGEONHOLE")],
    oid("B-MISSING-SPLIT"): [oid("B-COMMON-MISSING"), oid("B-DISTINCT-MISSING")],
    oid("B-COMMON-MISSING"): [oid("C-EXTEND-EDGE")],
    oid("B-DISTINCT-MISSING"): [
        oid("L-CROSS-COLOR-PRESENT"), oid("C-ALT-STATE"), oid("L-COLOR-UNIQUENESS"),
        oid("C-ALTERNATING-TRAIL"), oid("L-TRAIL-NOREPEAT"), oid("L-TRAIL-TERMINATES"),
        oid("L-TRAIL-ALTERNATES"), oid("L-ENDPOINT-PARITY"), oid("L-B-NOT-REACHED"),
        oid("C-SWAP"), oid("L-SWAP-PROPER"), oid("L-SWAP-MISSING"), oid("C-EXTEND-EDGE"),
    ],
    oid("C-ALTERNATING-TRAIL"): [oid("C-ALT-STATE"), oid("L-COLOR-UNIQUENESS")],
    oid("L-TRAIL-NOREPEAT"): [oid("C-ALTERNATING-TRAIL"), oid("L-COLOR-UNIQUENESS")],
    oid("L-TRAIL-TERMINATES"): [oid("C-ALTERNATING-TRAIL"), oid("L-TRAIL-NOREPEAT")],
    oid("L-TRAIL-ALTERNATES"): [oid("C-ALTERNATING-TRAIL")],
    oid("L-ENDPOINT-PARITY"): [oid("L-TRAIL-ALTERNATES")],
    oid("L-B-NOT-REACHED"): [oid("L-ENDPOINT-PARITY")],
    oid("C-SWAP"): [oid("C-ALTERNATING-TRAIL"), oid("L-B-NOT-REACHED")],
    oid("L-SWAP-PROPER"): [
        oid("C-SWAP"), oid("L-COLOR-UNIQUENESS"), oid("L-TRAIL-TERMINATES")
    ],
    oid("L-SWAP-MISSING"): [oid("C-SWAP"), oid("L-B-NOT-REACHED")],
    oid("C-EXTEND-EDGE"): [
        oid("L-CHOOSE-ACTUAL-EDGE"), oid("L-ACTUAL-EDGE-TRANSPORT")
    ],
}


CHECKED_INTERFACES = {
    oid("S-BIPARTITE"), oid("S-BOUNDARY"), oid("S-TRANSPORT"), oid("T-ASSEMBLE")
}


def edge(edge_id: str, source: str, edge_type: str, target: str,
         reciprocal: str | None = None) -> dict:
    value = {"edge_id": edge_id, "from": source, "type": edge_type, "to": target}
    if reciprocal is not None:
        value["reciprocal_edge_id"] = reciprocal
    return value


def graph(endpoints: list[str], values: list[dict]) -> dict:
    outgoing = {identifier: [] for identifier in endpoints}
    incoming = {identifier: [] for identifier in endpoints}
    for value in values:
        outgoing[value["from"]].append(value["edge_id"])
        incoming[value["to"]].append(value["edge_id"])
    return {"edges": values, "out": outgoing, "in": incoming}


def build() -> tuple[dict, dict, dict]:
    statement_hash = hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
    anchor_hash = hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest()
    obligations = []
    for spec in ROWS:
        fingerprint = (
            f"lean-expression-sha256:{ROOT_EXPRESSION}"
            if spec["short"] in {"ROOT", "S-TARGET"}
            else "planned:v1:sha256:" + digest([
                spec["id"], spec["reg_kind"], spec["claim"], spec["formal"], spec["output"]
            ])
        )
        reasons = []
        if spec["machine"] != "required":
            reasons.append("no_machine_proof_credit")
        if spec["human"] != "required":
            reasons.append("not_a_distinct_human_claim")
        obligations.append({
            "obligation_id": spec["id"],
            "statement_fingerprint": fingerprint,
            "kind": spec["reg_kind"],
            "root_relevant": True,
            "machine_eligibility": spec["machine"],
            "human_source_eligibility": spec["human"],
            "readable_eligibility": "required",
            "risk_class": spec["risk"],
            "exclusion_reason": (
                "_and_".join(reasons) + "_pending_independent_approval" if reasons else None
            ),
            "terminal_proof_body_id": spec["body"],
        })

    fields = (
        "obligation_id", "statement_fingerprint", "kind", "root_relevant",
        "machine_eligibility", "human_source_eligibility", "readable_eligibility",
        "risk_class", "exclusion_reason", "terminal_proof_body_id",
    )
    denominator = digest([{key: value[key] for key in fields} for value in obligations])
    ids = [value["obligation_id"] for value in obligations]
    by_id = {value["obligation_id"]: value for value in obligations}

    parents = {identifier: [] for identifier in ids}
    for parent, children in REQUIRES.items():
        for child in children:
            parents[child].append(parent)

    nodes = []
    for spec in ROWS:
        identifier = spec["id"]
        if identifier == oid("ROOT"):
            machine_debt = "M4"
        elif identifier in CHECKED_INTERFACES or spec["short"] in {
            "S-TARGET", "S-REPRESENTATION", "S-COLORING", "N-BOUNDED"
        }:
            machine_debt = "M3"
        else:
            machine_debt = "M4"
        children = REQUIRES.get(identifier, [])
        human_debt = "H1" if spec["human"] == "required" else "H2"
        nodes.append({
            "node_id": f"{THEOREM}-{spec['short']}",
            "obligation_id": identifier,
            "kind": spec["node_kind"],
            "human_statement": spec["claim"],
            "formal_target": spec["formal"],
            "output": spec["output"],
            "human_debt": human_debt,
            "machine_debt": machine_debt,
            "readability_debt": "R4",
            "evidence_ids": [],
            "source_crosswalk_id": (
                "not-applicable-pending-review" if spec["human"] != "required"
                else "Koenig-1916-Satz-C-node-map-pending-independent-review"
            ),
            "provenance_id": (
                "repo-local-conditional-interface" if identifier in CHECKED_INTERFACES
                else "anchor-audit:substrate-only" if spec["short"] in {
                    "S-REPRESENTATION", "S-BIPARTITE", "S-COLORING"
                } else "none"
            ),
            "foundation_profile": "Lean4 dependent type theory; classical finite-cardinality use expected; accepted exact axiom policy pending",
            "tcb_profile": "Lean-4.29.0+mathlib-8a178386; transitive declaration, compiled-artifact, and independent replay closure pending",
            "computation_record": "none; no enumeration, oracle, native shortcut, experiment, or unchecked certificate is credited",
            "step_budget": spec["budget"],
            "semantic_step_ledger": [{
                "step_id": identifier + "-STEP-01",
                "premise_ids": children if children else ["exact-formal-context-no-hidden-proof-premise"],
                "inference": spec["formal"],
                "source_locator": spec["locator"],
                "output": spec["output"],
                "outgoing_use": parents[identifier] if parents[identifier]
                else ["typed-non-proof-edge-or-canonical-root-boundary"],
            }],
            "public_readable_target": f"Stage1_Instances/{THEOREM}/obligation-tree.md#{identifier.lower()}",
            "validation_spec_id": f"VAL-{identifier}",
            "status_boundary": "Frozen architecture or checked conditional interface only; no open proof child, H0, M0, R0, audit completion, or theorem completion is discharged.",
            "task_ids": [ITEM, "S56-M-0861-PROOF", "S56-M-0861-VALIDATION"],
            "owned_sources": (
                [f"Stage1_Instances/{THEOREM}/ObligationTree.lean"]
                if identifier in CHECKED_INTERFACES | {oid("N-BOUNDED")} else []
            ),
            "owner": "THM-M-0861 proof lane",
            "reviewer": "independent Stage1 integration lane",
            "validity": {
                "validated_at": "2026-07-13" if identifier in CHECKED_INTERFACES else None,
                "review_due": "before proof acceptance",
                "invalidation_inputs": [
                    "Statement.lean", "anchor-audit.json", "obligation-registry.json",
                    "typed-graphs.json", "source crosswalk", "toolchain", "dependency pin",
                ],
                "revocation_state": "provisional" if identifier in CHECKED_INTERFACES else "open",
            },
        })

    registry = {
        "schema_version": "stage1-obligation-registry/1.0",
        "registry_id": "THM-M-0861-OBLIGATIONS-v1",
        "item_id": ITEM,
        "theorem_id": THEOREM,
        "registry_version": 1,
        "frozen_at": "2026-07-13T00:00:00+08:00",
        "freeze_basis": "Exact elaborated finite-bipartite-multigraph equality plus the immutable no-exact-candidate anchor audit; Koenig's source-shaped fixed-k edge-induction and alternating-color path architecture was selected before any proof closure credit.",
        "frozen_against_statement_sha256": statement_hash,
        "frozen_against_anchor_audit_sha256": anchor_hash,
        "root_obligation_id": oid("ROOT"),
        "denominator_sha256": denominator,
        "frozen_denominators": {
            "inventory": ids,
            "required_machine": [value["obligation_id"] for value in obligations if value["machine_eligibility"] == "required"],
            "required_human_source": [value["obligation_id"] for value in obligations if value["human_source_eligibility"] == "required"],
            "required_readable": ids,
            "informational_overlays": [oid("X-PROVENANCE"), oid("X-TRUST"), oid("X-WORKFLOW")],
        },
        "delta_policy": "Any correction, split, merge, exclusion, eligibility, risk, proof-body identity, or weight change requires registry version 2 and an append-only old/new ID delta.",
        "append_only_delta": [],
        "status_observed_after_freeze": {
            "provisionally_checked_interfaces": sorted(CHECKED_INTERFACES),
            "accepted_closed_obligations": [],
            "authoritative_root_machine_debt": "M4",
        },
        "mandatory_layer_analysis": {
            "S": [value["id"] for value in ROWS if value["short"].startswith("S-")],
            "N": [oid("N-BOUNDED")],
            "B": [value["id"] for value in ROWS if value["short"].startswith("B-")],
            "C": [value["id"] for value in ROWS if value["reg_kind"] == "construction"],
            "L": [value["id"] for value in ROWS if value["reg_kind"] == "lemma"],
            "X": [value["id"] for value in ROWS if value["short"].startswith("X-")],
            "T": [oid("T-ASSEMBLE"), oid("T-UPPER"), oid("T-LOWER"), oid("T-SATZ-C"), oid("ROOT")],
            "not_applicable_layers": [],
        },
        "obligations": obligations,
        "status_boundary": "The semantic denominator and eligibility are frozen, but every proof obligation remains unaccepted. The conditional assembly harness is not a proof of either upper or lower package.",
    }

    proof_edges = []
    unverified_plans = []
    sequence = 0
    for parent, children in REQUIRES.items():
        for child in children:
            sequence += 1
            req = f"P{sequence:03d}-REQ"
            reverse = f"P{sequence:03d}-REV"
            checked = (
                (parent == oid("ROOT") and child in {oid("S-TRANSPORT"), oid("T-ASSEMBLE")})
                or (parent == oid("T-ASSEMBLE") and child in {oid("T-UPPER"), oid("T-LOWER")})
            )
            reverse_type = "composes" if checked else "logical_decomposition"
            proof_edges.extend([
                edge(req, parent, "proof_requires", child, reverse),
                edge(reverse, child, reverse_type, parent, req),
            ])
            if not checked:
                unverified_plans.append({
                    "parent_obligation_id": parent,
                    "child_obligation_id": child,
                    "status": "source-shaped or planned relation; exact child-to-parent Lean composition remains open",
                })

    def edges(prefix: str, edge_type: str, pairs: list[tuple[str, str]]) -> list[dict]:
        return [edge(f"{prefix}{index:03d}", source, edge_type, target)
                for index, (source, target) in enumerate(pairs, 1)]

    overlay_ids = {oid("S-FOUNDATION"), oid("X-SOURCE"), oid("X-PROVENANCE"),
                   oid("X-TRUST"), oid("X-READABLE"), oid("X-WORKFLOW")}
    substantive_ids = [identifier for identifier in ids if identifier not in overlay_ids]
    graph_edges = {
        "proof": proof_edges,
        "refinement": edges("R", "logical_decomposition", [
            (oid("ROOT"), oid("S-TARGET")), (oid("ROOT"), oid("S-REPRESENTATION")),
            (oid("ROOT"), oid("S-BIPARTITE")), (oid("ROOT"), oid("S-COLORING")),
            (oid("ROOT"), oid("S-BOUNDARY")), (oid("ROOT"), oid("S-TRANSPORT")),
            (oid("ROOT"), oid("S-FOUNDATION")), (oid("T-UPPER"), oid("N-BOUNDED")),
        ]),
        "provenance": edges("S", "source_map", [
            (identifier, oid("X-SOURCE")) for identifier in substantive_ids
            if by_id[identifier]["human_source_eligibility"] == "required"
        ]) + edges("V", "provenance_of", [
            (oid("X-PROVENANCE"), oid("S-TARGET")),
            (oid("X-PROVENANCE"), oid("S-REPRESENTATION")),
            (oid("X-PROVENANCE"), oid("T-ASSEMBLE")),
        ]),
        "evidence": [],
        "trust": edges("T", "trusts", [
            (oid("ROOT"), oid("S-FOUNDATION")), (oid("ROOT"), oid("X-TRUST")),
            (oid("T-ASSEMBLE"), oid("X-TRUST")), (oid("S-REPRESENTATION"), oid("X-TRUST")),
        ]),
        "documentation": edges("D", "documents", [
            (oid("X-READABLE"), identifier) for identifier in ids if identifier != oid("X-READABLE")
        ]),
        "workflow": edges("W", "workflow_depends_on", [
            (ITEM, "S56-M-0861-ANCHOR_AUDIT"),
            ("S56-M-0861-PROOF", ITEM),
            ("S56-M-0861-VALIDATION", "S56-M-0861-PROOF"),
            ("S56-M-0861-RELEASE", "S56-M-0861-VALIDATION"),
        ]),
    }
    workflow_tasks = [
        "S56-M-0861-ANCHOR_AUDIT", ITEM, "S56-M-0861-PROOF",
        "S56-M-0861-VALIDATION", "S56-M-0861-RELEASE",
    ]
    graphs = {}
    for name, values in graph_edges.items():
        endpoints = workflow_tasks if name == "workflow" else ids
        graphs[name] = graph(endpoints, values)

    bundle = {
        "schema_version": "stage1-typed-graphs/1.0",
        "item_id": ITEM,
        "theorem_id": THEOREM,
        "registry_id": registry["registry_id"],
        "registry_denominator_sha256": denominator,
        "root_node_id": oid("ROOT"),
        "edge_endpoint_namespace": "canonical obligation_id except workflow task IDs",
        "edge_direction": "Proof requirements run parent to child. Only a kernel-checked reverse relation is composes; source-shaped unchecked reverse relations are logical_decomposition. Workflow runs task to prerequisite.",
        "workflow_task_nodes": workflow_tasks,
        "nodes": nodes,
        "graphs": graphs,
        "composition_certificates": [{
            "certificate_id": "COMP-M0861-ROOT",
            "parent_obligation_id": oid("ROOT"),
            "parent_statement_fingerprint": by_id[oid("ROOT")]["statement_fingerprint"],
            "child_obligation_ids": [oid("S-TRANSPORT"), oid("T-ASSEMBLE")],
            "declarations": [
                "Stage1Instances.THM_M_0861_Obligations.checked_root_transport",
                "Stage1Instances.THM_M_0861_Obligations.expanded_of_assembly",
                "Stage1Instances.THM_M_0861_Obligations.root_of_assembly",
            ],
            "kind": "Lean abstract-child harness",
            "status": "provisional kernel-checked conditional composition; bundled assembly remains open",
        }, {
            "certificate_id": "COMP-M0861-T-ASSEMBLE",
            "parent_obligation_id": oid("T-ASSEMBLE"),
            "parent_statement_fingerprint": by_id[oid("T-ASSEMBLE")]["statement_fingerprint"],
            "child_obligation_ids": [oid("T-UPPER"), oid("T-LOWER")],
            "declarations": [
                "Stage1Instances.THM_M_0861_Obligations.assembly_of_upper_and_lower",
            ],
            "kind": "Lean abstract-child harness",
            "status": "provisional kernel-checked conditional composition; both children remain open",
        }],
        "unverified_decomposition_plans": unverified_plans,
        "closure_boundary": {
            "provisionally_checked_interfaces": sorted(CHECKED_INTERFACES),
            "accepted_closed_obligations": [],
            "root_closed": False,
            "authoritative_root_vector": {"H": "H1", "M": "M4", "R": "R4"},
            "audit_complete": False,
            "theorem_complete": False,
            "minimal_open_proof_cut_set": [oid("T-UPPER"), oid("T-LOWER")],
            "remaining_release_cut_set": [
                oid("T-UPPER"), oid("T-LOWER"), oid("X-SOURCE"), oid("S-FOUNDATION"),
                oid("X-PROVENANCE"), oid("X-TRUST"), oid("X-READABLE"), oid("X-WORKFLOW"),
            ],
            "reason": "No exact formal proof body was located. All Satz C, lower-bound, source, readability, provenance, trust, validation, and release work remains open; the conditional harness supplies no child proof.",
        },
    }

    recipes = []
    for node in nodes:
        declarations = []
        if node["obligation_id"] in {oid("ROOT"), oid("T-ASSEMBLE")}:
            declarations = [
                "Stage1Instances.THM_M_0861.KonigEdgeColoringTarget",
                "Stage1Instances.THM_M_0861_Obligations.RootTransportTarget",
                "Stage1Instances.THM_M_0861_Obligations.AssemblyTarget",
                "Stage1Instances.THM_M_0861_Obligations.assembly_of_upper_and_lower",
                "Stage1Instances.THM_M_0861_Obligations.expanded_of_assembly",
                "Stage1Instances.THM_M_0861_Obligations.checked_root_transport",
                "Stage1Instances.THM_M_0861_Obligations.root_of_assembly",
                "Stage1Instances.THM_M_0861_Obligations.root_of_upper_and_lower",
            ]
        elif node["obligation_id"] == oid("N-BOUNDED"):
            declarations = [
                "Stage1Instances.THM_M_0861_Obligations.DegreeBound",
                "Stage1Instances.THM_M_0861_Obligations.BoundedSatzCTarget",
            ]
        elif node["obligation_id"] in {oid("T-UPPER"), oid("T-LOWER")}:
            declarations = [node["formal_target"]]
        recipes.append({
            "recipe_id": node["validation_spec_id"],
            "cwd": ".",
            "argv": ["python3", "-B", f"Stage1_Instances/{THEOREM}/check_obligation_tree.py"],
            "env_allowlist": {
                "PATH": "runner-provided tool path",
                "HOME": "runner-provided toolchain home",
                "TMPDIR": "runner-provided temporary directory",
                "PYTHONDONTWRITEBYTECODE": "1",
            },
            "timeout_seconds": 180,
            "network_policy": "denied",
            "expected_exit": 0,
            "expected_outputs": [{
                "path_or_stream": "stdout",
                "semantic_hash_policy": "contains exact PASS counts, recomputed denominator, open root H1/M4/R4, and theorem_complete=false",
            }],
            "covered_obligation_ids": [node["obligation_id"]],
            "covered_declarations": declarations,
        })
    specs = {
        "schema_version": "stage1-validation-specs/1.0",
        "item_id": ITEM,
        "theorem_id": THEOREM,
        "registry_denominator_sha256": denominator,
        "recipes": recipes,
        "status_boundary": "These worker recipes validate the frozen architecture and conditional Lean interface only. Recipes with no covered declaration do not claim kernel closure of their open mathematical node.",
    }
    return registry, bundle, specs


def main() -> None:
    registry, bundle, specs = build()
    for filename, value in (
        ("obligation-registry.json", registry),
        ("typed-graphs.json", bundle),
        ("validation-specs.json", specs),
    ):
        (HERE / filename).write_text(
            json.dumps(value, indent=2, ensure_ascii=True) + "\n", encoding="utf-8"
        )
    edge_count = sum(len(value["edges"]) for value in bundle["graphs"].values())
    print(
        f"built {len(registry['obligations'])} obligations and {edge_count} typed edges; "
        f"denominator {registry['denominator_sha256']}"
    )


if __name__ == "__main__":
    main()
