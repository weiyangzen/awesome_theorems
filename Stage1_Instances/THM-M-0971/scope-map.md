# THM-M-0971 scope map

## Preserved theorem family

The intake preserves the catalog's contextual identification of the Shearer bound as an optimal
condition for avoiding all bad events in the Lovasz Local Lemma setting. Its placement beside the
Lovasz Local Lemma and Moser-Tardos targets distinguishes it from unrelated results also called a
Shearer bound, such as entropy-cover inequalities and triangle-free-graph independence bounds.

This family description is not a canonical proposition. The matching 1985 primary-source lead
contains a sharp symmetric degree threshold and a more general sharp probability bound. Modern
accounts formulate independent-set-polynomial positivity criteria, sometimes in lopsided form, and
separate sufficiency from optimality/tightness. The repository does not choose among them.

## Decisions required at statement freeze

An exact, independently reviewed source statement must fix all of the following:

1. Whether the root is the original general lower bound, an independent-set-polynomial
   nonnegativity criterion, the symmetric maximum-degree threshold, a positivity corollary, or an
   optimality converse.
2. A finite vertex type or `[n]`, the simple dependency graph, and whether adjacency is open or
   closed-neighborhood dependence.
3. The probability space, event family, measurability premises, and probability codomain.
4. The exact independence hypothesis: independence of one event from the sigma-algebra generated
   by all nonneighbors, equality for intersections of nonneighbor events, a conditional lopsided
   inequality, or another source-defined condition.
5. The coordinate bounds `P(E_i) <= p_i`, their domain, and whether zero and one are allowed.
6. The exact independent-set polynomial, subset indexing, sign convention, empty product, and
   whether all induced-subset evaluations, all coefficients, or another family must be nonnegative
   or positive.
7. The conclusion: a numerical lower bound for avoiding a specified subset, strict positivity of
   avoiding every event, existence of an event system witnessing failure, or a sharp threshold.
8. Ordered binders, coercions, strict/nonstrict inequalities, alternate encodings, foundation and
   computation profiles, proof boundary, correction history, and every degenerate case.

## Boundary cases

Source review must address an empty vertex type; one vertex; edgeless and complete graphs; isolated
vertices; empty/full events; probabilities zero and one; empty and singleton index subsets; empty
products and sums; zero independent-set-polynomial values; maximum degrees zero and one; the
`d >= 2` branch of the symmetric formula; and whether equality lies inside the guaranteed region.

## Excluded substitutions

- The ordinary symmetric or asymmetric Lovasz Local Lemma is a sufficient criterion, not by itself
  the exact Shearer optimum.
- The Moser-Tardos resampling algorithm is constructive/algorithmic and is separately cataloged.
- A modern lopsided or variable-model generalization cannot replace Shearer's original formulation
  without a checked, source-approved relationship.
- The symmetric value `f(d)` alone cannot replace a requested general graph/probability bound, nor
  can the general criterion silently broaden a symmetric target.
- Graph independent-set APIs do not define the weighted signed polynomial or prove its probabilistic
  conclusion.
- Pairwise or mutual event independence cannot replace dependency-graph independence.
- A structure storing the desired avoidance bound or positivity conclusion supplies no proof.
- The untrusted catalog status, a theorem name, a bounded search, or `#check` output supplies no H,
  M, or R closure.

## Neighbor boundaries

`THM-M-0969` owns the Lovasz Local Lemma family, while `THM-M-0970` owns the Moser-Tardos
algorithm. They may later become explicit dependencies after exact statement and obligation
freezes, but neither transfers statement or proof credit. `THM-M-0972` owns Janson's inequality, a
different rare-event bound. No artifact or status is shared across these targets.

## Formal boundary

No canonical Lean expression is frozen. At pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, the discovery probe checks event-independence and
finite-intersection APIs plus simple-graph independent-set, neighbor, and maximum-degree APIs. The
bounded source-name/topic search found no exact target declaration. This is not an exhaustive anchor
audit or an external absence claim. The statement phase remains blocked until one exact source root
and all proposition-changing choices above are independently approved.
