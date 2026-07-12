import ObligationTree

/-!
# THM-M-1027 independent local validation probe

This module deliberately does not import `Proof`.  It reconstructs the
conditional adapter from the frozen external component contract to the exact
Wiener-existence target, giving a second elaboration path for local validation.
-/

noncomputable section

open MeasureTheory ProbabilityTheory
open scoped NNReal

namespace Stage1Instances.THM_M_1027.Validation

universe u

theorem independentlyReconstructedConditionalTarget
    {Omega : Type u} [m : MeasurableSpace Omega] {P : Measure Omega}
    {W : RealProcess Omega}
    (hP : IsProbabilityMeasure P)
    (hmeas : forall t : Time, Measurable (W t))
    (hincrement : forall s t : Time,
      HasLaw (fun omega => W s omega - W t omega)
        (gaussianReal 0 (max (s - t) (t - s))) P)
    (hzero : HasLaw (W 0) (gaussianReal 0 0) P)
    (hindep : HasIndepIncrements W P)
    (hcont : forall omega, Continuous (fun t : Time => W t omega)) :
    WienerExistenceTarget.{u} := by
  apply wienerExistenceTarget_of_witnessPackage
  let package : WienerWitnessPackage.{u} := {
    Omega := Omega
    measurableSpace := m
    P := P
    W := W
    probability := hP
    laws := {
      measurable := hmeas
      startsAtZero := by
        refine (hzero.ae_iff (p := fun x => x = 0) (by fun_prop)).2 ?_
        rw [gaussianReal_zero_var]
        simp
      incrementLaw := by
        intro s t hst
        have hvariance :
            IncrementVariance s t hst = max (t - s) (s - t) := by
          rw [max_eq_left]
          · apply NNReal.eq
            simp [IncrementVariance, NNReal.coe_sub hst]
          · rw [tsub_eq_zero_of_le hst]
            exact zero_le _
        simpa [hvariance] using hincrement t s
      independentIncrements := hindep
      continuousPaths := Filter.Eventually.of_forall hcont
    }
  }
  exact package

#print axioms independentlyReconstructedConditionalTarget

end Stage1Instances.THM_M_1027.Validation
