# Scope map

## Received scope

The repository fixes only the title `扩展图`, the collective attribution `众多数学家`, the period
`20世纪`, and the gloss `扩展图的存在性与构造`. It gives no bibliography, definition, ordered
binders, hypotheses, conclusion, constants, boundary cases, proof, or formal artifact. Stage0
repeats this wording and explicitly leaves the formal system, exact definitions and premises, proof
route, dependencies, equivalent forms, axioms, machine state, and artifact links open. The
`已验证` label is untrusted metadata.

The source cluster supports translating the title as "expander graphs": immediately following
catalog records separately name the Margulis construction, the Lubotzky-Phillips-Sarnak
construction, Ramanujan graphs, Morgenstern's theorem, and the Marcus-Spielman-Srivastava theorem.
That context identifies a subject only. It does not select a proposition or transfer evidence from
those other roots.

## Candidate mathematical families

An eventual source-approved target could concern one of the following, but none is asserted or
credited at intake:

- existence of finite vertex expanders with specified degree and vertex-expansion constant;
- existence of finite edge expanders or graphs with a specified isoperimetric/Cheeger constant;
- existence of regular spectral expanders with a stated adjacency or Laplacian eigenvalue bound;
- an infinite family of bounded-degree graphs with uniform positive expansion and unbounded order;
- probabilistic existence for selected sizes or an explicit, uniform, algorithmic construction;
- a theorem transporting one exact expansion notion to another under explicit hypotheses.

These statements have different domains, constants, quantifier orders, degenerate cases, and proof
obligations. A familiar textbook formulation cannot choose among them.

## Proposition-changing decisions

Before the statement phase can freeze a canonical claim, an accepted source and reviewer must fix:

1. The graph model: simple or multi, undirected or directed, bipartite or general, finite at every
   index, and whether loops or parallel edges are allowed.
2. The expansion notion: external vertex boundary, closed neighborhood growth, edge boundary,
   conductance, an adjacency eigenvalue gap, a normalized-Laplacian gap, or another invariant.
3. The coefficient type and normalization for every cardinality, ratio, and spectral inequality.
4. Regularity or maximum-degree conditions and the exact degree parameter, including whether it is
   fixed independently of graph order.
5. The expansion constant, whether it is fixed uniformly, and all strict versus non-strict bounds.
6. Which subsets are tested: nonempty only, proper only, size at most half the vertex set, volume at
   most half, or another cutoff; and whether boundary vertices inside the set are excluded.
7. The family encoding and index: every natural order, infinitely many orders, a subsequence, or an
   arbitrary unbounded sequence; equality versus lower bounds on graph size.
8. The exact quantifier order over degree, expansion constant, index, graph, and tested subsets.
9. Whether "construction" means nonconstructive existence, randomized sampling with probability
   bounds, an explicit algebraic family, a polynomial-time algorithm, or a computable generator.
10. Connectedness, regularity, labeling, uniformity, effective constants, and every source correction
    or erratum.

## Boundary and degenerate cases

No case is excluded before a proposition is selected. Source review must decide empty and singleton
vertex types; graphs of order below the degree; degree zero, one, or two; an empty tested subset; the
whole vertex set; half-size rounding for odd order; zero or negative real expansion constants;
disconnected graphs; repeated/isomorphic members of a family; bounded rather than unbounded family
orders; and whether isolated vertices or trivial complete graphs satisfy a vacuous formulation.

These cases matter: without uniform bounded degree, positive expansion, and an unbounded-size
condition, a convenient single finite graph can turn the meaningful family claim into a much weaker
existence statement.

## Explicit exclusions

The intake must not replace this item with Margulis construction (`THM-M-0882`),
Lubotzky-Phillips-Sarnak construction (`THM-M-0883`), Ramanujan graphs (`THM-M-0884`), Morgenstern's
theorem (`THM-M-0885`), or the Marcus-Spielman-Srivastava theorem (`THM-M-0886`). Those are separate
catalog roots even if a reviewed proof later supplies a typed relationship.

Also excluded are a single complete graph or other finite example substituted for an unbounded
family; assuming expansion or the desired construction as a structure field; switching among
vertex, edge, and spectral definitions without checked implications; generic `SimpleGraph`, matrix,
connectivity, or regularity APIs used as an exact theorem anchor; empirical random-graph tests; and
the untrusted catalog label used as source or kernel evidence.

## Lean boundary

Pinned mathlib provides `SimpleGraph` plus finite/local-finite interfaces, `neighborSet`,
`neighborFinset`, vertex degree, regularity, adjacency matrices, and Laplacian matrices. The bounded
intake query found no obvious
graph-expander declaration. `IntakeProbe.lean` authenticates only the adjacent substrate. It defines
no expansion predicate, declares no target theorem, and supplies no proof-body credit. An exhaustive
formal-candidate and provenance audit belongs to the later anchor-audit phase.

## Retry condition

Select a lawful immutable primary or authoritative source and pinpoint proposition; record its
edition, theorem/section/page, incorporated definitions, complete binders, hypotheses, conclusion,
proof boundary, corrections, and boundary conventions; reconcile the neighboring construction and
Ramanujan roots; and obtain independent source review. A later statement phase may then encode
exactly that proposition, minimize pinned imports, serialize its expression and environment, check
all transports, and run the required mutations.
