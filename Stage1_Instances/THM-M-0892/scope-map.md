# Scope map

## Preserved theorem family

The intake preserves the finite undirected simple-graph family named by the catalog. Candidate
components below are a resolution ledger, not statements credited to this target:

- a finite regular simple graph of degree `k` and diameter `2` attaining the Moore bound
  `1 + k + k * (k - 1) = k^2 + 1` vertices;
- the equivalent girth-5 formulation under the required nontriviality and connectedness clauses;
- the explicit degree-7, 50-vertex graph now called the Hoffman-Singleton graph;
- its characterization as a strongly regular graph with parameters `(50, 7, 0, 1)`;
- uniqueness of that graph up to graph isomorphism;
- the necessary degree restriction `k = 2`, `k = 3`, `k = 7`, or `k = 57`; and
- the separate open question whether a degree-57 diameter-2 Moore graph exists.

## Decisions required at statement freeze

1. Preserve a lawful immutable primary or authoritative edition, select an exact result and page
   or theorem locator, map incorporated definitions and proof boundaries, check corrections or
   errata, and obtain independent source approval.
2. Decide whether the root is existence of the degree-7 graph, uniqueness at degree `7`, the
   possible-degree classification, the diameter-3 result also named by the paper, or a precisely
   source-delimited conjunction.
3. Fix whether a Moore graph is defined through diameter and vertex count, degree and girth, the
   strongly regular parameter package, or another source definition, and prove every credited
   equivalence in the required direction.
4. Fix the vertex type and finiteness representation, decidable adjacency, exact regularity
   predicate, connectedness, nontriviality, diameter convention, girth convention, and cardinality
   equation.
5. Fix ordered binders and the quantifier over the degree. In particular, an existential graph at
   degree `7` and a universal classification over all degrees are different propositions.
6. Decide whether uniqueness is equality after transport, `SimpleGraph.Iso`, or another graph
   isomorphism notion, and whether an explicit construction must be exposed.
7. Freeze the foundation, computation, and certificate policy for any finite construction or
   adjacency-matrix verification.

## Degenerate and boundary cases

Source review must dispose explicitly of empty and singleton vertex types, degree `0` and `1`,
disconnected graphs, the junk value `0` used by mathlib's natural-valued diameter for disconnected
graphs and girth for acyclic graphs, complete graphs of diameter `1`, cycles at degree `2`, and the
distinction between diameter at most `2` and exactly `2`. It must also decide whether loops or
multiple edges are excluded by the model, whether local finiteness is data or derived from global
finiteness, and how graph isomorphism transports cardinality and metric properties.

In particular, the attractive strongly regular encoding `IsSRGWith (k^2 + 1) k 0 1` admits
small complete examples at `k = 0` and `k = 1` unless a lower bound such as `2 <= k` is included.
That lower bound must come from the selected source or be covered by an explicit checked transport;
it cannot be smuggled into an encoding after the fact.

The degree-57 case is especially important: presenting its existence as a theorem would turn an
open problem into a false completion claim. It can occur only as the unresolved alternative in a
source-approved classification statement unless a later accepted source proves more.

## Substitution exclusions

- The Petersen graph, 5-cycle, complete graphs, and individual diameter-3 examples are not the
  degree-7 Hoffman-Singleton result.
- A structure or hypothesis that stores the desired graph, adjacency table, strongly regular
  certificate, or isomorphism as data is not a proof of existence or uniqueness.
- A proof that some 50-vertex graph is 7-regular without diameter, girth, or Moore-bound closure is
  weaker than the relevant existence claim.
- A proof that all diameter-2 Moore graphs have one of four possible degrees does not construct the
  degree-7 graph and does not settle the degree-57 case.
- A numerical graph search, unchecked adjacency matrix, Sage computation, or external database
  entry supplies no theorem credit without a kernel-checked certificate covering the exact target.
- Generic simple-graph, regularity, diameter, girth, or strongly regular APIs are representation
  substrate, not the Hoffman-Singleton theorem.
- The catalog's `verified` label and this intake probe carry no human-source or machine-proof
  credit.

No canonical Lean target, expression fingerprint, checked alternate encoding, mutation suite,
discovery protocol, obligation registry, or proof body is frozen at intake.
