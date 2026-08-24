# Proof outline

Let `L` be the Laplacian of `G`, and for a vertex set `S` let `L[S]` be the
Laplacian of the spanning copy of the induced graph.  The target asks for a
universal positive constant `c` and, for every `0 < ε < 1`, a set with
`|S| ≥ c ε n` and `L[S] ⪯ ε L`.

1. Expand the frozen predicate `IsEpsilonLight` into the positive-semidefinite
   inequality `PosSemidef (ε • L - L[S])`.  This is the semantic root; the
   provider's proof body is never used.
2. Apply the finite spectral-selection argument to the edge rank-one
   decomposition of `L`.  It selects a vertex set of linear size while keeping
   the induced edge sum below the prescribed scalar multiple of the original
   Laplacian.  Zero-size vertex types and edgeless components are retained as
   explicit boundary cases.
3. Translate the matrix inequality back to `IsEpsilonLight`, preserve the card
   coercion to `ℝ`, and assemble the existential witness `c` before the
   quantifiers over `n`, `G`, and `ε`.
4. Transport the expanded claim-owned proposition to and from the frozen source
   statement.  Audit both composites and require Master recomputation of the
   elaborated expressions rather than accepting textual identity.

Every proof node has one unique prose fragment in `full-study.md`; the reverse
map and deletion-mutation decisions are sealed in `readability-review.json`.
