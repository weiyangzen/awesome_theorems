# THM-M-0668 rev-5.6 intake

This directory is the fail-closed `planned` intake for the repository label "quantifier
elimination". The source inventory says only "quantifier elimination for a theory" and names no
theory, language, structure class, theorem, hypotheses, or conclusion. Quantifier elimination is
normally a property of a fixed theory, not an unconditional theorem of first-order logic. The
inventory wording therefore does not yet determine one proposition that could receive statement or
proof credit.

The intended family is the standard semantic property: every formula in a fixed first-order
language is equivalent, modulo a fixed theory, to a quantifier-free formula with the same free
variables. This description is a scope boundary, not a broadened replacement theorem. The
statement phase must either identify the source-intended theory and exact result or classify the
generic inventory item as a definitional/family heading rather than a theorem target.

The provisional root vector is `[H5, M3, R4]`. `M3` records only pinned mathlib syntax and semantic
interfaces checked by `IntakeProbe.lean`; mathlib's prenex-normal-form theorem does not eliminate
quantifiers. No canonical Lean proposition, source proof, audit completion, or theorem completion
is claimed. The scope map, source crosswalk, and open task DAG preserve the unresolved choices, and
`validation.md` records the intake checks.
