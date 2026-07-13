# Scope map

## Preserved catalog scope

The repository fixes target `THM-M-0905`, the title `Galvin定理`, attribution to Fred Galvin, year
1995, and the gloss `Dinitz猜想的证明`. Importance "high" and source status `已验证` are untrusted
metadata. A proof attribution or proof-method label is not itself a truth-valued theorem statement.

The exact 1995 bibliographic lead is Galvin's *The List Chromatic Index of a Bipartite Multigraph*.
That title and later summaries identify a standard list-edge-coloring result family. They do not,
without primary-text inspection and source admission, settle which formulation this catalog target
owns or its exact binders and conventions.

## Candidate graph scope, not credited

A familiar candidate formulation is: if a bipartite multigraph admits a proper edge coloring with
`k` colors, then for every assignment of at least `k` allowed colors to each edge there is a proper
edge coloring choosing an allowed color at every edge. Equivalent-looking slogans compare the list
chromatic index with the chromatic index. This paragraph is a resolution candidate only. It is not
the canonical statement, an elaborated Lean expression, or proof evidence.

## Proposition-changing decisions

The statement phase must freeze all of the following from an admitted immutable source:

1. Whether the root is Galvin's stronger bipartite-multigraph theorem, the `K_(n,n)` Dinitz
   corollary, a list-chromatic-index equality, or a source-defined conjunction.
2. The multigraph representation and identity of parallel edges, the definition of incidence, and
   whether loops are excluded by definition or hypothesis.
3. Whether vertices, edges, and the whole multigraph are finite, locally finite, or subject to
   another source condition; isolated vertices and unused represented vertices must be handled.
4. Whether `k` ranges over all naturals or positive naturals, and whether `k`-edge-colorable means
   a supplied proper coloring witness, existence of such a witness, or chromatic index at most `k`.
5. Whether an allowed-color "list" is a finite set, multiset, or sequence; how duplicates count;
   and whether each collection has cardinality exactly `k` or at least `k`.
6. The color carrier, decidable equality and finiteness assumptions, whether one finite global
   palette is required, and whether list colors must coincide with colors used by a witness.
7. The exact proper-edge-coloring predicate, including how distinct parallel edges and all pairs of
   incident edges are compared.
8. The exact conclusion: existence of one list-respecting coloring, an inequality between
   invariants, or equality after a separately proved reverse inequality.
9. Every ordered binder, universe, typeclass hypothesis, logical principle, representation
   transport, and boundary case.
10. The source theorem/proof locator, incorporated definitions, correction and errata status, and
    an independent source-to-catalog fidelity review.

## Boundary and degenerate cases

No case is excluded at intake. Source review must decide `k = 0`; empty edge and vertex types;
edgeless graphs with isolated vertices; nonempty graphs with no possible zero-color coloring;
single edges; repeated parallel edges; disconnected graphs; empty or undersized lists; duplicate-
bearing lists; infinite color carriers with finite per-edge lists; and exact-size list thinning.
The statement must make any vacuity in the empty or edgeless cases explicit rather than inheriting
it accidentally from an encoding.

## Neighbor and substitution exclusions

- `THM-M-0904` owns the Dinitz conjecture family. A checked `K_(n,n)`/array corollary may later be a
  transport, but neither target automatically shares a root, receipt, or proof status.
- `THM-M-0906` owns general list-coloring theory. Definitions there may become dependencies, but a
  definition or general survey topic does not establish Galvin's theorem.
- Ordinary vertex colorability, bipartiteness, an edge labeling, or construction of a line graph is
  not list edge-choosability.
- A simple-graph theorem that collapses parallel edges cannot replace the multigraph family without
  an admitted source restriction and checked transport.
- A statement assuming the desired list-respecting coloring, matching decomposition, orientation,
  kernel-perfectness conclusion, or theorem as a structure field supplies no proof.
- A Latin square with one common palette is only a special assignment, not the arbitrary-list
  theorem.
- The catalog's `已验证` label, bibliographic metadata, an API probe, theorem name, or bounded search
  provides no H or M proof credit.

## Downstream boundary

No canonical Lean expression is frozen at intake. The statement phase must first admit and
independently review an immutable source, select one exact proposition, and reconcile the boundary
with `THM-M-0904`. Only then may it fix minimal imports, expression and environment fingerprints,
checked transports, and statement mutations. Anchor audit, obligation architecture, proof,
validation, and release remain separate open tasks.
