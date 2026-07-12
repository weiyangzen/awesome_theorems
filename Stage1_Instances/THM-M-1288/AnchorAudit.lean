import Mathlib.Analysis.FunctionalSpaces.SobolevInequality

/-!
# THM-M-1288 pinned anchor probes

The checked theorem below is mathlib's non-sharp Gagliardo-Nirenberg-Sobolev
inequality.  Its constant, `ENNReal` norm, and Frechet derivative do not match
the frozen Talenti constant, real integral norm, and gradient target.  This
module therefore records supporting infrastructure, not a proof of the root.
-/

noncomputable section

open MeasureTheory
open scoped ENNReal NNReal

namespace Stage1Instances.THM_M_1288.AnchorAudit

universe u v

/-- Direct checked wrapper around the closest pinned mathlib theorem. -/
theorem pinnedGagliardoNirenbergSobolev
    {E : Type u} {F : Type v}
    [NormedAddCommGroup E] [NormedSpace Real E] [MeasurableSpace E]
    [BorelSpace E] [FiniteDimensional Real E]
    [NormedAddCommGroup F] [NormedSpace Real F] [FiniteDimensional Real F]
    (mu : Measure E) [mu.IsAddHaarMeasure]
    {u : E -> F} (hu : ContDiff Real 1 u) (hcu : HasCompactSupport u)
    {p p' : NNReal} (hp : 1 <= p) (hn : 0 < Module.finrank Real E)
    (hp' : (p' : Real)⁻¹ = (p : Real)⁻¹ - (Module.finrank Real E : Real)⁻¹) :
    eLpNorm u (p' : ENNReal) mu <=
      (MeasureTheory.SNormLESNormFDerivOfEqConst F mu (p : Real) : ENNReal) *
        eLpNorm (fderiv Real u) (p : ENNReal) mu := by
  exact MeasureTheory.eLpNorm_le_eLpNorm_fderiv_of_eq mu hu hcu hp hn hp'

#check MeasureTheory.eLpNorm_le_eLpNorm_fderiv_one
#check MeasureTheory.eLpNorm_le_eLpNorm_fderiv_of_eq_inner
#check MeasureTheory.eLpNorm_le_eLpNorm_fderiv_of_eq
#check MeasureTheory.eLpNorm_le_eLpNorm_fderiv_of_le
#check MeasureTheory.SNormLESNormFDerivOfEqConst
#print axioms pinnedGagliardoNirenbergSobolev

end Stage1Instances.THM_M_1288.AnchorAudit
