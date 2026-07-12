import ObligationTree

/-!
# THM-M-1027 proof-phase bridge bodies

This module implements the normalization and assembly needed to turn the
component theorems of the pinned external Brownian construction into the
frozen Wiener witness.  The external construction itself remains an explicit
premise until its package is available in the repository's Lake closure.
-/

noncomputable section

open MeasureTheory ProbabilityTheory
open scoped NNReal

namespace Stage1Instances.THM_M_1027

universe u

/-- For ordered times, the frozen real-difference variance is NNReal subtraction. -/
theorem incrementVariance_eq_tsub {s t : Time} (hst : s <= t) :
    IncrementVariance s t hst = t - s := by
  apply NNReal.eq
  simp [IncrementVariance, NNReal.coe_sub hst]

/-- Normalize the symmetric variance used by the external subtraction theorem. -/
theorem incrementVariance_eq_max_tsub {s t : Time} (hst : s <= t) :
    IncrementVariance s t hst = max (t - s) (s - t) := by
  rw [max_eq_left]
  · exact incrementVariance_eq_tsub hst
  · rw [tsub_eq_zero_of_le hst]
    exact zero_le _

/-- A real random variable with centered zero-variance Gaussian law is zero a.e. -/
theorem hasLaw_gaussianReal_zero_ae_eq_zero
    {Omega : Type u} [MeasurableSpace Omega] {P : Measure Omega} {X : Omega -> Real}
    (hX : HasLaw X (gaussianReal 0 0) P) :
    Filter.Eventually (fun omega => X omega = 0) (ae P) := by
  refine (hX.ae_iff (p := fun x => x = 0) (by fun_prop)).2 ?_
  rw [gaussianReal_zero_var]
  simp

/--
Checked adapter from the external Brownian component API to the exact frozen
witness package.  Its subtraction arguments and variance are normalized here,
and the zero-start law is derived rather than assumed.
-/
def WienerWitnessPackage.ofExternalBrownianComponents
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
    WienerWitnessPackage.{u} where
  Omega := Omega
  measurableSpace := m
  P := P
  W := W
  probability := hP
  laws := {
    measurable := hmeas
    startsAtZero := hasLaw_gaussianReal_zero_ae_eq_zero hzero
    incrementLaw := by
      intro s t hst
      simpa [incrementVariance_eq_max_tsub hst] using hincrement t s
    independentIncrements := hindep
    continuousPaths := Filter.Eventually.of_forall hcont
  }

/-- Conditional root closure with only the unavailable external components exposed. -/
theorem wienerExistenceTarget_of_externalBrownianComponents
    {Omega : Type u} [MeasurableSpace Omega] {P : Measure Omega}
    {W : RealProcess Omega}
    (hP : IsProbabilityMeasure P)
    (hmeas : forall t : Time, Measurable (W t))
    (hincrement : forall s t : Time,
      HasLaw (fun omega => W s omega - W t omega)
        (gaussianReal 0 (max (s - t) (t - s))) P)
    (hzero : HasLaw (W 0) (gaussianReal 0 0) P)
    (hindep : HasIndepIncrements W P)
    (hcont : forall omega, Continuous (fun t : Time => W t omega)) :
    WienerExistenceTarget.{u} :=
  wienerExistenceTarget_of_witnessPackage
    (WienerWitnessPackage.ofExternalBrownianComponents
      hP hmeas hincrement hzero hindep hcont)

#print axioms incrementVariance_eq_tsub
#print axioms incrementVariance_eq_max_tsub
#print axioms hasLaw_gaussianReal_zero_ae_eq_zero
#print axioms WienerWitnessPackage.ofExternalBrownianComponents
#print axioms wienerExistenceTarget_of_externalBrownianComponents

end Stage1Instances.THM_M_1027
