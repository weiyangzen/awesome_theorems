# THM-M-0979 rev-5.6 intake

`THM-M-0979` is the counting-combinatorics catalog row named `Bernstein inequality`. The
repository gives only Sergei Bernstein, 1924, and the gloss "tail probability of a sum." It does
not give a formula, hypotheses, a source locator, or a formal declaration. The catalog's
`verified` label is untrusted inventory metadata under rev-5.6.

## Intake result

This dossier preserves the Bernstein probability-inequality family but leaves the canonical
statement null. The source corpus contains a second row, `THM-M-0995`, whose Chinese title is a
translation of the same name and whose attribution, year, gloss, importance, and claimed status
are otherwise identical. That separately owned target has a modern bounded-summand upper-tail
candidate and Lean artifacts. They are useful discovery inputs, but no statement choice, task
state, or proof credit transfers to this target.

An author-hosted second edition of Roman Vershynin's *High-Dimensional Probability* was inspected
as a modern source lead. Section 2.9 contains several nonidentical Bernstein inequalities: a
proved subexponential form, a weighted corollary, and a bounded variance-sensitive form with a
factor `2`. The foreign `THM-M-0995` candidate instead uses a bounded form without that factor.
This confirms that the catalog gloss does not select constants, tail convention, or assumptions.
The modern text also points to Bernstein's 1924 work, but the historical primary text was not
inspected or admitted.

## Formal boundary

`IntakeProbe.lean` authenticates pinned moment-generating-function, Chernoff, sub-Gaussian sum,
independence, and variance interfaces. It also elaborates a proposition shape parameterized by an
unresolved prefactor. That definition is deliberately noncanonical and proves nothing. A bounded
local search found no separately named terminal scalar Bernstein tail theorem in pinned mathlib.

The provisional vector is `[H1, M3, R4]`: modern complete proof material for one member of the
family is located but exact source identity and mapping are open; only candidate statement shape
and adjacent Lean interfaces exist; and no accepted source-faithful reconstruction exists. All
six downstream phases remain open. No H0, M0, R0, accepted execution state, audit completion,
theorem completion, or master acceptance is claimed.
