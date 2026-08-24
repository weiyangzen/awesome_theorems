# Machine-checked audit

The claim-owned term in `Proof.lean` performs one inference under
`Filter.Eventually.mono`. At a fixed sufficiently large `n`, it specializes the
cyclic theorem to `V`, `T`, the tree proof, and the edge-count equality. It then
destructures the witness into:

1. an embedding family `f`;
2. the cyclic-shift equality;
3. pairwise edge-set disjointness; and
4. the supremum equality with the complete graph.

The result reuses `f`, item 3, and item 4. Item 2 is intentionally discarded;
no hypothesis used by Ringel and no requested output is discarded. The term
does not invoke the frozen provider declaration or its proof body and therefore
does not transport `sorryAx` into the claim-owned reduction.

The worker is forbidden to run Lean, Lake, or Elan. Consequently the local
receipt is a semantic/evidence preflight, while trust-zero elaboration, exact
expression recomputation, axiom census, and a clean offline rebuild remain
mandatory Master operations after harvest.
