# THM-M-0276 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the Banach open mapping theorem.
The repository gives Stefan Banach, 1929, and only the gloss "a surjective bounded linear
operator is an open map." Its `已验证` ("verified") label is untrusted inventory metadata under
rev-5.6, not a source audit, exact Lean proposition, or proof receipt.

The gloss identifies the classical functional-analysis theorem family, but omits
proposition-changing choices. It does not say whether the scalars are real, complex, or a more
general valued field; state explicitly that both spaces are Banach; define "bounded linear
operator"; choose ordinary linear versus semilinear maps; or define "open map." Those choices
cannot be supplied silently at intake.

A versioned set of Technion functional-analysis lecture notes was inspected as a modern
lecture-note source lead. Its Open Mapping Theorem states that an onto bounded operator between Banach
spaces is open and presents the standard Baire-category proof route. The printed proof has a
material but apparently repairable typo: its Baire cover repeats the unit ball where the subsequent
argument requires balls of radius `n`. No accepted correction or independent review is recorded.
The notes fix the scalars to real or complex numbers, are not cited by the catalog, and have no
complete source-to-Lean transport. They therefore support only provisional `H2`, not `H0`.

Pinned mathlib contains the direct exact-topic declaration `ContinuousLinearMap.isOpenMap` in
`Mathlib.Analysis.Normed.Operator.Banach`. It proves openness for a surjective continuous
semilinear map between complete normed spaces over compatible nontrivially normed fields. The
same-field real/complex textbook form is a specialization of that more general interface, but no
specialization is selected or credited at intake. `IntakeProbe.lean` authenticates this interface,
supporting declarations, and representative axiom reports only.

The provisional vector is `[H2, M3, R4]`: a named modern theorem-and-proof-route lead exists but
its printed Baire-cover typo, catalog identity, exact assumptions, correction status, transport, and independent review remain
open; direct pinned interfaces exist but the canonical target and checked bridge are not frozen;
and no source-faithful readable proof reconstruction exists for an exact root.

`instance.json` is the structured scope authority. `scope-map.md` and
`source-statement-crosswalk.md` freeze the unresolved choices and non-substitution boundary.
`task-dag.json` keeps all six downstream phases open. No H0, M0, R0, accepted proof state, audit
completion, theorem completion, or master acceptance is claimed.
