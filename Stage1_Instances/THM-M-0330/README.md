# THM-M-0330 rev-5.6 intake

This directory is the `planned` intake dossier for the Hille-Yosida theorem named by the Stage0
phrase "characterization of generators of strongly continuous semigroups". The intake does not
choose silently among the contraction and exponentially bounded forms of the theorem. That choice,
including the scalar field and all constants, is an explicit statement-phase task.

`THM-M-1041` and legacy module `S1_M_234.lean` concern the same theorem family and are discovery
inputs only. They do not transfer scope, accepted state, or proof credit to this target. The root is
provisionally `[H1, M4, R4]`: published source candidates are known, but no pinpoint source audit or
exact Lean proposition has been accepted. Audit completion and theorem completion are both false.

The statement phase has now selected and kernel-elaborated the real Banach-space contraction form.
Its concrete generator, semigroup, and resolvent predicates are in `Statement.lean`; the frozen
expression and environment fingerprint are in `statement.json`, and exact commands are recorded in
`statement-validation.md`. This is statement-only evidence pending master acceptance: the root
remains `[H1, M4, R4]`, with no source-fidelity, proof, audit-completion, or theorem-completion claim.
