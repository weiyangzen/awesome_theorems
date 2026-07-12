# THM-M-0026 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for Hilbert's Nullstellensatz. The
repository supplies the gloss "correspondence between maximal ideals of a polynomial ring over an
algebraically closed field and points of the algebraic set," attributes it to David Hilbert, and
dates it 1893. That identifies the classical maximal-ideal/affine-point theorem family, but it does
not yet fix a binder-complete proposition.

In particular, the catalog does not state the finite variable index, whether the coefficient field
and the field of points are identical, whether the result is an existential classification, an
`Iff`, or a bijection of spaces, or what "points of the algebraic set" means. It also does not say
whether the intended root is the weak maximal-ideal form or the strong radical/zero-locus identity.
This intake preserves those choices for source review rather than silently selecting the most
convenient formal declaration.

An inspected Stacks Project source lead and a close pinned mathlib implementation are recorded in
the source crosswalk. Pinned mathlib contains both
`MvPolynomial.isMaximal_iff_eq_vanishingIdeal_singleton` and the stronger
`MvPolynomial.vanishingIdeal_zeroLocus_eq_radical`. Their presence is discovery evidence, not proof
credit for an as-yet-unfrozen root. `IntakeProbe.lean` only confirms that these adjacent APIs
elaborate in the pinned environment.

Lifecycle is `planned`; the provisional root vector is `[H1, M3, R4]`. The canonical mathematical
statement and Lean expression remain null, every downstream phase remains open, and no H0/M0/R0,
audit completion, theorem completion, accepted receipt, or master acceptance is claimed.
