import Mathlib.Analysis.Calculus.VectorField

/-!
# THM-M-1258 anchor audit

These probes elaborate the pinned mathlib declarations used to state the frozen bracket-generating
condition. They are supporting infrastructure, not a theorem that the condition holds.
-/

#check VectorField.lieBracket
#check VectorField.lieBracket_swap
#check VectorField.lieBracket_self
#check Submodule.span
#check Submodule.span_eq_top_of_span_eq_top

