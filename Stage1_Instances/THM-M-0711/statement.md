# Canonical Lean statement

`Statement.lean` freezes the repository gloss as the standard fixed-group Novikov-Boone claim.
It existentially quantifies a natural number `n` of generators and a finite relator set
`rels : Finset (FreeGroup (Fin n))`. An input word is an effective list of pairs in
`Fin n x Bool`; the Boolean chooses the generator or its inverse. `evalWord` evaluates that list
in the free group, and `PresentedGroup.mk` maps it to the quotient by the relators.

The conclusion is the literal negation of mathlib's `ComputablePred` for the identity predicate.
Thus the target says that no computable Boolean decision procedure exists for all encoded words
of one fixed finite presentation. It does not assert that every finitely presented group has an
undecidable word problem and does not replace the group word problem with a different undecidable
problem.

The imports are deliberately limited to `Mathlib.Computability.Halting`, which defines
`ComputablePred`, and `Mathlib.GroupTheory.PresentedGroup`, which supplies free and presented
groups. The elaborated declaration is `Stage1.THM_M_0711.NovikovBooneTarget`.

This phase freezes the exact Lean proposition selected for the repository's terse source gloss.
It does not clear the separately recorded primary-source crosswalk debt: the historical edition,
page, exact strength, and independent source review remain open. It also supplies no proof term.
