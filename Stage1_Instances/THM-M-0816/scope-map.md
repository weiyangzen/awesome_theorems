# Scope map

## Preserved theorem family

The repository fixes the eponym, Pál Turán, the year 1941, and the subject "maximum number of edges
in a graph containing no complete subgraph." The intended statement must remain within the finite
simple-graph extremal family now called Turán's theorem. Intake does not silently choose among
these materially different roots:

1. **Sharp edge inequality.** An `n`-vertex graph with no clique of size `r + 1` has at most as
   many edges as the complete `r`-partite graph whose part sizes differ by at most one.
2. **Exact arithmetic formula.** The maximum is expressed using `n / r` and `n % r`, or an
   algebraically equivalent floor/ceiling or binomial formula.
3. **Equality or uniqueness form.** An extremal `(r + 1)`-clique-free graph is isomorphic to the
   balanced complete `r`-partite Turán graph.
4. **Extremal-number form.** The extremal number for forbidding a complete graph equals the edge
   count of the appropriate Turán graph.

The gloss omits the clique parameter entirely. It could even be read as forbidding every complete
subgraph, which is not the standard theorem because every nonempty graph contains trivial complete
subgraphs. Source review must recover the intended parameterized proposition rather than repair the
gloss by assumption.

## Candidate scope in pinned mathlib

The dedicated pinned module works with a finite vertex type `V`, a `SimpleGraph V`, decidable
adjacency, and a natural parameter `r`. It defines `G.IsTuranMaximal r` by extremality among graphs
that are `CliqueFree (r + 1)`, and defines `turanGraph n r` on `Fin n` by adjacency of vertices in
different residue classes modulo `r`.

Its strongest directly relevant candidate surfaces are:

- `SimpleGraph.isTuranMaximal_iff_nonempty_iso_turanGraph`, for `0 < r`, characterizing an
  `r`-Turán-maximal graph up to isomorphism;
- `SimpleGraph.CliqueFree.card_edgeFinset_le`, the exact edge upper bound for an
  `(r + 1)`-clique-free graph;
- `SimpleGraph.card_edgeFinset_turanGraph`, the exact natural-number edge formula;
- `SimpleGraph.extremalNumber_top` and
  `SimpleGraph.card_edgeFinset_eq_extremalNumber_top_iff_nonempty_iso_turanGraph`, a forbidden
  complete-graph encoding.

These declarations are candidates, not canonical targets. The statement phase must select the
source variant, freeze all binders and side conditions, serialize one elaborated expression, and
compile checked transports before any candidate can receive proof credit.

## Boundaries to resolve

- finite simple undirected graphs versus another graph model;
- a graph on exactly `n` vertices versus an arbitrary finite vertex type with `card V = n`;
- the convention that forbidding `K_(r+1)` corresponds to an `r`-partite extremal graph;
- inequality only versus exact value, equality case, or uniqueness up to isomorphism;
- an explicit quotient/remainder formula versus the abstract edge count of `turanGraph n r`;
- whether `0 < r` is assumed and how `r = 0` is interpreted;
- the regimes `n = 0`, `n < r`, `n = r`, empty graphs, and complete graphs;
- whether adjacency, graph equality, and graph isomorphism need explicit decidability instances;
- exact natural-number subtraction and division semantics in arithmetic presentations;
- which historical source proposition and notation the repository intends.

## Explicit non-substitutions

- Mantel's triangle-free theorem alone, unless selected as a specialization and connected to the
  source-approved general theorem by checked implications;
- Erdős-Stone, Erdős-Simonovits stability, supersaturation, Ramsey, or hypergraph Turán theorems;
- spectral, weighted, directed, infinite, multipartite-host, or forbidden-family variants;
- only the fact that `turanGraph` is clique-free, without the extremal bound;
- only an edge inequality when the selected source root requires the equality characterization,
  or conversely;
- a convenient fixed value of `r`, weakened bound, stronger hypothesis, assumed extremal witness,
  or preconstructed partition not selected by source;
- the untrusted catalog label `已验证`, module documentation, or a successful `#check` treated as
  source closure, kernel closure, or theorem completion.

No canonical expression, statement fingerprint, checked alternate encoding, obligation registry,
discovery protocol, proof state, or completion claim is frozen at intake.

