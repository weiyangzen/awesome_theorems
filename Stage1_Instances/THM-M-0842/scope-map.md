# Scope map

## Preserved catalog scope

- Target: `THM-M-0842`, `Simonovits稳定性`, in combinatorics / graph theory.
- Literal gloss: stability of extremal graphs.
- Attribution and year: Miklós Simonovits, 1968.
- Lifecycle: `planned` from the uniform `L0 / rework_required` baseline.
- The source label `已验证` is inventory metadata, not human-source or kernel evidence.

The 1968 attribution and title strongly identify Simonovits's extremal-graph stability family. They
do not select one binder-complete theorem from that family.

## Candidate roots not credited

1. **Original general stability definition/framework.** Simonovits defines stability for a graph
   property and develops results for finite forbidden families and associated extremal graphs.
2. **Original Theorem 7.** Under the preceding theorem's finite-family and extremal-graph
   hypotheses, a sufficiently dense forbidden-family-free graph can be made `d`-chromatic by
   deleting fewer than `epsilon * n^2` edges.
3. **Original Theorem 8(a).** For fixed `r >= 2`, `d >= 2`, and `epsilon > 0`, sufficiently large
   graphs excluding the balanced complete `(d + 1)`-partite graph with `r` vertices per part and
   lying within `delta * n^2` edges of the `d`-partite Turán count can be made `d`-chromatic after
   deleting at most the integer part of `epsilon * n^2` edges.
4. **Modern arbitrary-`F` edit-distance form.** For a fixed graph `F` with chromatic number
   `d + 1`, every sufficiently large `F`-free graph whose edge count is within a quadratic error
   of the Turán density is within `epsilon * n^2` edge edits of a balanced Turán graph.
5. **Clique-only deletion form.** A sufficiently dense `K_(d+1)`-free graph can be made
   `d`-partite by deleting few edges; later results give stronger quantitative relationships.

These roots differ in their forbidden object, asymptotic threshold, comparison graph, use of an
extremal family, and whether the conclusion permits deletion only or two-sided edits. Intake does
not choose or conflate them.

## Proposition-changing decisions

The statement phase must freeze all of the following from one immutable source passage:

- whether the root is Simonovits's original Theorem 7, Theorem 8(a), or a named modern equivalent;
- a single forbidden graph or a finite/infinite forbidden family, and its finiteness and nonempty-
  edge assumptions;
- the chromatic parameter and its offset convention (`d`, `r`, or `chi(F) - 1`);
- finite simple labeled graphs on `Fin n` versus arbitrary finite vertex types up to isomorphism;
- the exact lower edge bound: `e(T_(n,d)) - delta*n^2`, an extremal number, or a density formula;
- strict versus weak inequalities, integer casts, floors, and the ordered dependence of
  `delta` and `n0` on the fixed graph data and `epsilon`;
- deletion to a `d`-colorable / `d`-partite subgraph versus symmetric edit distance to a balanced
  Turán graph, including whether vertex relabeling is minimized over;
- the normalization of edit distance and whether the budget counts unordered edges once;
- incorporated definitions, source theorem dependencies, corrections or errata, and proof scope;
- every universe, typeclass, ordered binder, hypothesis, conclusion, alternate encoding, and
  checked transport direction.

## Boundary and degenerate cases

No case is excluded at intake. Source selection must resolve `d = 0` or `1`, empty forbidden
families, forbidden graphs with no edges, `n = 0` or smaller than the forbidden graph, `epsilon = 0`
or large tolerance, `delta = 0`, empty and complete input graphs, zero-part Turán graphs, the exact
threshold `n = n0`, equality at the edge bound, and rounding when a real quadratic budget is
compared with a natural edge count.

## Neighbor and substitution exclusions

- `THM-M-0841` separately owns the Erdős-Stone theorem. Its asymptotic extremal-number conclusion
  is an ingredient or neighboring result, not structural stability.
- `THM-M-0816` separately owns Turán's exact theorem. Exact maximality of `turanGraph` does not
  imply that every almost maximal graph is structurally close to it.
- `THM-M-0843` separately owns Szemerédi's regularity lemma. A regular partition or a later short
  proof using regularity cannot replace the requested conclusion.
- Spectral, signless-Laplacian, hypergraph, multipartite-host, random-graph, saturated-graph,
  graphon, and clique-count stability variants are out of scope unless an accepted target
  correction selects one.
- An assumed stability predicate, a witness supplied as input, a graph experiment, or a numerical
  test is not a proof. The catalog's verified label supplies no proof credit.

## Lean and trust boundary

Pinned mathlib contains exact Turán-theorem and graph-edit substrate, but no located target-level
stability theorem. The probe authenticates interface availability only. Exact imports, a canonical
expression and environment fingerprint, checked transports, statement mutations, a complete
formal-candidate audit, foundation and axiom policy, obligation registry, typed graphs, proof-body
provenance, readable reconstruction, hermetic replay, and independent verification remain open.
