# Proof outline — large-n Kotzig statement

1. Freeze the exact provider record and byte range. The FormalConjectures body
   is not proof evidence because it contains `sorryAx`.
2. Restate the proposition under the claim-owned namespace with active
   `Mathlib` semantics and no local semantic declarations.
3. Prove bidirectional identity of the two proposition surfaces by `Iff.rfl`.
4. Expose forward and reverse transport theorems. Each takes the relevant exact
   proposition as an explicit premise and returns it at the definitionally
   identical surface; no provider body is cited.
5. Audit the identity and transport boundary in `Audit.lean`.
6. Bind every proof node to a unique readable fragment and every fragment back
   to its proof node.
7. Run the task-local `--no-lean` validator, seal the trace, and hand the exact
   bytes to Master for canonical trust-zero compilation and acceptance.

The mathematical content retained by the exact proposition is: eventuality in
`n`; arbitrary finite vertex type; arbitrary simple graph `T`; tree and edge
count hypotheses; a family of vertex embeddings; cyclic translation from one
base embedding; pairwise edge-disjoint mapped copies; and equality of their
supremum with the complete graph. No hypothesis or conclusion is distilled
away.
