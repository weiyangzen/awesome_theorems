# THM-M-0065 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for `THM-M-0065`, the Jordan-Holder
theorem for groups. The repository supplies only the gloss that a group's composition series is
unique up to isomorphism, attributes it to Camille Jordan and Otto Holder in 1889, and labels it
verified. Under rev-5.6 that label is untrusted inventory metadata, not a cited human proof, an
exact proposition, or kernel evidence.

The gloss identifies the standard theorem family but omits proposition-changing details. It does
not define a group composition series, distinguish subnormality from global normality, state an
existence or finite-length premise, fix endpoints, or explain that uniqueness normally means equal
length and simple quotient factors matched up to permutation and group isomorphism. Intake
preserves that family without silently choosing those clauses.

J. S. Milne's author-hosted *Group Theory*, version 4.01 (2025), was inspected as a
modern source lead. Definition 6.1 and Theorem 6.2 on printed pages 87-89 give the finite-group
subnormal-series statement, including equal lengths and a permutation matching quotient groups by
isomorphism. Remark 6.3 extends it to any group possessing a finite composition series. The catalog
does not cite this mutable source, its correction history was not audited, the finite versus
conditional-arbitrary domain remains to be selected, and no independent review is recorded. It
therefore supports `H1`, not `H0`.

Pinned mathlib contains a very close abstract result:
`CompositionSeries.jordan_holder` in `Mathlib.Order.JordanHolder`. It proves that two composition
series with the same head and last are equivalent in any `JordanHolderLattice`. The equivalence
matches adjacent factors through a bijection of steps. However, the same module explicitly leaves
a subgroup instance and group-specific API as TODO, and no such instance was located. The abstract
lattice theorem and the existing module instance are not substitutes for the requested group
theorem without a checked group transport.

`IntakeProbe.lean` authenticates the abstract pinned API and axiom report only. The provisional root
vector is `[H1, M3, R4]`: a complete modern proof source lead has unresolved mapping; a strong
formal interface and generic theorem exist but no exact group target is frozen or credited; and no
source-faithful readable proof reconstruction exists. The PDF front matter says November 6 while
its revision history says November 7; that one-day discrepancy remains part of the source audit.
`instance.json` is the structured scope
authority and `task-dag.json` leaves all six downstream phases open. No H0, M0, R0, accepted state,
audit completion, theorem completion, or master acceptance is claimed.
