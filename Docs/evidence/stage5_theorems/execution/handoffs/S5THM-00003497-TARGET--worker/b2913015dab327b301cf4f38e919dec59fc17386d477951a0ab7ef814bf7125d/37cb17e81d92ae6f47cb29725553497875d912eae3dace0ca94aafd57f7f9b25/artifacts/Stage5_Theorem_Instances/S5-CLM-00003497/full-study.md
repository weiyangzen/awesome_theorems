# Full study: the asymptotic Ringel projection

## N0 — Eventual quantifier

The target is an eventual assertion in `Filter.atTop`: one threshold must work
for every later natural `n`, every finite vertex type `V`, every simple graph
`T` on `V`, and both hypotheses that `T` is a tree and has exactly `n` edges.
The output retains a whole family of `2n+1` embeddings, not merely one copy.

## N1 — Cyclic input

The stronger input returns the same embedding family requested by Ringel plus
three facts: each embedding is a cyclic translate of the zeroth embedding, the
mapped edge sets are pairwise disjoint, and their supremum is the complete
graph. The finite type, tree, and edge-count hypotheses are passed unchanged.

## N2 — Forgetful projection

For a fixed sufficiently large `n`, destructure the cyclic witness. Keep the
embedding family verbatim. Delete only the cyclic-translate conjunct, because
Ringel does not request it. The disjointness proof and supremum equality already
have exactly the target types, so no graph, vertex type, or equality is cast or
rewritten. `Filter.Eventually.mono` performs this pointwise projection without
changing the threshold.

## N3 — Output

The retained data form the exact Ringel witness: pairwise edge-disjoint mapped
copies whose supremum is the top simple graph on `Fin (2*n+1)`. Downstream users
may rely on both outputs and on the original eventual uniformity. The only
exceptional case is a failed input premise; the implication then supplies no
witness, exactly as its type says. The trust boundary is the stronger cyclic
mathematical input; the claim-owned projection itself is a transparent Lean
term with no local oracle, parser extension, shadowing declaration, or semantic
substitution.

## Provenance and trust boundary

The frozen provider bytes identify the source statements but their bodies are
not proof authority: both source declarations contain `sorryAx`. The active
files therefore use `Mathlib` and mention the provider module and qualified
Ringel name only inside provenance comments. The canonical Master must compute
the actual elaborated expressions and all transitive constants from integrated
sources; worker-supplied digests are bindings to recheck, not acceptance.

## Exceptional cases and downstream use

No small-`n` construction is asserted: eventuality packages the threshold from
the cyclic theorem. No decidable equality instance is introduced, and the
argument works with `Finite V` exactly as frozen. Any downstream theorem that
only needs a Ringel decomposition can apply the projection without retaining
or inspecting cyclicity.
