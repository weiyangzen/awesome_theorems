import Statement

/-!
# THM-M-1268 independent local validation probe

This module deliberately does not import `Proof`. It reconstructs the exact
frozen root from the pinned weak-closure and semicontinuity interfaces.
-/

noncomputable section

namespace Stage1Instances.THM_M_1268.Validation

open Set

universe u

abbrev Sublevel {E : Type u} (f : E -> EReal) (r : EReal) : Set E :=
  f ⁻¹' Iic r

theorem convex_sublevel {E : Type u} [NormedAddCommGroup E] [NormedSpace Real E]
    {f : E -> EReal} (hf : IsExtendedRealConvex f) (r : EReal) :
    Convex Real (Sublevel f r) := by
  intro x hx y hy a b ha hb hab
  refine (hf.2 x y a b ha hb hab).trans ?_
  calc
    (a : EReal) * f x + (b : EReal) * f y
        <= (a : EReal) * r + (b : EReal) * r := by
          exact add_le_add
            (mul_le_mul_of_nonneg_left hx (EReal.coe_nonneg.mpr ha))
            (mul_le_mul_of_nonneg_left hy (EReal.coe_nonneg.mpr hb))
    _ = r := by
      rw [← EReal.right_distrib_of_nonneg
        (EReal.coe_nonneg.mpr ha) (EReal.coe_nonneg.mpr hb),
        ← EReal.coe_add, hab, EReal.coe_one, one_mul]

theorem convex_closed_is_weak_closed
    {E : Type u} [NormedAddCommGroup E] [NormedSpace Real E]
    {s : Set E} (hconvex : Convex Real s) (hclosed : IsClosed s) :
    IsClosed ((toWeakSpace Real E).symm ⁻¹' s) := by
  have himage : (toWeakSpace Real E) '' s =
      (toWeakSpace Real E).symm ⁻¹' s := by
    ext x
    constructor
    · rintro ⟨y, hy, rfl⟩
      simpa using hy
    · intro hx
      exact ⟨(toWeakSpace Real E).symm x, hx, by simp⟩
  rw [← himage, ← closure_eq_iff_isClosed]
  rw [← hconvex.toWeakSpace_closure Real, hclosed.closure_eq]

/-- An exact-root reconstruction independent of the local proof module. -/
theorem independentlyReconstructedWeakLowerSemicontinuity :
    WeakLowerSemicontinuityTarget.{u} := by
  intro E _ _ f hf
  constructor
  · intro hweak
    simpa [OnWeakSpace] using
      hweak.comp (map_continuous (toWeakSpaceCLM Real E))
  · intro hnorm
    rw [lowerSemicontinuous_iff_isClosed_preimage]
    intro r
    exact convex_closed_is_weak_closed (convex_sublevel hf r)
      (lowerSemicontinuous_iff_isClosed_preimage.mp hnorm r)

#print axioms convex_sublevel
#print axioms convex_closed_is_weak_closed
#print axioms independentlyReconstructedWeakLowerSemicontinuity

end Stage1Instances.THM_M_1268.Validation
