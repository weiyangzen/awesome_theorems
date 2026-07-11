import «Stage1_Instances».«THM-M-0395».Statement

/-!
# THM-M-0395 proof execution

This module implements the elementary finiteness transports used at the end of
the frozen proof route.  The arithmetic-geometric inputs to that route remain
open, so this module deliberately does not declare Faltings's theorem.
-/

noncomputable section

open Stage1Rev56.THMM0395

universe u v

namespace Stage1Rev56.THMM0395.Proof

/-- Finiteness transports backwards through an injective map.  This is the
set-theoretic transport required by the terminal composition after base change
and the Abel-Jacobi embedding have been constructed. -/
theorem finite_of_injective_to {α : Type u} {β : Type v} [Finite β]
    (f : α → β) (hf : Function.Injective f) : Finite α :=
  Finite.of_injective f hf

/-- The same terminal transport with both frozen injections made explicit.
The finite target, base-change injection, and Abel-Jacobi injection are genuine
premises; none is manufactured by this theorem. -/
theorem finite_of_two_injections {α : Type u} {β : Type v} {γ : Type*}
    [Finite γ] (baseChange : α → β) (abelJacobi : β → γ)
    (hBaseChange : Function.Injective baseChange)
    (hAbelJacobi : Function.Injective abelJacobi) : Finite α := by
  letI : Finite β := finite_of_injective_to abelJacobi hAbelJacobi
  exact finite_of_injective_to baseChange hBaseChange

/-- Convert the universal-set finiteness encoding back to the exact conclusion
used by the canonical statement. -/
theorem finite_points_of_finite_univ
    {K : Type u} [Field K] [NumberField K] (C : CurveOver K)
    (h : (Set.univ : Set (RationalPoint C.scheme C.structureMap)).Finite) :
    Finite (RationalPoint C.scheme C.structureMap) :=
  (finite_points_iff_finite_univ C).2 h

#print axioms finite_of_injective_to
#print axioms finite_of_two_injections
#print axioms finite_points_of_finite_univ

end Stage1Rev56.THMM0395.Proof
