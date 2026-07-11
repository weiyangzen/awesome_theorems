# THM-M-0087 rev-5.6 intake

This is the `planned` rev-5.6 instance for the Gabriel-Popescu theorem. Historical
file `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_133.lean` is discovery input
only; none of its statement, wrapper, or build claims receives rev-5.6 proof credit.

The human claim frozen for subsequent audit is the classical representation
theorem: a Grothendieck abelian category with a generator is equivalent to a
Serre quotient of a module category. The existing Lean candidate instead packages
the full and faithful functor `Hom(G,-)` and a finite-limit-preserving left adjoint.
Whether that candidate is exactly equivalent to the quotient formulation is an
open statement-phase obligation, not an assumed identification.

The structured scope is in `intake.json`, the mathematical boundary in
`scope-map.md`, and the source/Lean mismatch in `source-statement-crosswalk.md`.

## Statement verdict

`Statement.lean` now freezes and elaborates the pinned mathlib formulation of
Gabriel-Popescu with one direct import. The declaration explicitly quantifies a
Grothendieck abelian category and separator and concludes fullness, faithfulness,
the tensor-Hom adjunction, and finite-limit preservation of the left adjoint.
The exact declaration and boundary are recorded in `statement.json`.

This statement node does not silently claim a constructed equivalence with a
named Serre quotient. The pinned mathlib module says its checked formulation
implies that characterization, but that transport is a later proof obligation.
Master acceptance and every proof/release gate remain outstanding.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H1, M3, R3]`. The first
failed theorem gate is exact-statement elaboration: no normalized expression hash,
environment fingerprint, checked transport to the quotient formulation, or
mutation evidence has been accepted. The theorem is not complete.

## Validation boundary

The commands in `validation.md` validate manifest membership, repository
structure, JSON syntax, and dossier-local references only. No Lean proof or
historical build result is claimed by this intake node.
