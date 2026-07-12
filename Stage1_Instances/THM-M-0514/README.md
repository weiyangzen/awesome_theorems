# THM-M-0514 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository label "complex
multiplication theory". The source inventory adds only the gloss "class field theory of imaginary
quadratic fields". That names a theory containing several major results, not one proposition.

In particular, the record does not choose between the first main theorem (algebraicity and class
field generation by singular moduli), the second main theorem (the Artin action on CM values), a
ring-class-field variant for a nonmaximal order, or a statement about CM elliptic curves. Those
statements have different objects, hypotheses, moduli functions, conductors, and conclusions.
Choosing one would substitute invented mathematics for the source record.

The intake therefore freezes the ambiguity and exclusions rather than a theorem. The root remains
`[H3, M4, R4]`. A pinned Lean probe confirms that mathlib has nearby number-field, CM-field,
class-group, class-number, and elliptic-curve APIs. These are prerequisites only: mathlib's
`NumberField.IsCMField` is not the classical main theorem of complex multiplication. Exact commands
and results are recorded in `validation.md`.
