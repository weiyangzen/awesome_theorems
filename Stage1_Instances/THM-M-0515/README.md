# THM-M-0515 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository label "Kronecker's
Jugendtraum". The repository supplies only the gloss "generation of class fields of imaginary
quadratic fields". That identifies a theorem family, not one proposition: it does not say which
class fields are quantified over, which special values generate them, whether generation is over
the quadratic field or another base, or which conductor and exceptional cases are included.

The intake therefore freezes that ambiguity and rejects several tempting substitutions. The root
is `[H3, M4, R4]`. A pinned Lean probe confirms that mathlib exposes CM fields, rings of integers,
class groups, and class numbers, but it is not the missing class-field-generation theorem. Exact
commands and results are recorded in `validation.md`.

