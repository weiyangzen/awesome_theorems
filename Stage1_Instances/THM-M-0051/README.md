# THM-M-0051 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the catalog entry named the
"Grassmann identity." The repository supplies only the gloss "an identity about exterior algebra,"
attributes it to Hermann Grassmann in 1844, and labels it verified. Under rev-5.6 that label is
untrusted inventory metadata, not a source audit, an exact proposition, or proof evidence.

The gloss does not contain a formula. It does not specify whether the intended result is a
square-zero or anticommutation identity for exterior generators, an identity for alternating
products, a Grassmann-Pluecker relation, the universal property of an exterior algebra, or another
historical identity. It fixes no coefficient ring, module, degree, binders, hypotheses, conclusion,
sign convention, or boundary cases. Choosing any familiar result at intake would substitute
mathematics that the source record does not state.

A bibliographic record for Grassmann's *Die Lineale Ausdehnungslehre ein neuer Zweig der
Mathematik* was inspected as a historical source lead. It matches the catalog's author and 1844
work family, but no original or reprint passage, exact formula, definitions, proof, translation,
correction, or erratum was inspected. The record therefore cannot disambiguate the target and is
not `H0` evidence.

Pinned mathlib supplies a developed exterior-algebra API. `IntakeProbe.lean` authenticates several
nearby interfaces, including square-zero, generator anticommutation, alternating multiplication,
functoriality, and grading. The declarations are mutually different candidate surfaces; none is
source-mapped to the catalog entry, and the probe grants no proof credit.

The provisional root vector is `[H1, M4, R4]`: `H1` records a matching historical work lead with the
exact claim and proof mapping unresolved; `M4` records that no usable formal artifact for the
unidentified exact proposition is credited; and `R4` records that no source-faithful proof route can
be reconstructed before the target is identified. All six downstream phases remain open in
`task-dag.json`.

No canonical proposition, exact Lean target, H0, M0, R0, accepted execution state, audit completion,
theorem completion, or master acceptance is claimed.
