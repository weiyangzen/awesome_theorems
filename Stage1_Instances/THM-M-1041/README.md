# THM-M-1041 rev-5.6 intake

This directory is the `planned` intake for the Hille-Yosida theorem. It identifies the intended
claim as the generator characterization for strongly continuous semigroups on a Banach space,
while leaving the exact classical variant, scalar field, and constants to source inspection in the
statement phase.

The legacy Lean module is discovery input only. Its terminal predicates contain the desired
resolvent and generator facts as abstract `Prop` fields, so its wrappers receive no statement or
proof credit. The provisional root vector is `[H2, M4, R4]`; no exact Lean target, audit completion,
or theorem completion is claimed.

The scope map, source crosswalk, and open task DAG define the downstream work. Intake validation
and its deliberately narrow boundary are recorded in `validation.md`.
