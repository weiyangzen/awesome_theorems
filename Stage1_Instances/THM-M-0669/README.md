# THM-M-0669 rev-5.6 intake

This directory is the fail-closed `planned` intake for Tarski's quantifier-elimination theorem for
real closed fields. The repository gloss says only "quantifier elimination for real closed fields".
The human scope is therefore frozen to the standard theorem that every first-order formula over a
real closed field, in a fixed language of ordered rings or a checked definitionally equivalent
language, is equivalent over the theory of real closed fields to a quantifier-free formula.

The intake does not choose between ordered-ring primitives and a pure ring language with definable
order, and it does not silently identify quantifier elimination with decidability. Those choices,
the exact theory axioms, free-variable convention, uniform syntactic transformation, and primary
source anchor remain statement-phase obligations.

`IntakeProbe.lean` checks only relevant pinned mathlib ingredients. It is not the target theorem and
receives no proof credit. The provisional root vector is `[H1, M4, R4]`; no exact Lean target, H0,
M0, audit completion, or theorem completion is claimed. The scope map, source crosswalk, and open
task DAG record the downstream boundary, while `validation.md` records the self-tests.
