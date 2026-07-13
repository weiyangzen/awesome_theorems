# Scope map

## Preserved theorem family

The catalog phrase `谱隙与扩展性` is preserved as the Alon-Milman 1985 result family relating a
finite graph's Laplacian spectral gap to isoperimetric, metric-neighborhood, or expander behavior.
The matching paper is:

N. Alon and V. D. Milman, *lambda_1, Isoperimetric Inequalities for Graphs, and
Superconcentrators*, *Journal of Combinatorial Theory, Series B* 38(1) (1985), 73-88,
DOI `10.1016/0095-8956(85)90092-9`.

This family identification is not a canonical statement. The paper has several proposition-changing
candidates rather than one theorem literally named "Alon-Milman theorem."

## Candidate roots not credited

1. Lemma 2.1, pp. 77-78: for disjoint vertex subsets `A,B`, their distance `rho`, normalized sizes
   `a,b`, and internal-edge sets `E_A,E_B`, the paper bounds the second Laplacian eigenvalue using
   the edges outside `E_A union E_B`.
2. Theorem 2.5, pp. 78-79: if `rho > 1`, maximal degree `d` and the same notation are fixed, then
   `b <= (1-a) / (1 + (lambda_1/d) * a * rho^2)`.
3. Theorem 2.6, p. 79: an iterated exponential separation/concentration bound depending on
   `lambda_1`, `d`, `a`, and a real threshold `p>=1` strictly below the set distance.
4. Theorem 2.7, pp. 79-80: a diameter upper bound in terms of maximum degree, `lambda_1`, and
   `log_2 |V|`.
5. Theorem 4.3, pp. 83-84: the extended double cover of an `(n,k,epsilon)` enlarger is an
   `(n,k+1,c)` expander for `c = 4*epsilon/(k+4*epsilon)`.
6. The modern `d`-regular edge-expansion formulation: for second adjacency eigenvalue `lambda` and
   edge-expansion ratio `h(G)`, `(d-lambda)/2 <= h(G) <= sqrt(2*d*(d-lambda))`. Later surveys
   attribute this discrete result independently to Alon-Milman and others, but the notation,
   packaging, and proof boundary are not the catalog's selected source statement.

## Proposition-changing decisions

Before the statement phase can freeze a claim, an accepted source and reviewer must decide:

1. Which numbered primary result, or which checked reformulation of it, the catalog denotes.
2. Whether the graph is finite, connected, simple, undirected, regular, or allowed to be a Cayley
   multigraph, and whether empty or singleton carriers are permitted.
3. Whether the spectrum is that of `Q = C^T C`, the adjacency matrix, the combinatorial Laplacian,
   or the normalized Laplacian; the eigenvalue ordering and multiplicity convention; and whether
   `lambda_1` in the paper becomes `lambda_2` in modern zero-based spectral notation.
4. Whether expansion means edges leaving a set, external vertex neighborhood, conductance,
   distance-neighborhood concentration, an enlarger, or the bipartite extended-double-cover
   expander predicate.
5. Every normalization: division by `|S|`, `min(|S|,|V-S|)`, volume, or `|V|`; ordered versus
   unordered boundary edges; natural-to-real coercions; strict versus non-strict inequalities.
6. The ordered binders for graph, vertex subsets, distance, degree, eigenvalue, and constants, plus
   which quantities are definitions and which are hypotheses.
7. Whether the root is one implication from gap to expansion or a two-sided equivalence, and which
   proof sources are admitted for each direction.
8. How source corrections, typographical ambiguities, and later repackagings are reconciled.

## Boundary and degenerate cases

No case is excluded before the proposition is selected. Source review must decide disconnected
graphs and the multiplicity of zero; empty, singleton, edgeless, and complete graphs; maximum
degree zero; `A` or `B` empty; full or half-sized tested sets; zero distance, Theorem 2.5's
`rho > 1`, and Theorem 2.6's `dist(A,B)>p>=1`; `a=0`, `b=0`, or vanishing denominators; loops and parallel edges; equality at
the expansion bound; and whether an expander family must have unbounded order.

These are not cosmetic. For example, the paper's Theorem 2.5 is a metric-separation inequality for
arbitrary connected graphs, while the familiar two-sided statement uses edge expansion of a
finite connected regular graph.

## Explicit exclusions

- `THM-M-0888` Cheeger inequality is a distinct catalog root. Its manifold or graph formulation
  cannot be substituted for this Alon-Milman source boundary.
- `THM-M-0881` expander graphs is a general existence/construction topic, and `THM-M-0887` spectral
  graph theory is a broad subject. Neither transfers a statement or proof here.
- Theorem 4.3 cannot be replaced by merely assuming the desired expansion in an enlarger or model
  field, and one finite example cannot replace a uniform family claim.
- The unrelated convex-geometry result also called the Alon-Milman theorem is excluded by this
  target's graph-theory category, 1985 date, attribution, and spectral-gap/expansion gloss.
- Adjacency, combinatorial-Laplacian, and normalized-Laplacian gaps are not interchangeable without
  checked hypotheses and transports.
- Numerical eigenvalues, graph sampling, a source title match, and the untrusted `verified` label
  provide no proof credit.

## Lean boundary and retry condition

Pinned mathlib provides adjacent finite `SimpleGraph`, degree, distance, adjacency matrix,
Laplacian matrix, positive-semidefinite, and Hermitian-spectrum APIs. The intake probe authenticates
only those interfaces. A bounded exact-topic search found no Alon-Milman or graph-expansion
terminal theorem in repo-local Lean or pinned mathlib. Exhaustive discovery belongs to the later
anchor-audit phase.

Retry the statement gate after an independent reviewer selects and admits an immutable primary
root or explicitly approved modern reformulation, maps all incorporated definitions and premises,
records corrections and proof boundaries, and fixes the choices above. Then encode that exact
proposition with minimal pinned imports, preserve its elaborated expression and environment, check
every alternate transport, and run the required mutations.
