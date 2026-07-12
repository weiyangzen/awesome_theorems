# THM-M-0533 rev-5.6 intake

This directory is the `planned` intake for the Mayer-Vietoris sequence. It freezes the intended
human claim as the long exact singular-homology sequence associated to a space covered by two
subspaces, with the maps induced by the inclusions and the connecting homomorphism. The exact
cover hypothesis, reduced versus unreduced convention, coefficients, signs, and endpoint behavior
remain decisions for the statement phase and must be taken from an inspected source.

The repository metadata phrase `space union's homology sequence` and its `verified` label are
discovery input only. The pinned mathlib tree contains a Mayer-Vietoris sequence for **sheaf
cohomology**; that is a related but different theorem and receives no proof credit for this
singular-homology target. No theorem-specific legacy slot was found.

The provisional root vector is `[H3, M4, R4]`. This intake claims neither an exact Lean expression,
source fidelity (`H0`), kernel closure, audit completion, nor theorem completion. The scope map,
source crosswalk, and open task DAG define the downstream work; validation evidence is recorded in
`validation.md`.

The statement phase now freezes and elaborates the open-cover, integral singular-homology target
in `Statement.lean`; see `statement-receipt.md`. This is provisional node evidence only and does
not change the planned lifecycle or claim proof/theorem completion.
