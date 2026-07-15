#!/usr/bin/env python3
"""Build the frozen THM-M-0841 obligation registry and typed graph bundle."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ITEM = "S56-M-0841-OBLIGATION_TREE"
THEOREM = "THM-M-0841"
PREFIX = "M0841"
ROOT_EXPRESSION = "ed4a8b422615bfafc69ab9f770dc99b77d308d78bca30e67790206426799a733"
GRAPH_NAMES = (
    "proof", "refinement", "provenance", "evidence", "trust", "documentation", "workflow",
)
STRUCTURE_RECIPE = "VAL-M0841-OBLIGATION-STRUCTURE"
LEAN_RECIPE = "VAL-M0841-OBLIGATION-LEAN"


def digest(value: object) -> str:
    encoded = json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=True
    ).encode()
    return hashlib.sha256(encoded).hexdigest()


def oid(short: str) -> str:
    return f"{PREFIX}-{short}"


def spec(
    short: str,
    kind: str,
    risk: str,
    claim: str,
    formal: str,
    output: str,
    source: str,
    budget: int,
    machine: str = "required",
    human_source: str = "required",
    readable: str = "required",
    body: str | None = None,
) -> dict[str, object]:
    return {
        "id": oid(short),
        "kind": kind,
        "risk": risk,
        "claim": claim,
        "formal": formal,
        "output": output,
        "source": source,
        "budget": budget,
        "machine": machine,
        "human_source": human_source,
        "readable": readable,
        "body": body,
    }


# Architecture only: these rows deliberately carry no candidate status or closure observation.
SPECS = (
    spec("ROOT", "root", "critical", "Prove the exact page-1087 sparse complementary-graph Erdos-Stone target.", "Stage1Instances.THM_M_0841.ErdosStoneTarget", "The exact frozen canonical proposition.", "Erdos-Stone-1946:p1087:theorem", 12),
    spec("S-TARGET", "definition", "critical", "Preserve the exact epsilon, r, n0, n, graph, edge-bound, part-size, and containment binders.", "Stage1Instances.THM_M_0841.ErdosStoneTarget", "The unchanged elaborated root interface.", "Statement.lean:29-40", 20, human_source="not_applicable"),
    spec("S-DEFINITIONS", "definition", "high", "Freeze finite simple graphs, graph complement, non-induced containment, complete equipartite graphs, and the iterated logarithm.", "iteratedLog; SimpleGraph.completeEquipartiteGraph; SimpleGraph.IsContained; SimpleGraph.compl", "The exact mathematical vocabulary used by both source forms.", "Statement.lean:17-40; Erdos-Stone-1946:p1087:definitions", 24),
    spec("S-DOMAIN", "definition", "high", "Retain all natural/real coercions, labeled Fin n vertices, local decidable adjacency, and strict ordered binders.", "the binder context of ErdosStoneTarget", "A closed Prop in universe zero with no hidden finiteness or decidability premise.", "Statement.lean:29-40; statement.json:ordered_binders", 22, human_source="not_applicable"),
    spec("S-BOUNDARY", "branch", "high", "Retain 0 < epsilon < 1, r >= 2, positive n0 and k, n > n0, and strict sparse edge inequality.", "the boundary premises of ErdosStoneTarget", "No admitted endpoint, zero part size, or weak threshold substitution.", "Statement.lean:29-40,123-143; Erdos-Stone-1946:p1087", 20),
    spec("S-EXPANDED-TRANSPORT", "transport", "normal", "Unfold the local iteratedLog notation without changing any binder or conclusion.", "Stage1Instances.THM_M_0841.erdosStoneTarget_iff_expandedSourceTarget", "The checked source-expanded spelling.", "Statement.lean:42-59", 12, human_source="not_applicable", body="local:Statement.lean#erdosStoneTarget_iff_expandedSourceTarget"),
    spec("S-COMPLEMENT-TRANSPORT", "transport", "critical", "Convert the sparse edge upper bound into a dense complement lower bound with explicit tolerance slack and the n.choose 2 correction.", "Stage1Instances.THM_M_0841_Obligations.SparseFromDense", "The exact sparse root from the complete dense indexed family.", "Erdos-Stone-1946:pp1087-1088; source-statement-crosswalk.md", 48),
    spec("S-FOUNDATION", "certificate", "critical", "Account for classical choice, quotient soundness, propositional extensionality, imports, compiled artifacts, and the no-oracle policy.", "planned transitive foundation and TCB report", "An accepted logical-foundation and trusted-computing boundary.", "AnchorAudit.lean:52-62; anchor-audit.json:immutable_environment", 28, human_source="not_applicable"),
    spec("N-DENSE-FORM", "normalization", "critical", "State the page-1088 complete cross-group dense formulation as an indexed family DenseClaim r.", "Stage1Instances.THM_M_0841_Obligations.DenseClaim", "A dense complete-equipartite containment claim for each r >= 2.", "ObligationTree.lean:DenseClaim; Erdos-Stone-1946:p1088", 26),
    spec("N-THRESHOLD-PACKAGE", "normalization", "high", "Combine all finite eventual-size requirements into one positive natural threshold without changing strict n > n0.", "planned signature: finite maximum of positivity, logarithm, induction, and counting thresholds", "One threshold satisfying every later large-n side condition.", "Erdos-Stone-1946:pp1088-1090:large-enough clauses", 34),
    spec("N-LOG-ROUNDING", "normalization", "critical", "Control iterated-log domains, natural floor/ceiling conventions, q and k positivity, and all integer inequalities.", "planned exact q/k floor-ceil package", "Legal positive natural part sizes matching the printed bounds.", "Erdos-Stone-1946:pp1087-1089", 48),
    spec("N-PART-SIZE-STABILITY", "normalization", "critical", "Show that the fixed k selected from n remains permitted when the final graph has n(1-d) vertices and d stays bounded away from one.", "planned iterated-log stability under a constant-factor decrease of n", "The same k is admissible in the final c+delta application.", "Erdos-Stone-1946:pp1089-1090:same-q-k assertion", 72),
    spec("N-ASYMPTOTICS", "normalization", "critical", "Prove q=o(n), k/log q -> 0, q powers versus n bounds, and every eventual numerical estimate used by deletion.", "planned finite threshold package for all asymptotic inequalities", "Concrete inequalities at every chosen n above the joint threshold.", "Erdos-Stone-1946:pp1088-1090", 78),
    spec("L-INTERSECTION-LEMMA", "core_lemma", "critical", "Among N subsets of an n-element set, each of size at least p, find at least N*C(p,k)/C(n,k) sharing at least k elements.", "planned finite-family intersection lemma with multiplicities", "The exact p1087 combinatorial lemma.", "Erdos-Stone-1946:pp1087-1088:lemma", 88),
    spec("L-INTERSECTION-DOUBLE-COUNT", "core_lemma", "critical", "Choose p-subsets, double-count contained k-subsets, and compare their maximum fiber multiplicity with the original family.", "planned Finset/Fintype double-counting signature", "N*C(p,k) <= M*C(n,k).", "Erdos-Stone-1946:p1088:lemma-proof", 64),
    spec("L-INTERSECTION-RATIO", "core_lemma", "high", "Derive M/N >= ((p-k+1)/n)^k from the binomial-coefficient ratio.", "planned exact ordered-field corollary", "The source's Corollary 1.", "Erdos-Stone-1946:p1088:Corollary-1", 42),
    spec("L-INTERSECTION-LOG", "core_lemma", "critical", "Under p >= alpha*n and k <= alpha*log n, derive M/N >= n^(-3/4) with all positivity and rounding hypotheses.", "planned exact real/natural logarithmic corollary", "The source's Corollary 2.", "Erdos-Stone-1946:p1088:Corollary-2", 68),
    spec("B-R-TWO", "branch", "critical", "Prove DenseClaim 2 by the high-degree neighborhood argument.", "Stage1Instances.THM_M_0841_Obligations.DenseBase", "The exact dense two-part base case.", "Erdos-Stone-1946:p1088:r=2", 24),
    spec("C-HIGH-DEGREE", "construction", "high", "Form the vertices of degree at least epsilon*n/2 and their neighborhood family.", "planned Finset of high-degree vertices and neighborFinset map", "N indexed subsets of Fin n, each large enough for Corollary 2.", "Erdos-Stone-1946:p1088:r=2", 42),
    spec("L-HIGH-DEGREE-COUNT", "core_lemma", "critical", "Use the total edge lower bound and low-degree bound to prove N > epsilon*n/2.", "planned degree-sum inequality", "A linear lower bound on the number of high-degree vertices.", "Erdos-Stone-1946:p1088:r=2", 54),
    spec("L-BASE-COMMON", "core_lemma", "critical", "Apply the logarithmic intersection corollary to the high-degree neighborhoods.", "planned specialization of M0841-L-INTERSECTION-LOG", "Many high-degree vertices share at least floor(epsilon*log n/2) neighbors.", "Erdos-Stone-1946:p1088:r=2", 36),
    spec("L-BASE-SIZE", "core_lemma", "critical", "Prove N/n^(3/4) > k and floor(epsilon*log n/2) >= k for k=ceil(sqrt(log n)).", "planned exact eventual numerical package", "Enough distinct vertices on both sides of the bipartite copy.", "Erdos-Stone-1946:p1088:r=2", 62),
    spec("T-BASE-ASSEMBLE", "terminal", "critical", "Choose distinct P and R vertices and package their cross adjacency as completeEquipartiteGraph 2 k containment.", "planned exact DenseBase proof terminal", "Stage1Instances.THM_M_0841_Obligations.DenseBase.", "Erdos-Stone-1946:p1088:r=2", 44),
    spec("B-R-GE-THREE", "branch", "critical", "Prove the strong-induction step DenseClaim r for every r >= 3.", "Stage1Instances.THM_M_0841_Obligations.DenseStep", "The exact dense induction-step package.", "Erdos-Stone-1946:pp1088-1090:r>=3", 30),
    spec("C-ADMISSIBLE", "construction", "critical", "Define admissible tolerances for the fixed r and set c to their greatest lower bound.", "planned admissibility set and sInf package", "The critical tolerance c used by contradiction.", "Erdos-Stone-1946:p1088", 52),
    spec("L-ADMISSIBLE-BOUNDS", "core_lemma", "critical", "Show admissibility is nonempty and 0 <= c <= 1/(2(r-1)); the endpoint is vacuous.", "planned order-theoretic bounds on sInf", "A bounded critical tolerance with an explicit contradiction ceiling.", "Erdos-Stone-1946:p1088", 58),
    spec("B-C-ZERO", "branch", "high", "If c=0, use upward closure of admissibility to prove every positive tolerance.", "planned zero-infimum branch", "DenseClaim r.", "Erdos-Stone-1946:p1088", 34),
    spec("B-C-POSITIVE", "branch", "critical", "Assume c>0, choose 0<delta<c/(2r), and derive a contradiction.", "planned positive-infimum branch", "False, eliminating c>0.", "Erdos-Stone-1946:pp1088-1090", 28),
    spec("C-COUNTEREXAMPLE", "construction", "critical", "Use nonadmissibility of c-delta to choose arbitrarily large dense graphs without the required r-partite copy.", "planned counterexample extraction above every threshold", "A large graph G at density c-delta with no K_r(k).", "Erdos-Stone-1946:p1089", 44),
    spec("C-IH-BLOCKS", "construction", "critical", "Apply the r-1 induction hypothesis at the printed auxiliary tolerance to find r-1 groups of 2q vertices.", "planned DenseClaim (r-1) specialization", "r-1 mutually complete blocks and chosen q-subblocks.", "Erdos-Stone-1946:p1089", 58),
    spec("C-RICH-VERTICES", "construction", "critical", "Select remaining vertices adjacent to at least (r-2)q+kq/log q block vertices.", "planned rich-vertex Finset", "A set of N possible vertices for the final part.", "Erdos-Stone-1946:p1089", 40),
    spec("L-RICH-EACH-PART", "core_lemma", "high", "Show each rich vertex has at least kq/log q neighbors in every one of the r-1 blocks.", "planned pigeonhole estimate over block degrees", "The per-block density premise for repeated Corollary 2.", "Erdos-Stone-1946:p1089", 38),
    spec("L-ITERATED-INTERSECTION", "core_lemma", "critical", "Apply the logarithmic intersection corollary successively through all r-1 blocks.", "planned r-1-fold common-fiber construction", "At least N/(q^(3/4))^(r-1) vertices share k neighbors in every block.", "Erdos-Stone-1946:p1089", 74),
    spec("L-RICH-CARD-BOUND", "core_lemma", "critical", "Use absence of the target copy and asymptotics to prove N < k*q^(3(r-1)/4) < n^(1/2) < n*k/log q.", "planned exact rich-vertex cardinal chain", "The sharp N bound used in the deleted-edge estimate.", "Erdos-Stone-1946:p1089", 62),
    spec("C-DELETE-BLOCK", "construction", "high", "Delete q(r-1) selected block vertices and every incident edge.", "planned induced remainder graph construction", "The next graph G_(t+1) with n-q(r-1) vertices.", "Erdos-Stone-1946:p1089", 36),
    spec("L-DELETED-EDGE-BOUND", "core_lemma", "critical", "Bound the deleted edges by the exact three-term expression and then by n*q*(r-2)*(1+delta).", "planned finite edge partition and arithmetic estimate", "A per-round loss bound.", "Erdos-Stone-1946:p1089", 84),
    spec("C-DELETION-SEQUENCE", "construction", "critical", "Iterate the block-deletion construction while its density and large-n hypotheses survive.", "planned finite sequence of induced graphs", "Graphs G_t with fixed q and k and accumulated loss bounds.", "Erdos-Stone-1946:pp1089-1090", 70),
    spec("L-DELETION-INVARIANT", "core_lemma", "critical", "Prove every intermediate graph remains large enough and above the r-1 induction density with the same q and k.", "planned sequence invariant", "Legality of every scheduled deletion round.", "Erdos-Stone-1946:pp1089-1090", 88),
    spec("C-STEP-COUNT", "construction", "high", "Set s=floor(c*n/((r-1)q)) and d=(r-1)q*s/n.", "planned natural step count and real ratio", "The number of rounds and removed-vertex fraction.", "Erdos-Stone-1946:p1090", 40),
    spec("L-S-ROUNDS", "core_lemma", "critical", "Show at least s rounds run, removed vertices are at most cn<=n/4, and total lost edges obey the printed bound.", "planned induction on the deletion sequence", "A final graph with at least 3n/4 vertices and controlled edge loss.", "Erdos-Stone-1946:p1090", 72),
    spec("L-D-LIMIT", "core_lemma", "critical", "Establish 0<d<=c and d tends to c along the arbitrarily large counterexamples.", "planned floor-error and limit argument", "Replacement of d by c in the final limiting inequality.", "Erdos-Stone-1946:p1090", 54),
    spec("L-TAIL-ADMISSIBLE", "core_lemma", "critical", "Apply admissibility of c+delta to the final graph, using the same-k part-size stability bridge.", "planned final-remainder upper bound", "An upper edge bound at tolerance c+delta for G_s.", "Erdos-Stone-1946:p1090", 66),
    spec("L-GLOBAL-EDGE-INEQUALITY", "core_lemma", "critical", "Combine the counterexample lower density, final admissible upper density, and total deleted-edge bound.", "planned exact real inequality before limits", "The source's displayed inequality in n, c, delta, and d.", "Erdos-Stone-1946:p1090", 58),
    spec("L-LIMIT-PASSAGE", "core_lemma", "critical", "First send n to infinity so d tends to c, then send delta to zero without reversing a strict boundary.", "planned two-stage limiting argument", "The limiting algebraic inequality for c.", "Erdos-Stone-1946:p1090", 60),
    spec("L-ALGEBRA-CONTRADICTION", "core_lemma", "critical", "Simplify the limiting inequality to contradict c<=1/(2(r-1))<=1/4.", "planned exact ordered-field arithmetic conclusion", "False under c>0.", "Erdos-Stone-1946:p1090", 38),
    spec("T-INDUCTIVE-ASSEMBLE", "terminal", "critical", "Combine the c=0 and c>0 branches and discharge the strong-induction step.", "planned exact DenseStep proof terminal", "Stage1Instances.THM_M_0841_Obligations.DenseStep.", "Erdos-Stone-1946:pp1088-1090", 40),
    spec("T-DENSE-ASSEMBLE", "terminal", "critical", "Use strong induction to combine DenseBase and DenseStep into the complete indexed dense family.", "Stage1Instances.THM_M_0841_Obligations.denseFamily_compose", "Stage1Instances.THM_M_0841_Obligations.DenseFamily.", "ObligationTree.lean:denseFamily_compose", 18, body="local:ObligationTree.lean#denseFamily_compose"),
    spec("T-ROOT-COMPOSE", "terminal", "critical", "Consume the assembled dense family and exact sparse-from-dense transport to produce the frozen root.", "Stage1Instances.THM_M_0841_Obligations.sparse_compose", "Stage1Instances.THM_M_0841.ErdosStoneTarget.", "ObligationTree.lean:sparse_compose", 16, body="local:ObligationTree.lean#sparse_compose"),
    spec("X-SOURCE", "terminal", "critical", "Map every material proof node to pages 1087-1090, corrections, assumptions, and independent review.", "planned primary-source node crosswalk", "Human-source evidence without machine proof credit.", "source-statement-crosswalk.md; Erdos-Stone-1946:pp1087-1090", 42, machine="not_applicable"),
    spec("X-PROVENANCE", "certificate", "critical", "Bind future proof bodies, wrappers, imports, revisions, source hashes, licenses, and terminal origins without duplicate credit.", "planned content-addressed provenance packet", "Release provenance without mathematical proof credit.", "anchor-audit.json:candidates", 40, machine="informational", human_source="not_applicable", readable="not_applicable"),
    spec("X-TRUST", "certificate", "critical", "Close imported olean, executable, axiom, unsafe/oracle, computation, hermetic replay, and independent-verification boundaries.", "planned transitive trust and TCB closure", "Release trust evidence without mathematical proof credit.", "anchor-audit.json:immutable_environment", 42, machine="informational", human_source="not_applicable", readable="not_applicable"),
    spec("X-READABLE", "terminal", "high", "Produce a complete node-anchored reconstruction and independent combinatorics review.", "planned readable reconstruction", "Readable coverage without machine proof credit.", "future readable proof surface", 48, machine="not_applicable", human_source="not_applicable"),
    spec("X-WORKFLOW", "certificate", "high", "Bind proof, validation, release, freshness, revocation, and independent-verification tasks.", "planned Stage1 workflow receipts", "Workflow acceptance without proof credit.", "task-dag.json and future accepted receipts", 28, machine="informational", human_source="not_applicable", readable="not_applicable"),
)


PROOF_PAIRS = (
    ("ROOT", "T-ROOT-COMPOSE", "composes"),
    ("T-ROOT-COMPOSE", "T-DENSE-ASSEMBLE", "composes"),
    ("T-ROOT-COMPOSE", "S-COMPLEMENT-TRANSPORT", "composes"),
    ("T-DENSE-ASSEMBLE", "B-R-TWO", "composes"),
    ("T-DENSE-ASSEMBLE", "B-R-GE-THREE", "composes"),
    ("B-R-TWO", "T-BASE-ASSEMBLE", "logical_decomposition"),
    ("T-BASE-ASSEMBLE", "C-HIGH-DEGREE", "logical_decomposition"),
    ("T-BASE-ASSEMBLE", "L-BASE-COMMON", "logical_decomposition"),
    ("T-BASE-ASSEMBLE", "L-BASE-SIZE", "logical_decomposition"),
    ("C-HIGH-DEGREE", "L-HIGH-DEGREE-COUNT", "logical_decomposition"),
    ("L-BASE-COMMON", "L-INTERSECTION-LOG", "logical_decomposition"),
    ("L-INTERSECTION-LOG", "L-INTERSECTION-RATIO", "logical_decomposition"),
    ("L-INTERSECTION-RATIO", "L-INTERSECTION-LEMMA", "logical_decomposition"),
    ("L-INTERSECTION-LEMMA", "L-INTERSECTION-DOUBLE-COUNT", "logical_decomposition"),
    ("B-R-GE-THREE", "T-INDUCTIVE-ASSEMBLE", "logical_decomposition"),
    ("T-INDUCTIVE-ASSEMBLE", "C-ADMISSIBLE", "logical_decomposition"),
    ("T-INDUCTIVE-ASSEMBLE", "B-C-ZERO", "logical_decomposition"),
    ("T-INDUCTIVE-ASSEMBLE", "B-C-POSITIVE", "logical_decomposition"),
    ("C-ADMISSIBLE", "L-ADMISSIBLE-BOUNDS", "logical_decomposition"),
    ("B-C-POSITIVE", "C-COUNTEREXAMPLE", "logical_decomposition"),
    ("B-C-POSITIVE", "C-IH-BLOCKS", "logical_decomposition"),
    ("B-C-POSITIVE", "C-DELETION-SEQUENCE", "logical_decomposition"),
    ("B-C-POSITIVE", "L-GLOBAL-EDGE-INEQUALITY", "logical_decomposition"),
    ("B-C-POSITIVE", "L-LIMIT-PASSAGE", "logical_decomposition"),
    ("B-C-POSITIVE", "L-ALGEBRA-CONTRADICTION", "logical_decomposition"),
    ("C-COUNTEREXAMPLE", "N-THRESHOLD-PACKAGE", "logical_decomposition"),
    ("C-IH-BLOCKS", "N-LOG-ROUNDING", "logical_decomposition"),
    ("C-IH-BLOCKS", "N-ASYMPTOTICS", "logical_decomposition"),
    ("C-DELETION-SEQUENCE", "C-RICH-VERTICES", "logical_decomposition"),
    ("C-DELETION-SEQUENCE", "C-DELETE-BLOCK", "logical_decomposition"),
    ("C-DELETION-SEQUENCE", "L-DELETION-INVARIANT", "logical_decomposition"),
    ("C-DELETION-SEQUENCE", "C-STEP-COUNT", "logical_decomposition"),
    ("C-DELETION-SEQUENCE", "L-S-ROUNDS", "logical_decomposition"),
    ("C-RICH-VERTICES", "L-RICH-EACH-PART", "logical_decomposition"),
    ("C-RICH-VERTICES", "L-ITERATED-INTERSECTION", "logical_decomposition"),
    ("C-RICH-VERTICES", "L-RICH-CARD-BOUND", "logical_decomposition"),
    ("L-ITERATED-INTERSECTION", "L-INTERSECTION-LOG", "logical_decomposition"),
    ("L-RICH-CARD-BOUND", "N-ASYMPTOTICS", "logical_decomposition"),
    ("C-DELETE-BLOCK", "L-DELETED-EDGE-BOUND", "logical_decomposition"),
    ("L-DELETED-EDGE-BOUND", "L-RICH-CARD-BOUND", "logical_decomposition"),
    ("L-DELETION-INVARIANT", "N-PART-SIZE-STABILITY", "logical_decomposition"),
    ("L-DELETION-INVARIANT", "N-ASYMPTOTICS", "logical_decomposition"),
    ("L-S-ROUNDS", "L-DELETED-EDGE-BOUND", "logical_decomposition"),
    ("L-GLOBAL-EDGE-INEQUALITY", "L-S-ROUNDS", "logical_decomposition"),
    ("L-GLOBAL-EDGE-INEQUALITY", "L-D-LIMIT", "logical_decomposition"),
    ("L-GLOBAL-EDGE-INEQUALITY", "L-TAIL-ADMISSIBLE", "logical_decomposition"),
    ("L-TAIL-ADMISSIBLE", "N-PART-SIZE-STABILITY", "logical_decomposition"),
    ("L-LIMIT-PASSAGE", "L-D-LIMIT", "logical_decomposition"),
    ("S-COMPLEMENT-TRANSPORT", "N-DENSE-FORM", "logical_decomposition"),
    ("S-COMPLEMENT-TRANSPORT", "N-THRESHOLD-PACKAGE", "logical_decomposition"),
)


CHECKED_PARENTS = {
    oid("ROOT"): "Stage1Instances.THM_M_0841_Obligations.root_of_terminal",
    oid("T-ROOT-COMPOSE"): "Stage1Instances.THM_M_0841_Obligations.sparse_compose",
    oid("T-DENSE-ASSEMBLE"): "Stage1Instances.THM_M_0841_Obligations.denseFamily_compose",
}
CHECKED_INTERFACES = {
    oid("ROOT"), oid("T-ROOT-COMPOSE"), oid("T-DENSE-ASSEMBLE"), oid("B-R-TWO"),
    oid("B-R-GE-THREE"), oid("S-COMPLEMENT-TRANSPORT"), oid("N-DENSE-FORM"),
}


def exclusion(row: dict[str, object]) -> dict[str, str] | None:
    if row["machine"] == row["human_source"] == row["readable"] == "required":
        return None
    if row["id"] == oid("X-SOURCE"):
        code = "human_source_boundary_only"
        reason = "This node carries source review and never receives machine proof credit."
    elif row["id"] == oid("X-READABLE"):
        code = "readability_boundary_only"
        reason = "This node carries readable reconstruction and never receives proof credit."
    elif row["machine"] == "required":
        code = "formal_interface_not_separate_human_claim"
        reason = "This formal statement or foundation interface is not a separate source theorem."
    else:
        code = "assurance_overlay_no_proof_credit"
        reason = "This assurance overlay is informational for mathematical proof coverage."
    return {
        "code": code,
        "justification": reason,
        "approval": "pending independent Stage1 integration review",
    }


def graph(edges: list[dict[str, object]], endpoints: list[str]) -> dict[str, object]:
    incoming = {identifier: [] for identifier in endpoints}
    outgoing = {identifier: [] for identifier in endpoints}
    for edge in edges:
        outgoing[str(edge["from"])].append(str(edge["edge_id"]))
        incoming[str(edge["to"])].append(str(edge["edge_id"]))
    return {"edges": edges, "out": outgoing, "in": incoming}


def build() -> tuple[dict, dict, dict, str]:
    statement_hash = hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
    anchor_hash = hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest()
    obligations = []
    for row in SPECS:
        identifier = str(row["id"])
        fingerprint = (
            f"lean-expression-sha256:{ROOT_EXPRESSION}"
            if identifier in {oid("ROOT"), oid("S-TARGET")}
            else "planned:v1:sha256:"
            + digest([identifier, row["kind"], row["claim"], row["formal"], row["output"]])
        )
        obligations.append({
            "obligation_id": identifier,
            "statement_fingerprint": fingerprint,
            "kind": row["kind"],
            "root_relevant": identifier not in {oid("X-PROVENANCE"), oid("X-WORKFLOW")},
            "machine_eligibility": row["machine"],
            "human_source_eligibility": row["human_source"],
            "readable_eligibility": row["readable"],
            "risk_class": row["risk"],
            "exclusion_reason": exclusion(row),
            "terminal_proof_body_id": row["body"],
        })

    fields = (
        "obligation_id", "statement_fingerprint", "kind", "root_relevant",
        "machine_eligibility", "human_source_eligibility", "readable_eligibility",
        "risk_class", "exclusion_reason", "terminal_proof_body_id",
    )
    denominator = digest([{field: row[field] for field in fields} for row in obligations])
    ids = [row["obligation_id"] for row in obligations]
    registry = {
        "schema_version": "stage1-obligation-registry/1.0",
        "normative_profile": "machine-theorem-assurance/1.0",
        "registry_id": "THM-M-0841-OBLIGATIONS-v2",
        "item_id": ITEM,
        "theorem_id": THEOREM,
        "registry_version": 2,
        "frozen_at": "2026-07-15T19:28:00+08:00",
        "freeze_basis": "The exact elaborated page-1087 target and the visible semantic architecture of the immutable 1946 proof determine the registry. Eligibility is fixed by role before candidate or closure status is attached.",
        "freeze_order_boundary": "SPECS and PROOF_PAIRS contain architecture only. Their canonical ten-field projection is hashed before status_observed_after_freeze is added.",
        "frozen_against_statement_sha256": statement_hash,
        "frozen_against_anchor_audit_sha256": anchor_hash,
        "root_obligation_id": oid("ROOT"),
        "denominator_sha256": denominator,
        "canonical_projection_fields": list(fields),
        "frozen_denominators": {
            "inventory": ids,
            "required_machine": [r["obligation_id"] for r in obligations if r["machine_eligibility"] == "required"],
            "required_human_source": [r["obligation_id"] for r in obligations if r["human_source_eligibility"] == "required"],
            "required_readable": [r["obligation_id"] for r in obligations if r["readable_eligibility"] == "required"],
            "informational_overlays": [r["obligation_id"] for r in obligations if r["machine_eligibility"] == "informational"],
        },
        "distinct_terminal_proof_body_ids": sorted({str(r["terminal_proof_body_id"]) for r in obligations if r["terminal_proof_body_id"]}),
        "deduplication_policy": "The conditional wrappers and statement transport retain their actual local body identities but receive no theorem-closure credit. Aliases, wrappers, graph copies, and candidate variants cannot inflate unique semantic or terminal-body coverage.",
        "layer_exclusions": {
            "external_computation": {
                "status": "not_applicable_pending_independent_approval",
                "reason": "The selected source route uses mathematical counting, induction, and limits, not a solver, native evaluator, numerical experiment, external oracle, or certificate.",
                "reviewer": "independent Stage1 integration lane",
            }
        },
        "delta_policy": "Any later target correction, split, merge, exclusion, eligibility, risk, edge role, fingerprint, or terminal-body identity change requires registry version 3 and an append-only old/new ID delta.",
        "append_only_delta": [{
            "from_registry_id": "THM-M-0841-OBLIGATIONS-v1",
            "from_denominator_sha256": "f7e5b07b6580e7933e3e2f0cc320eb120080fafa9ca442737ed0c5beaa29fd56",
            "from_inventory_count": 53,
            "to_registry_id": "THM-M-0841-OBLIGATIONS-v2",
            "to_denominator_sha256": denominator,
            "to_inventory_count": len(ids),
            "added_obligation_ids": [],
            "removed_obligation_ids": [],
            "changed_existing_obligation_ids": [oid("T-ROOT-COMPOSE")],
            "changed_obligations": {
                oid("T-ROOT-COMPOSE"): {
                    "old_statement_fingerprint": "planned:v1:sha256:1fe56018a4d73c16b86bf409c1fa8d2382942c57fd5cab52bdab00ec86cb0d31",
                    "new_statement_fingerprint": next(
                        row["statement_fingerprint"] for row in obligations
                        if row["obligation_id"] == oid("T-ROOT-COMPOSE")
                    ),
                    "old_formal_target": "Stage1Instances.THM_M_0841_Obligations.compose_root",
                    "new_formal_target": "Stage1Instances.THM_M_0841_Obligations.sparse_compose",
                    "old_terminal_proof_body_id": "local:ObligationTree.lean#compose_root",
                    "new_terminal_proof_body_id": "local:ObligationTree.lean#sparse_compose",
                },
            },
            "proof_edge_changes": {
                "removed": [
                    [oid("T-ROOT-COMPOSE"), oid("B-R-TWO")],
                    [oid("T-ROOT-COMPOSE"), oid("B-R-GE-THREE")],
                ],
                "added": [[oid("T-ROOT-COMPOSE"), oid("T-DENSE-ASSEMBLE")]],
            },
            "reason": "Repair the root proof spine so the sparse composition consumes the assembled dense family and every required machine obligation is root-reachable.",
            "status_effect": "No obligation closes and accepted H1/M3/R4 remains unchanged.",
        }],
        "obligations": obligations,
        "status_observed_after_freeze": {
            "interface_checked_obligations": sorted(CHECKED_INTERFACES),
            "candidate_machine_classification": "M3_no_exact_proof_candidate",
            "candidate_evidence_level": "statement_and_support_interfaces_only",
            "candidate_closure_credit": False,
            "accepted_closed_obligations": [],
            "root_machine_debt": "M3",
        },
        "status_boundary": "Frozen architecture only. Conditional interfaces close no mathematical obligation; accepted H1/M3/R4, AUDIT-Z, and theorem completion do not change.",
    }

    children: dict[str, list[str]] = {}
    reverse_types: dict[tuple[str, str], str] = {}
    proof_edges = []
    for parent_short, child_short, reverse_type in PROOF_PAIRS:
        parent, child = oid(parent_short), oid(child_short)
        req, reverse = f"REQ-{parent}-{child}", f"{'CMP' if reverse_type == 'composes' else 'DEC'}-{child}-{parent}"
        proof_edges.extend([
            {"edge_id": req, "from": parent, "type": "proof_requires", "to": child, "reciprocal_edge_id": reverse},
            {"edge_id": reverse, "from": child, "type": reverse_type, "to": parent, "reciprocal_edge_id": req},
        ])
        children.setdefault(parent, []).append(child)
        reverse_types[(parent, child)] = reverse_type

    refinement_edges = [
        {"edge_id": "REF-ROOT-TARGET", "from": oid("ROOT"), "type": "logical_decomposition", "to": oid("S-TARGET")},
        {"edge_id": "REF-TARGET-DEFINITIONS", "from": oid("S-TARGET"), "type": "logical_decomposition", "to": oid("S-DEFINITIONS")},
        {"edge_id": "REF-TARGET-DOMAIN", "from": oid("S-TARGET"), "type": "logical_decomposition", "to": oid("S-DOMAIN")},
        {"edge_id": "REF-TARGET-BOUNDARY", "from": oid("S-TARGET"), "type": "logical_decomposition", "to": oid("S-BOUNDARY")},
        {"edge_id": "REF-TARGET-EXPANDED", "from": oid("S-TARGET"), "type": "transports", "to": oid("S-EXPANDED-TRANSPORT"), "checked_direction": "iff"},
        {"edge_id": "REF-TARGET-FOUNDATION", "from": oid("S-TARGET"), "type": "logical_decomposition", "to": oid("S-FOUNDATION")},
        {"edge_id": "REF-DENSE-FORM", "from": oid("S-COMPLEMENT-TRANSPORT"), "type": "logical_decomposition", "to": oid("N-DENSE-FORM")},
    ]
    provenance_edges = []
    for obligation in obligations:
        identifier = obligation["obligation_id"]
        if identifier != oid("X-SOURCE") and obligation["human_source_eligibility"] == "required":
            provenance_edges.append({"edge_id": f"SOURCE-{identifier}", "from": identifier, "type": "source_map", "to": oid("X-SOURCE")})
        if identifier not in {oid("X-SOURCE"), oid("X-PROVENANCE"), oid("X-TRUST")}:
            provenance_edges.append({"edge_id": f"PROVENANCE-{identifier}", "from": oid("X-PROVENANCE"), "type": "provenance_of", "to": identifier})
    evidence_edges = [
        {"edge_id": f"EVIDENCE-{identifier}", "from": oid("X-PROVENANCE"), "type": "evidence_for", "to": identifier, "accepted": False}
        for identifier in ids if identifier not in {oid("X-SOURCE"), oid("X-PROVENANCE"), oid("X-TRUST")}
    ]
    trust_edges = [
        {"edge_id": "TRUST-ROOT-FOUNDATION", "from": oid("ROOT"), "type": "trusts", "to": oid("S-FOUNDATION")},
        {"edge_id": "TRUST-ROOT-TCB", "from": oid("ROOT"), "type": "trusts", "to": oid("X-TRUST")},
        {"edge_id": "TRUST-PROVENANCE-TCB", "from": oid("X-PROVENANCE"), "type": "trusts", "to": oid("X-TRUST")},
    ]
    documentation_edges = [
        {"edge_id": f"DOCUMENT-{identifier}", "from": oid("X-READABLE"), "type": "documents", "to": identifier}
        for identifier in ids if identifier != oid("X-READABLE")
    ]
    workflow_tasks = [
        "S56-M-0841-ANCHOR_AUDIT", ITEM, "S56-M-0841-PROOF",
        "S56-M-0841-VALIDATION", "S56-M-0841-RELEASE",
    ]
    workflow_edges = [
        {"edge_id": "FLOW-TREE-ANCHOR", "from": ITEM, "type": "workflow_depends_on", "to": "S56-M-0841-ANCHOR_AUDIT"},
        {"edge_id": "FLOW-PROOF-TREE", "from": "S56-M-0841-PROOF", "type": "workflow_depends_on", "to": ITEM},
        {"edge_id": "FLOW-VALIDATION-PROOF", "from": "S56-M-0841-VALIDATION", "type": "workflow_depends_on", "to": "S56-M-0841-PROOF"},
        {"edge_id": "FLOW-RELEASE-VALIDATION", "from": "S56-M-0841-RELEASE", "type": "workflow_depends_on", "to": "S56-M-0841-VALIDATION"},
    ]

    row_by_id = {str(row["id"]): row for row in SPECS}
    nodes = []
    for obligation in obligations:
        identifier = obligation["obligation_id"]
        row = row_by_id[identifier]
        premises = children.get(identifier, ["frozen-formal-context"])
        nodes.append({
            "node_id": f"{THEOREM}-{identifier.removeprefix(PREFIX + '-')}",
            "obligation_id": identifier,
            "kind": row["kind"],
            "human_statement": row["claim"],
            "formal_target": row["formal"],
            "output": row["output"],
            "human_debt": "H1",
            "machine_debt": "M3" if row["machine"] == "required" else "M4",
            "readability_debt": "R4",
            "evidence_ids": [],
            "source_crosswalk_id": "not-applicable" if row["human_source"] == "not_applicable" else "erdos-stone-1946-pp1087-1090-map-v1-pending-review",
            "provenance_id": "conditional-local-composition:v1" if identifier in CHECKED_INTERFACES else "none",
            "foundation_profile": "lean4-mathlib-classical/v1-pending-transitive-review",
            "tcb_profile": "lean-4.29.0+mathlib-8a178386/v1-pending-release-closure",
            "computation_record": "none credited; finite counting and limiting steps require kernel proof",
            "step_budget": row["budget"],
            "semantic_step_ledger": [{
                "step_id": f"STEP-{identifier}-01",
                "premise_ids": premises,
                "inference": row["formal"],
                "source_locator": row["source"],
                "output": row["output"],
                "outgoing_use": "Consumed only by declared proof/refinement edges; this architecture ledger supplies no closure.",
            }],
            "public_readable_target": f"Stage1_Instances/{THEOREM}/obligation-tree.md#{identifier.lower()}",
            "validation_spec_id": LEAN_RECIPE if identifier in CHECKED_INTERFACES else STRUCTURE_RECIPE,
            "status_boundary": "Open architecture obligation; no M0, accepted proof, H0, R0, AUDIT-Z, or theorem completion credit.",
            "task_ids": [ITEM],
            "owned_sources": [f"Stage1_Instances/{THEOREM}/ObligationTree.lean"] if identifier in CHECKED_INTERFACES else [],
            "owner": "THM-M-0841 proof lane",
            "reviewer": "independent Stage1 integration lane",
            "validity": {
                "validated_at": "2026-07-15" if identifier in CHECKED_INTERFACES else None,
                "review_due": "before any proof acceptance and whenever an invalidation input changes",
                "invalidation_inputs": ["Statement.lean", "anchor-audit.json", "registry or graph", "toolchain or dependency pin", "source or assurance review"],
                "revocation_state": "not-accepted",
            },
        })

    obligation_by_id = {row["obligation_id"]: row for row in obligations}
    certificates = []
    for parent, declaration in CHECKED_PARENTS.items():
        child_ids = children.get(parent, [])
        certificates.append({
            "certificate_id": f"COMP-{parent}",
            "parent_obligation_id": parent,
            "parent_statement_fingerprint": obligation_by_id[parent]["statement_fingerprint"],
            "required_child_ids": child_ids,
            "required_child_statement_fingerprints": {child: obligation_by_id[child]["statement_fingerprint"] for child in child_ids},
            "fingerprint_binding_boundary": "The root fingerprint is the statement-phase expression hash; internal child fingerprints are frozen planned signatures pending exact type serialization before proof acceptance.",
            "checked_declaration": declaration,
            "certificate_kind": "lean_abstract_child_harness",
            "status": "provisionally_elaborated_not_accepted",
            "introduces_undeclared_premises": False,
            "accepted": False,
        })
    certificate_parents = set(CHECKED_PARENTS)
    plans = [{
        "plan_id": f"DECOMP-{parent}",
        "parent_obligation_id": parent,
        "planned_child_ids": child_ids,
        "source_declaration": "Erdos and Stone 1946 proof architecture, printed pages 1087-1090",
        "status": "source_body_decomposition_unverified_as_child_to_parent_composition",
        "required_future_certificate": "An exact Lean abstract-child harness must bind these fingerprints and consume every child before parent closure.",
    } for parent, child_ids in children.items() if parent not in certificate_parents]

    bundle = {
        "schema_version": "stage1-typed-graphs/1.0",
        "normative_profile": "machine-theorem-assurance/1.0",
        "item_id": ITEM,
        "theorem_id": THEOREM,
        "registry_id": registry["registry_id"],
        "registry_version": 2,
        "registry_denominator_sha256": denominator,
        "root_node_id": oid("ROOT"),
        "edge_endpoint_namespace": "canonical obligation IDs except workflow task IDs",
        "edge_direction": "proof_requires points parent to child; checked reverse edges are composes; unverified reverse edges are logical_decomposition; workflow points task to prerequisite",
        "workflow_task_nodes": workflow_tasks,
        "nodes": nodes,
        "graphs": {
            "proof": graph(proof_edges, ids),
            "refinement": graph(refinement_edges, ids),
            "provenance": graph(provenance_edges, ids),
            "evidence": graph(evidence_edges, ids),
            "trust": graph(trust_edges, ids),
            "documentation": graph(documentation_edges, ids),
            "workflow": graph(workflow_edges, workflow_tasks),
        },
        "composition_certificates": certificates,
        "unverified_decomposition_plans": plans,
        "closure_boundary": {
            "closed_obligations": [],
            "root_closed": False,
            "accepted_root_machine_debt": "M3",
            "audit_complete": False,
            "theorem_complete": False,
            "proof_leaf_cut_set": sorted(identifier for identifier in ids if identifier not in children and obligation_by_id[identifier]["machine_eligibility"] == "required"),
            "remaining_machine_root_cut_set": [oid("B-R-TWO"), oid("B-R-GE-THREE"), oid("S-COMPLEMENT-TRANSPORT")],
            "remaining_release_cut_set": [oid("X-SOURCE"), oid("S-FOUNDATION"), oid("X-PROVENANCE"), oid("X-TRUST"), oid("X-READABLE"), oid("X-WORKFLOW")],
            "candidate_evidence": "No exact root proof candidate was located; pinned mathlib supplies support interfaces only.",
            "reason": "Only conditional top-level composition is checked. Every mathematical premise and every internal source decomposition remains open.",
        },
    }

    recipes = {
        "schema_version": "stage1-validation-specs/1.0",
        "normative_profile": "machine-theorem-assurance/1.0",
        "item_id": ITEM,
        "theorem_id": THEOREM,
        "recipes": [
            {
                "recipe_id": STRUCTURE_RECIPE,
                "cwd": ".",
                "argv": ["python3", "-B", f"Stage1_Instances/{THEOREM}/check_obligation_tree.py"],
                "env_allowlist": {},
                "timeout_seconds": 120,
                "network_policy": "denied",
                "expected_exit": 0,
                "expected_outputs": [{"path_or_stream": "stdout", "semantic_hash_policy": f"contains PASS {THEOREM} obligation tree"}],
                "covered_obligation_ids": ids,
                "covered_declarations": [],
                "coverage_boundary": "Checks the frozen registry, node schemas, ledgers, typed graph semantics, reachability, mappings, and open status; supplies no proof closure.",
            },
            {
                "recipe_id": LEAN_RECIPE,
                "cwd": ".",
                "argv": ["python3", "-B", f"Stage1_Instances/{THEOREM}/check_obligation_tree.py", "--run-lean"],
                "env_allowlist": {},
                "timeout_seconds": 180,
                "network_policy": "denied",
                "expected_exit": 0,
                "expected_outputs": [{"path_or_stream": "stdout", "semantic_hash_policy": "contains Lean conditional composition: pass and no sorryAx"}],
                "covered_obligation_ids": sorted(CHECKED_INTERFACES),
                "covered_declarations": [
                    "Stage1Instances.THM_M_0841.ErdosStoneTarget",
                    "Stage1Instances.THM_M_0841_Obligations.DenseClaim",
                    "Stage1Instances.THM_M_0841_Obligations.DenseBase",
                    "Stage1Instances.THM_M_0841_Obligations.DenseStep",
                    "Stage1Instances.THM_M_0841_Obligations.DenseFamily",
                    "Stage1Instances.THM_M_0841_Obligations.SparseFromDense",
                    "Stage1Instances.THM_M_0841_Obligations.denseFamily_compose",
                    "Stage1Instances.THM_M_0841_Obligations.sparse_compose",
                    "Stage1Instances.THM_M_0841_Obligations.compose_root",
                    "Stage1Instances.THM_M_0841_Obligations.exactRoot_iff_canonical",
                    "Stage1Instances.THM_M_0841_Obligations.root_of_terminal",
                ],
                "coverage_boundary": "Kernel-checks exact conditional interfaces and top composition only. It supplies none of DenseBase, DenseStep, or SparseFromDense and closes no obligation.",
            },
        ],
    }

    markdown = [
        f"# {THEOREM} frozen obligation architecture", "", f"Item: `{ITEM}`.", "",
        f"Registry version 2 freezes {len(ids)} canonical obligations before proof-phase closure",
        "credit. The proof route follows the immutable 1946 paper from its finite set-family",
        "intersection lemma through the two-part base, the admissible-tolerance induction, repeated",
        "block deletion, and the final limiting contradiction. The sparse-to-dense complement",
        "transport is an explicit required obligation rather than a definitional rewrite.", "",
        "## Proof route", "", "```text",
        "ROOT -> root terminal -> assembled dense family + sparse/dense transport",
        "  base -> high-degree vertices -> common neighborhoods -> K_(k,k)",
        "  step -> admissible infimum -> c=0 or c>0",
        "    c>0 -> counterexample -> (r-1) inductive blocks -> rich vertices",
        "      -> repeated intersection -> one-round deletion -> deletion sequence",
        "      -> final admissible remainder -> edge squeeze -> limiting contradiction",
        "  common engine -> intersection double count -> ratio -> logarithmic corollary",
        "```", "",
        "Only the conditional root/dense-family composition is checked in Lean here. Internal",
        "relations are frozen as unverified source-body decompositions until a later proof task",
        "supplies exact child-to-parent harnesses.", "", "## Node ledger", "",
    ]
    for row in SPECS:
        identifier = str(row["id"])
        markdown.extend([
            f"### {identifier.lower()}", "", str(row["claim"]), "",
            f"Formal target: `{row['formal']}`.", "",
            f"Output: {row['output']}", "",
            f"Source boundary: {row['source']}.", "",
            f"Budget: {row['budget']} substantive steps maximum; structured ledger: 1 recorded step.", "",
        ])
    markdown.extend([
        "## Freeze boundary", "",
        "All accepted machine obligations remain open at `M3`; the assurance-only overlays are",
        "not proof obligations. No exact root proof body was found. The conditional Lean harness",
        "takes the dense base, strong-induction step, and sparse-from-dense bridge as explicit",
        "premises, so it cannot be mistaken for Erdos-Stone proof closure. Primary-source H0, all",
        "internal composition certificates, readable R0, transitive provenance and trust, hermetic",
        "replay, independent verification, AUDIT-Z, and theorem completion remain open. Any scope or",
        "eligibility change requires a successor registry and append-only delta.", "",
    ])
    return registry, bundle, recipes, "\n".join(markdown)


def main() -> None:
    registry, bundle, recipes, markdown = build()
    for name, value in (
        ("obligation-registry.json", registry),
        ("typed-graphs.json", bundle),
        ("validation-specs.json", recipes),
    ):
        (HERE / name).write_text(
            json.dumps(value, indent=2, ensure_ascii=True) + "\n", encoding="utf-8"
        )
    (HERE / "obligation-tree.md").write_text(markdown, encoding="utf-8")
    edge_count = sum(len(graph["edges"]) for graph in bundle["graphs"].values())
    ledger_count = sum(len(node["semantic_step_ledger"]) for node in bundle["nodes"])
    print(
        f"wrote {len(registry['obligations'])} obligations, {edge_count} typed edges, "
        f"and {ledger_count} substantive ledger steps"
    )
    print(f"registry denominator sha256: {registry['denominator_sha256']}")


if __name__ == "__main__":
    main()
