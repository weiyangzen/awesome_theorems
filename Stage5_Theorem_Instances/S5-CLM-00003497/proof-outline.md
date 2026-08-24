# Proof outline

Let `K(n)` be the cyclic decomposition assertion and `R(n)` the Ringel
decomposition assertion for the same natural number `n`. The frozen source
states both assertions eventually in the at-top filter.

For each `n`, `K(n) → R(n)`: specialize `K(n)` to a finite vertex type, a tree,
and its edge-count equality. The cyclic assertion returns embeddings `f i`
together with three conjuncts. Erase only the first conjunct, which says every
copy is a translate of copy zero. The other two conjuncts are definitionally
the pairwise-disjointness and complete-cover outputs required by `R(n)`.

Monotonicity of `Filter.Eventually` lifts this pointwise implication to
`(∀ᶠ n, K(n)) → (∀ᶠ n, R(n))`. This is exactly the term in `Proof.lean`.

The statement transport in `Statement.lean` is bidirectional because the
frozen source and claim-owned Ringel propositions have the same binders,
hypotheses, witness type, disjointness clause, and supremum clause.
