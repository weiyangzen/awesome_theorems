# Proof outline

1. Fix a field `k`. Unfold the exact frozen predicate
   `Arxiv.«2208.14736».IsCancellative k k[X]`.
2. Fix a commutative finite-type `k`-algebra `B` and an input equivalence
   `k[X][X] ≃ₐ[k] B[X]`.
3. Apply the one-dimensional polynomial cancellation closure at this exact
   elaborated root; no characteristic assumption is introduced.
4. Return `Nonempty (k[X] ≃ₐ[k] B)`.
5. Transport the result in both directions across the identity crosswalk.

The structured DAG and reverse readability ledger carry the hypotheses,
inference, output, downstream use, exceptional-case statement, and trust
boundary; this outline intentionally does not duplicate those inventories.
