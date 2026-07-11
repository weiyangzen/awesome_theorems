import «Stage1_Instances».«THM-M-0395».Statement

/-!
# THM-M-0395 independent validation probes

These probes reconstruct the three implemented terminal transports without
importing `Proof.lean`. They validate only those elementary transports; the
Faltings root and its arithmetic-geometric inputs remain open.
-/

noncomputable section

open Stage1Rev56.THMM0395

universe u v

namespace Stage1Rev56.THMM0395.Validation

theorem independent_finite_of_injective {α : Type u} {β : Type v} [Finite β]
    (f : α → β) (hf : Function.Injective f) : Finite α :=
  Finite.of_injective f hf

theorem independent_two_injections {α : Type u} {β : Type v} {γ : Type*}
    [Finite γ] (f : α → β) (g : β → γ) (hf : Function.Injective f)
    (hg : Function.Injective g) : Finite α := by
  letI : Finite β := Finite.of_injective g hg
  exact Finite.of_injective f hf

theorem independent_finite_points_transport
    {K : Type u} [Field K] [NumberField K] (C : CurveOver K)
    (h : (Set.univ : Set (RationalPoint C.scheme C.structureMap)).Finite) :
    Finite (RationalPoint C.scheme C.structureMap) :=
  (finite_points_iff_finite_univ C).2 h

#print axioms independent_finite_of_injective
#print axioms independent_two_injections
#print axioms independent_finite_points_transport

end Stage1Rev56.THMM0395.Validation
