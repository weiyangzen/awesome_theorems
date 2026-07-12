import Statement

/-!
# THM-M-1016 conditional obligation composition

This module checks the final continuous-mapping/Slutsky composition.  The scaled Frechet
remainder remains an explicit premise; no proof of the delta method is asserted.
-/

noncomputable section

open Filter MeasureTheory
open scoped Topology

namespace Stage1Instances.THM_M_1016

universe u v w

/-- Once the scaled nonlinear remainder is negligible in measure, the frozen conclusion follows. -/
theorem deltaMethod_of_remainder
    (Omega : Type u) (Omega' : Type v)
    [MeasurableSpace Omega] [MeasurableSpace Omega']
    (mu : Measure Omega) (mu' : Measure Omega')
    [IsProbabilityMeasure mu] [IsProbabilityMeasure mu']
    (E : Type w) (F : Type*)
    [NormedAddCommGroup E] [NormedSpace Real E] [FiniteDimensional Real E]
    [MeasurableSpace E] [BorelSpace E]
    [NormedAddCommGroup F] [NormedSpace Real F] [FiniteDimensional Real F]
    [MeasurableSpace F] [BorelSpace F]
    (X : Nat -> Omega -> E) (Z : Omega' -> E) (theta : E)
    (r : Nat -> Real) (_hr_pos : forall n, 0 < r n) (_hr_inf : Tendsto r atTop atTop)
    (g : E -> F) (g' : E →L[Real] F) (_hg_meas : Measurable g)
    (_hg_diff : HasFDerivAt g g' theta)
    (hX : TendstoInDistribution
      (fun n omega => r n • (X n omega - theta)) atTop Z (fun _ => mu) mu')
    (hrem : TendstoInMeasure mu
      (fun n omega =>
        r n • (g (X n omega) - g theta) - g' (r n • (X n omega - theta)))
      atTop 0)
    (hmeas : forall n, AEMeasurable
      (fun omega => r n • (g (X n omega) - g theta)) mu) :
    TendstoInDistribution
      (fun n omega => r n • (g (X n omega) - g theta)) atTop
      (fun omega => g' (Z omega)) (fun _ => mu) mu' := by
  have hlinear : TendstoInDistribution
      (fun n omega => g' (r n • (X n omega - theta))) atTop
      (fun omega => g' (Z omega)) (fun _ => mu) mu' := by
    simpa [Function.comp_def] using hX.continuous_comp g'.continuous
  exact tendstoInDistribution_of_tendstoInMeasure_sub
    (l := atTop) (μ'' := mu) (μ' := mu')
    (X := fun n omega => g' (r n • (X n omega - theta)))
    (Y := fun n omega => r n • (g (X n omega) - g theta))
    (Z := fun omega => g' (Z omega)) hlinear hrem hmeas

#print axioms deltaMethod_of_remainder

end Stage1Instances.THM_M_1016
