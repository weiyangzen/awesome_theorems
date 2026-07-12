import Statement

/-!
# THM-M-0346 conditional obligation composition

The analytic Carleson-Hunt theorem and both encoding transports remain explicit
premises. This file checks their composition into the exact frozen target only.
-/

open Filter MeasureTheory

namespace Stage1.THM_M_0346

noncomputable section

/-- Output contract after the representative, coefficient, and cutoff transports
have converted an integrated Carleson-Hunt theorem to the frozen encoding. -/
def TransportedCarlesonHunt : Prop :=
  forall f : Lp Complex 2 (@AddCircle.haarAddCircle (1 : Real) inferInstance),
    ∀ᵐ x ∂(@AddCircle.haarAddCircle (1 : ℝ) inferInstance),
      Tendsto (fun N : ℕ ↦ symmetricPartialSum f N x) atTop (nhds (f x))

/-- Checked conditional assembly into the exact canonical root. -/
theorem root_of_transported_carleson_hunt
    (transported : TransportedCarlesonHunt) : CarlesonTarget := by
  exact transported

#print axioms root_of_transported_carleson_hunt

end

end Stage1.THM_M_0346
