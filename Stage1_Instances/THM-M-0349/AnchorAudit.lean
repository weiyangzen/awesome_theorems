import Mathlib.Analysis.Fourier.AddCircle

/-!
# THM-M-0349: pinned mathlib anchor audit

This module checks the two nearest reusable declarations found in the pinned
mathlib tree. Neither is the conjugate-function theorem: one supplies density
of Fourier monomials in finite-exponent `Lp`, and the other supplies Fourier
series convergence only at exponent two.
-/

namespace Stage1Instances.THM_M_0349.AnchorAudit

open MeasureTheory
open scoped ENNReal

#check @span_fourierLp_closure_eq_top
#check @hasSum_fourier_series_L2

/-- The pinned density result is useful for a later extension-from-a-dense-
subspace proof, but it constructs no conjugate operator and proves no bound. -/
theorem finiteExponentFourierDensity {T : Real} [hT : Fact (0 < T)]
    {p : ENNReal} [Fact (1 <= p)] (hp : p ≠ (⊤ : ENNReal)) :
    (Submodule.span Complex (Set.range (@fourierLp T hT p _))).topologicalClosure = ⊤ := by
  exact span_fourierLp_closure_eq_top hp

/-- The pinned Hilbert-basis result closes Fourier expansion only in `L2`; it
does not give strong-type boundedness for all `1 < p < infinity`. -/
theorem exponentTwoFourierExpansion {T : Real} [hT : Fact (0 < T)]
    (f : Lp Complex 2 (@AddCircle.haarAddCircle T hT)) :
    HasSum (fun i => fourierCoeff f i • fourierLp 2 i) f := by
  exact hasSum_fourier_series_L2 f

end Stage1Instances.THM_M_0349.AnchorAudit

#print axioms Stage1Instances.THM_M_0349.AnchorAudit.finiteExponentFourierDensity
#print axioms Stage1Instances.THM_M_0349.AnchorAudit.exponentTwoFourierExpansion
