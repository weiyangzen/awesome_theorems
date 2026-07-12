import Statement

/-!
# THM-M-1056 conditional obligation composition

This module makes the mathematical Oseledets package an explicit premise and
checks only its composition into the frozen canonical target. It contains no
proof of the multiplicative ergodic theorem.
-/

open MeasureTheory

namespace Stage1Instances.THM_M_1056

universe u v

/-- The still-open output of the forward/backward filtration, transversality,
and measurable-projection construction. -/
def OseledetsCorePackage : Prop :=
  forall (Omega : Type u) [MeasurableSpace Omega]
    (mu : Measure Omega) [IsProbabilityMeasure mu]
    (E : Type v) [NormedAddCommGroup E] [NormedSpace Real E]
    [FiniteDimensional Real E] [MeasurableSpace E] [BorelSpace E]
    (hE : 0 < Module.finrank Real E)
    (T : Omega ≃ᵐ Omega) (hT : Ergodic T mu)
    (A : Omega -> E ≃L[Real] E),
      StronglyMeasurable (fun omega => (A omega).toContinuousLinearMap) ->
      Integrable (fun omega => logPlus (norm (A omega).toContinuousLinearMap)) mu ->
      Integrable (fun omega => logPlus (norm (A omega).symm.toContinuousLinearMap)) mu ->
      Nonempty (LyapunovSplitting T A mu)

/-- Checked child-to-root composition. The premise remains the entire open
analytic package and therefore supplies no root proof credit. -/
theorem root_of_oseledetsCorePackage
    (core : OseledetsCorePackage.{u, v}) :
    OseledetsMultiplicativeErgodicTarget.{u, v} := by
  exact core

#print axioms root_of_oseledetsCorePackage

end Stage1Instances.THM_M_1056
