# THM-M-0085 rev-5.6 intake

This directory contains the `planned` dossier and self-tested statement for Beck's monadicity
theorem. `Statement.lean` freezes the creates-`G`-split-coequalizers form for a fixed adjunction:
creation of those coequalizers implies that its Eilenberg-Moore comparison functor is an
equivalence. The has/preserves/reflects and reflects-isomorphisms criteria remain alternate
sufficient variants and are not silently substituted.

The legacy Lean module is discovery input only, despite containing checked mathlib wrappers. Under
the uniform rev-5.6 baseline those declarations receive no inherited statement or proof credit.
The provisional root vector remains `[H2, M4, R4]`; statement elaboration supplies no proof credit
and theorem completion is not claimed.

The scope map, source crosswalk, and open task DAG define downstream work. Intake checks are in
`validation.md`; exact elaboration, environment hashes, checked expansion, and structural mutation
results are in `statement.json` and `statement-validation.md`.
