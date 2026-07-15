# THM-M-0841 frozen obligation architecture

Item: `S56-M-0841-OBLIGATION_TREE`.

Registry version 2 freezes 53 canonical obligations before proof-phase closure
credit. The proof route follows the immutable 1946 paper from its finite set-family
intersection lemma through the two-part base, the admissible-tolerance induction, repeated
block deletion, and the final limiting contradiction. The sparse-to-dense complement
transport is an explicit required obligation rather than a definitional rewrite.

## Proof route

```text
ROOT -> root terminal -> assembled dense family + sparse/dense transport
  base -> high-degree vertices -> common neighborhoods -> K_(k,k)
  step -> admissible infimum -> c=0 or c>0
    c>0 -> counterexample -> (r-1) inductive blocks -> rich vertices
      -> repeated intersection -> one-round deletion -> deletion sequence
      -> final admissible remainder -> edge squeeze -> limiting contradiction
  common engine -> intersection double count -> ratio -> logarithmic corollary
```

Only the conditional root/dense-family composition is checked in Lean here. Internal
relations are frozen as unverified source-body decompositions until a later proof task
supplies exact child-to-parent harnesses.

## Node ledger

### m0841-root

Prove the exact page-1087 sparse complementary-graph Erdos-Stone target.

Formal target: `Stage1Instances.THM_M_0841.ErdosStoneTarget`.

Output: The exact frozen canonical proposition.

Source boundary: Erdos-Stone-1946:p1087:theorem.

Budget: 12 substantive steps maximum; structured ledger: 1 recorded step.

### m0841-s-target

Preserve the exact epsilon, r, n0, n, graph, edge-bound, part-size, and containment binders.

Formal target: `Stage1Instances.THM_M_0841.ErdosStoneTarget`.

Output: The unchanged elaborated root interface.

Source boundary: Statement.lean:29-40.

Budget: 20 substantive steps maximum; structured ledger: 1 recorded step.

### m0841-s-definitions

Freeze finite simple graphs, graph complement, non-induced containment, complete equipartite graphs, and the iterated logarithm.

Formal target: `iteratedLog; SimpleGraph.completeEquipartiteGraph; SimpleGraph.IsContained; SimpleGraph.compl`.

Output: The exact mathematical vocabulary used by both source forms.

Source boundary: Statement.lean:17-40; Erdos-Stone-1946:p1087:definitions.

Budget: 24 substantive steps maximum; structured ledger: 1 recorded step.

### m0841-s-domain

Retain all natural/real coercions, labeled Fin n vertices, local decidable adjacency, and strict ordered binders.

Formal target: `the binder context of ErdosStoneTarget`.

Output: A closed Prop in universe zero with no hidden finiteness or decidability premise.

Source boundary: Statement.lean:29-40; statement.json:ordered_binders.

Budget: 22 substantive steps maximum; structured ledger: 1 recorded step.

### m0841-s-boundary

Retain 0 < epsilon < 1, r >= 2, positive n0 and k, n > n0, and strict sparse edge inequality.

Formal target: `the boundary premises of ErdosStoneTarget`.

Output: No admitted endpoint, zero part size, or weak threshold substitution.

Source boundary: Statement.lean:29-40,123-143; Erdos-Stone-1946:p1087.

Budget: 20 substantive steps maximum; structured ledger: 1 recorded step.

### m0841-s-expanded-transport

Unfold the local iteratedLog notation without changing any binder or conclusion.

Formal target: `Stage1Instances.THM_M_0841.erdosStoneTarget_iff_expandedSourceTarget`.

Output: The checked source-expanded spelling.

Source boundary: Statement.lean:42-59.

Budget: 12 substantive steps maximum; structured ledger: 1 recorded step.

### m0841-s-complement-transport

Convert the sparse edge upper bound into a dense complement lower bound with explicit tolerance slack and the n.choose 2 correction.

Formal target: `Stage1Instances.THM_M_0841_Obligations.SparseFromDense`.

Output: The exact sparse root from the complete dense indexed family.

Source boundary: Erdos-Stone-1946:pp1087-1088; source-statement-crosswalk.md.

Budget: 48 substantive steps maximum; structured ledger: 1 recorded step.

### m0841-s-foundation

Account for classical choice, quotient soundness, propositional extensionality, imports, compiled artifacts, and the no-oracle policy.

Formal target: `planned transitive foundation and TCB report`.

Output: An accepted logical-foundation and trusted-computing boundary.

Source boundary: AnchorAudit.lean:52-62; anchor-audit.json:immutable_environment.

Budget: 28 substantive steps maximum; structured ledger: 1 recorded step.

### m0841-n-dense-form

State the page-1088 complete cross-group dense formulation as an indexed family DenseClaim r.

Formal target: `Stage1Instances.THM_M_0841_Obligations.DenseClaim`.

Output: A dense complete-equipartite containment claim for each r >= 2.

Source boundary: ObligationTree.lean:DenseClaim; Erdos-Stone-1946:p1088.

Budget: 26 substantive steps maximum; structured ledger: 1 recorded step.

### m0841-n-threshold-package

Combine all finite eventual-size requirements into one positive natural threshold without changing strict n > n0.

Formal target: `planned signature: finite maximum of positivity, logarithm, induction, and counting thresholds`.

Output: One threshold satisfying every later large-n side condition.

Source boundary: Erdos-Stone-1946:pp1088-1090:large-enough clauses.

Budget: 34 substantive steps maximum; structured ledger: 1 recorded step.

### m0841-n-log-rounding

Control iterated-log domains, natural floor/ceiling conventions, q and k positivity, and all integer inequalities.

Formal target: `planned exact q/k floor-ceil package`.

Output: Legal positive natural part sizes matching the printed bounds.

Source boundary: Erdos-Stone-1946:pp1087-1089.

Budget: 48 substantive steps maximum; structured ledger: 1 recorded step.

### m0841-n-part-size-stability

Show that the fixed k selected from n remains permitted when the final graph has n(1-d) vertices and d stays bounded away from one.

Formal target: `planned iterated-log stability under a constant-factor decrease of n`.

Output: The same k is admissible in the final c+delta application.

Source boundary: Erdos-Stone-1946:pp1089-1090:same-q-k assertion.

Budget: 72 substantive steps maximum; structured ledger: 1 recorded step.

### m0841-n-asymptotics

Prove q=o(n), k/log q -> 0, q powers versus n bounds, and every eventual numerical estimate used by deletion.

Formal target: `planned finite threshold package for all asymptotic inequalities`.

Output: Concrete inequalities at every chosen n above the joint threshold.

Source boundary: Erdos-Stone-1946:pp1088-1090.

Budget: 78 substantive steps maximum; structured ledger: 1 recorded step.

### m0841-l-intersection-lemma

Among N subsets of an n-element set, each of size at least p, find at least N*C(p,k)/C(n,k) sharing at least k elements.

Formal target: `planned finite-family intersection lemma with multiplicities`.

Output: The exact p1087 combinatorial lemma.

Source boundary: Erdos-Stone-1946:pp1087-1088:lemma.

Budget: 88 substantive steps maximum; structured ledger: 1 recorded step.

### m0841-l-intersection-double-count

Choose p-subsets, double-count contained k-subsets, and compare their maximum fiber multiplicity with the original family.

Formal target: `planned Finset/Fintype double-counting signature`.

Output: N*C(p,k) <= M*C(n,k).

Source boundary: Erdos-Stone-1946:p1088:lemma-proof.

Budget: 64 substantive steps maximum; structured ledger: 1 recorded step.

### m0841-l-intersection-ratio

Derive M/N >= ((p-k+1)/n)^k from the binomial-coefficient ratio.

Formal target: `planned exact ordered-field corollary`.

Output: The source's Corollary 1.

Source boundary: Erdos-Stone-1946:p1088:Corollary-1.

Budget: 42 substantive steps maximum; structured ledger: 1 recorded step.

### m0841-l-intersection-log

Under p >= alpha*n and k <= alpha*log n, derive M/N >= n^(-3/4) with all positivity and rounding hypotheses.

Formal target: `planned exact real/natural logarithmic corollary`.

Output: The source's Corollary 2.

Source boundary: Erdos-Stone-1946:p1088:Corollary-2.

Budget: 68 substantive steps maximum; structured ledger: 1 recorded step.

### m0841-b-r-two

Prove DenseClaim 2 by the high-degree neighborhood argument.

Formal target: `Stage1Instances.THM_M_0841_Obligations.DenseBase`.

Output: The exact dense two-part base case.

Source boundary: Erdos-Stone-1946:p1088:r=2.

Budget: 24 substantive steps maximum; structured ledger: 1 recorded step.

### m0841-c-high-degree

Form the vertices of degree at least epsilon*n/2 and their neighborhood family.

Formal target: `planned Finset of high-degree vertices and neighborFinset map`.

Output: N indexed subsets of Fin n, each large enough for Corollary 2.

Source boundary: Erdos-Stone-1946:p1088:r=2.

Budget: 42 substantive steps maximum; structured ledger: 1 recorded step.

### m0841-l-high-degree-count

Use the total edge lower bound and low-degree bound to prove N > epsilon*n/2.

Formal target: `planned degree-sum inequality`.

Output: A linear lower bound on the number of high-degree vertices.

Source boundary: Erdos-Stone-1946:p1088:r=2.

Budget: 54 substantive steps maximum; structured ledger: 1 recorded step.

### m0841-l-base-common

Apply the logarithmic intersection corollary to the high-degree neighborhoods.

Formal target: `planned specialization of M0841-L-INTERSECTION-LOG`.

Output: Many high-degree vertices share at least floor(epsilon*log n/2) neighbors.

Source boundary: Erdos-Stone-1946:p1088:r=2.

Budget: 36 substantive steps maximum; structured ledger: 1 recorded step.

### m0841-l-base-size

Prove N/n^(3/4) > k and floor(epsilon*log n/2) >= k for k=ceil(sqrt(log n)).

Formal target: `planned exact eventual numerical package`.

Output: Enough distinct vertices on both sides of the bipartite copy.

Source boundary: Erdos-Stone-1946:p1088:r=2.

Budget: 62 substantive steps maximum; structured ledger: 1 recorded step.

### m0841-t-base-assemble

Choose distinct P and R vertices and package their cross adjacency as completeEquipartiteGraph 2 k containment.

Formal target: `planned exact DenseBase proof terminal`.

Output: Stage1Instances.THM_M_0841_Obligations.DenseBase.

Source boundary: Erdos-Stone-1946:p1088:r=2.

Budget: 44 substantive steps maximum; structured ledger: 1 recorded step.

### m0841-b-r-ge-three

Prove the strong-induction step DenseClaim r for every r >= 3.

Formal target: `Stage1Instances.THM_M_0841_Obligations.DenseStep`.

Output: The exact dense induction-step package.

Source boundary: Erdos-Stone-1946:pp1088-1090:r>=3.

Budget: 30 substantive steps maximum; structured ledger: 1 recorded step.

### m0841-c-admissible

Define admissible tolerances for the fixed r and set c to their greatest lower bound.

Formal target: `planned admissibility set and sInf package`.

Output: The critical tolerance c used by contradiction.

Source boundary: Erdos-Stone-1946:p1088.

Budget: 52 substantive steps maximum; structured ledger: 1 recorded step.

### m0841-l-admissible-bounds

Show admissibility is nonempty and 0 <= c <= 1/(2(r-1)); the endpoint is vacuous.

Formal target: `planned order-theoretic bounds on sInf`.

Output: A bounded critical tolerance with an explicit contradiction ceiling.

Source boundary: Erdos-Stone-1946:p1088.

Budget: 58 substantive steps maximum; structured ledger: 1 recorded step.

### m0841-b-c-zero

If c=0, use upward closure of admissibility to prove every positive tolerance.

Formal target: `planned zero-infimum branch`.

Output: DenseClaim r.

Source boundary: Erdos-Stone-1946:p1088.

Budget: 34 substantive steps maximum; structured ledger: 1 recorded step.

### m0841-b-c-positive

Assume c>0, choose 0<delta<c/(2r), and derive a contradiction.

Formal target: `planned positive-infimum branch`.

Output: False, eliminating c>0.

Source boundary: Erdos-Stone-1946:pp1088-1090.

Budget: 28 substantive steps maximum; structured ledger: 1 recorded step.

### m0841-c-counterexample

Use nonadmissibility of c-delta to choose arbitrarily large dense graphs without the required r-partite copy.

Formal target: `planned counterexample extraction above every threshold`.

Output: A large graph G at density c-delta with no K_r(k).

Source boundary: Erdos-Stone-1946:p1089.

Budget: 44 substantive steps maximum; structured ledger: 1 recorded step.

### m0841-c-ih-blocks

Apply the r-1 induction hypothesis at the printed auxiliary tolerance to find r-1 groups of 2q vertices.

Formal target: `planned DenseClaim (r-1) specialization`.

Output: r-1 mutually complete blocks and chosen q-subblocks.

Source boundary: Erdos-Stone-1946:p1089.

Budget: 58 substantive steps maximum; structured ledger: 1 recorded step.

### m0841-c-rich-vertices

Select remaining vertices adjacent to at least (r-2)q+kq/log q block vertices.

Formal target: `planned rich-vertex Finset`.

Output: A set of N possible vertices for the final part.

Source boundary: Erdos-Stone-1946:p1089.

Budget: 40 substantive steps maximum; structured ledger: 1 recorded step.

### m0841-l-rich-each-part

Show each rich vertex has at least kq/log q neighbors in every one of the r-1 blocks.

Formal target: `planned pigeonhole estimate over block degrees`.

Output: The per-block density premise for repeated Corollary 2.

Source boundary: Erdos-Stone-1946:p1089.

Budget: 38 substantive steps maximum; structured ledger: 1 recorded step.

### m0841-l-iterated-intersection

Apply the logarithmic intersection corollary successively through all r-1 blocks.

Formal target: `planned r-1-fold common-fiber construction`.

Output: At least N/(q^(3/4))^(r-1) vertices share k neighbors in every block.

Source boundary: Erdos-Stone-1946:p1089.

Budget: 74 substantive steps maximum; structured ledger: 1 recorded step.

### m0841-l-rich-card-bound

Use absence of the target copy and asymptotics to prove N < k*q^(3(r-1)/4) < n^(1/2) < n*k/log q.

Formal target: `planned exact rich-vertex cardinal chain`.

Output: The sharp N bound used in the deleted-edge estimate.

Source boundary: Erdos-Stone-1946:p1089.

Budget: 62 substantive steps maximum; structured ledger: 1 recorded step.

### m0841-c-delete-block

Delete q(r-1) selected block vertices and every incident edge.

Formal target: `planned induced remainder graph construction`.

Output: The next graph G_(t+1) with n-q(r-1) vertices.

Source boundary: Erdos-Stone-1946:p1089.

Budget: 36 substantive steps maximum; structured ledger: 1 recorded step.

### m0841-l-deleted-edge-bound

Bound the deleted edges by the exact three-term expression and then by n*q*(r-2)*(1+delta).

Formal target: `planned finite edge partition and arithmetic estimate`.

Output: A per-round loss bound.

Source boundary: Erdos-Stone-1946:p1089.

Budget: 84 substantive steps maximum; structured ledger: 1 recorded step.

### m0841-c-deletion-sequence

Iterate the block-deletion construction while its density and large-n hypotheses survive.

Formal target: `planned finite sequence of induced graphs`.

Output: Graphs G_t with fixed q and k and accumulated loss bounds.

Source boundary: Erdos-Stone-1946:pp1089-1090.

Budget: 70 substantive steps maximum; structured ledger: 1 recorded step.

### m0841-l-deletion-invariant

Prove every intermediate graph remains large enough and above the r-1 induction density with the same q and k.

Formal target: `planned sequence invariant`.

Output: Legality of every scheduled deletion round.

Source boundary: Erdos-Stone-1946:pp1089-1090.

Budget: 88 substantive steps maximum; structured ledger: 1 recorded step.

### m0841-c-step-count

Set s=floor(c*n/((r-1)q)) and d=(r-1)q*s/n.

Formal target: `planned natural step count and real ratio`.

Output: The number of rounds and removed-vertex fraction.

Source boundary: Erdos-Stone-1946:p1090.

Budget: 40 substantive steps maximum; structured ledger: 1 recorded step.

### m0841-l-s-rounds

Show at least s rounds run, removed vertices are at most cn<=n/4, and total lost edges obey the printed bound.

Formal target: `planned induction on the deletion sequence`.

Output: A final graph with at least 3n/4 vertices and controlled edge loss.

Source boundary: Erdos-Stone-1946:p1090.

Budget: 72 substantive steps maximum; structured ledger: 1 recorded step.

### m0841-l-d-limit

Establish 0<d<=c and d tends to c along the arbitrarily large counterexamples.

Formal target: `planned floor-error and limit argument`.

Output: Replacement of d by c in the final limiting inequality.

Source boundary: Erdos-Stone-1946:p1090.

Budget: 54 substantive steps maximum; structured ledger: 1 recorded step.

### m0841-l-tail-admissible

Apply admissibility of c+delta to the final graph, using the same-k part-size stability bridge.

Formal target: `planned final-remainder upper bound`.

Output: An upper edge bound at tolerance c+delta for G_s.

Source boundary: Erdos-Stone-1946:p1090.

Budget: 66 substantive steps maximum; structured ledger: 1 recorded step.

### m0841-l-global-edge-inequality

Combine the counterexample lower density, final admissible upper density, and total deleted-edge bound.

Formal target: `planned exact real inequality before limits`.

Output: The source's displayed inequality in n, c, delta, and d.

Source boundary: Erdos-Stone-1946:p1090.

Budget: 58 substantive steps maximum; structured ledger: 1 recorded step.

### m0841-l-limit-passage

First send n to infinity so d tends to c, then send delta to zero without reversing a strict boundary.

Formal target: `planned two-stage limiting argument`.

Output: The limiting algebraic inequality for c.

Source boundary: Erdos-Stone-1946:p1090.

Budget: 60 substantive steps maximum; structured ledger: 1 recorded step.

### m0841-l-algebra-contradiction

Simplify the limiting inequality to contradict c<=1/(2(r-1))<=1/4.

Formal target: `planned exact ordered-field arithmetic conclusion`.

Output: False under c>0.

Source boundary: Erdos-Stone-1946:p1090.

Budget: 38 substantive steps maximum; structured ledger: 1 recorded step.

### m0841-t-inductive-assemble

Combine the c=0 and c>0 branches and discharge the strong-induction step.

Formal target: `planned exact DenseStep proof terminal`.

Output: Stage1Instances.THM_M_0841_Obligations.DenseStep.

Source boundary: Erdos-Stone-1946:pp1088-1090.

Budget: 40 substantive steps maximum; structured ledger: 1 recorded step.

### m0841-t-dense-assemble

Use strong induction to combine DenseBase and DenseStep into the complete indexed dense family.

Formal target: `Stage1Instances.THM_M_0841_Obligations.denseFamily_compose`.

Output: Stage1Instances.THM_M_0841_Obligations.DenseFamily.

Source boundary: ObligationTree.lean:denseFamily_compose.

Budget: 18 substantive steps maximum; structured ledger: 1 recorded step.

### m0841-t-root-compose

Consume the assembled dense family and exact sparse-from-dense transport to produce the frozen root.

Formal target: `Stage1Instances.THM_M_0841_Obligations.sparse_compose`.

Output: Stage1Instances.THM_M_0841.ErdosStoneTarget.

Source boundary: ObligationTree.lean:sparse_compose.

Budget: 16 substantive steps maximum; structured ledger: 1 recorded step.

### m0841-x-source

Map every material proof node to pages 1087-1090, corrections, assumptions, and independent review.

Formal target: `planned primary-source node crosswalk`.

Output: Human-source evidence without machine proof credit.

Source boundary: source-statement-crosswalk.md; Erdos-Stone-1946:pp1087-1090.

Budget: 42 substantive steps maximum; structured ledger: 1 recorded step.

### m0841-x-provenance

Bind future proof bodies, wrappers, imports, revisions, source hashes, licenses, and terminal origins without duplicate credit.

Formal target: `planned content-addressed provenance packet`.

Output: Release provenance without mathematical proof credit.

Source boundary: anchor-audit.json:candidates.

Budget: 40 substantive steps maximum; structured ledger: 1 recorded step.

### m0841-x-trust

Close imported olean, executable, axiom, unsafe/oracle, computation, hermetic replay, and independent-verification boundaries.

Formal target: `planned transitive trust and TCB closure`.

Output: Release trust evidence without mathematical proof credit.

Source boundary: anchor-audit.json:immutable_environment.

Budget: 42 substantive steps maximum; structured ledger: 1 recorded step.

### m0841-x-readable

Produce a complete node-anchored reconstruction and independent combinatorics review.

Formal target: `planned readable reconstruction`.

Output: Readable coverage without machine proof credit.

Source boundary: future readable proof surface.

Budget: 48 substantive steps maximum; structured ledger: 1 recorded step.

### m0841-x-workflow

Bind proof, validation, release, freshness, revocation, and independent-verification tasks.

Formal target: `planned Stage1 workflow receipts`.

Output: Workflow acceptance without proof credit.

Source boundary: task-dag.json and future accepted receipts.

Budget: 28 substantive steps maximum; structured ledger: 1 recorded step.

## Freeze boundary

All accepted machine obligations remain open at `M3`; the assurance-only overlays are
not proof obligations. No exact root proof body was found. The conditional Lean harness
takes the dense base, strong-induction step, and sparse-from-dense bridge as explicit
premises, so it cannot be mistaken for Erdos-Stone proof closure. Primary-source H0, all
internal composition certificates, readable R0, transitive provenance and trust, hermetic
replay, independent verification, AUDIT-Z, and theorem completion remain open. Any scope or
eligibility change requires a successor registry and append-only delta.
