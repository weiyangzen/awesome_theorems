/-!
# THM-M-1061 proof-phase kernel lemmas

These lemmas discharge the direct boundary projections used by both analytic
branches.  They are intentionally stated against the frozen `SatisfiesLDP`
definition, so each body is checked rather than recorded only in prose.

The lower-bound localization, compact-core estimate, and tail estimate are not
supplied by the pinned dependency closure.  The final extended-real
liminf/limsup merge is discharged below, but its two analytic premises remain
open.  Consequently this module is partial proof work and does not close the
root.
-/

namespace Stage1Instances.THM_M_1061.Proof

open Filter MeasureTheory
open Set Topology
open scoped ENNReal

universe u

variable {X : Type u} [MeasurableSpace X] [TopologicalSpace X]
variable {mu : Nat -> Measure X} {a : Nat -> Real} {I : X -> ENNReal}

/-- The probability-measure boundary is a direct consequence of the frozen
full-LDP hypothesis. -/
theorem probabilityMeasure_of_satisfiesLDP
    (h : Stage1Instances.THM_M_1061.SatisfiesLDP mu a I) :
    forall n, IsProbabilityMeasure (mu n) :=
  h.1

/-- Every speed is strictly positive under the frozen full-LDP hypothesis. -/
theorem speed_pos_of_satisfiesLDP
    (h : Stage1Instances.THM_M_1061.SatisfiesLDP mu a I) :
    forall n, 0 < a n :=
  h.2.1

/-- The speed tends to zero under the frozen full-LDP hypothesis. -/
theorem speed_tendsto_zero_of_satisfiesLDP
    (h : Stage1Instances.THM_M_1061.SatisfiesLDP mu a I) :
    Tendsto a atTop (nhds 0) :=
  h.2.2.1

/-- Package the three elementary boundary facts without changing their types. -/
theorem basic_boundaries_of_satisfiesLDP
    (h : Stage1Instances.THM_M_1061.SatisfiesLDP mu a I) :
    (forall n, IsProbabilityMeasure (mu n)) /\
      (forall n, 0 < a n) /\ Tendsto a atTop (nhds 0) :=
  ⟨probabilityMeasure_of_satisfiesLDP h,
    speed_pos_of_satisfiesLDP h,
    speed_tendsto_zero_of_satisfiesLDP h⟩

/-- Project the closed-set upper bound with its exact extended-real type. -/
theorem closed_upper_of_satisfiesLDP
    (h : Stage1Instances.THM_M_1061.SatisfiesLDP mu a I) :
    forall C : Set X, IsClosed C ->
      limsup (fun n => (a n : EReal) * ENNReal.log (mu n C)) atTop <=
        -⨅ x ∈ C, (I x : EReal) :=
  h.2.2.2.1

/-- Project the open-set lower bound with its exact extended-real type. -/
theorem open_lower_of_satisfiesLDP
    (h : Stage1Instances.THM_M_1061.SatisfiesLDP mu a I) :
    forall G : Set X, IsOpen G ->
      -⨅ x ∈ G, (I x : EReal) <=
        liminf (fun n => (a n : EReal) * ENNReal.log (mu n G)) atTop :=
  h.2.2.2.2

omit [MeasurableSpace X] in
/-- Lower semicontinuity is the first half of the frozen good-rate package. -/
theorem lowerSemicontinuous_of_isGoodRateFunction
    (h : Stage1Instances.THM_M_1061.IsGoodRateFunction I) :
    LowerSemicontinuous I :=
  h.1

omit [MeasurableSpace X] in
/-- Finite compact sublevels are the second half of the good-rate package. -/
theorem compact_sublevel_of_isGoodRateFunction
    (h : Stage1Instances.THM_M_1061.IsGoodRateFunction I) :
    forall r : ENNReal, Ne r ∞ -> IsCompact {x | I x <= r} :=
  h.2

omit [TopologicalSpace X] in
/-- A bounded test function gives the expected pointwise upper bound on its
scaled log exponential integral under a probability measure. -/
theorem logExpIntegral_upper_bound
    {m : Measure X} {b B : Real} {F : X -> Real}
    [IsProbabilityMeasure m]
    (hb : 0 < b) (hB : forall x, |F x| <= B) :
    ((b : EReal) * ENNReal.log
      (∫⁻ x, ENNReal.ofReal (Real.exp (F x / b)) ∂m)) <= (B : EReal) := by
  have hlin_le :
      (∫⁻ x, ENNReal.ofReal (Real.exp (F x / b)) ∂m) <=
        ENNReal.ofReal (Real.exp (B / b)) := by
    rw [← mul_one (ENNReal.ofReal (Real.exp (B / b))),
      ← @measure_univ X _ m _, ← lintegral_const]
    apply lintegral_mono
    intro x
    apply ENNReal.ofReal_le_ofReal
    apply Real.exp_monotone
    exact div_le_div_of_nonneg_right
      (le_trans (le_abs_self _) (hB x)) hb.le
  calc
    _ <= (b : EReal) * ENNReal.log
        (ENNReal.ofReal (Real.exp (B / b))) :=
      mul_le_mul_of_nonneg_left (ENNReal.log_monotone hlin_le)
        (EReal.coe_nonneg.2 hb.le)
    _ = (B : EReal) := by
      rw [ENNReal.log_ofReal_of_pos (Real.exp_pos _), Real.log_exp]
      rw [← EReal.coe_mul]
      congr 1
      field_simp

omit [TopologicalSpace X] in
/-- A bounded test function also gives the matching pointwise lower bound on
its scaled log exponential integral. -/
theorem logExpIntegral_lower_bound
    {m : Measure X} {b B : Real} {F : X -> Real}
    [IsProbabilityMeasure m]
    (hb : 0 < b) (hB : forall x, |F x| <= B) :
    ((-B : EReal) <= (b : EReal) * ENNReal.log
      (∫⁻ x, ENNReal.ofReal (Real.exp (F x / b)) ∂m)) := by
  have hlin_ge :
      ENNReal.ofReal (Real.exp (-B / b)) <=
        (∫⁻ x, ENNReal.ofReal (Real.exp (F x / b)) ∂m) := by
    rw [← mul_one (ENNReal.ofReal (Real.exp (-B / b))),
      ← @measure_univ X _ m _, ← lintegral_const]
    apply lintegral_mono
    intro x
    apply ENNReal.ofReal_le_ofReal
    apply Real.exp_monotone
    apply div_le_div_of_nonneg_right _ hb.le
    have hx := neg_le_of_abs_le (hB x)
    linarith
  calc
    (-B : EReal) = ((-B : Real) : EReal) := by rw [EReal.coe_neg]
    _ = (b : EReal) * ENNReal.log
        (ENNReal.ofReal (Real.exp (-B / b))) := by
      rw [ENNReal.log_ofReal_of_pos (Real.exp_pos _), Real.log_exp]
      rw [← EReal.coe_mul]
      congr 1
      field_simp
    _ <= _ := mul_le_mul_of_nonneg_left (ENNReal.log_monotone hlin_ge)
      (EReal.coe_nonneg.2 hb.le)

/-- Specialize both pointwise bounds to every index of the frozen LDP
sequence.  This discharges the pointwise finite-value bounds contributing to
`S-BOUNDARIES`, not that whole node or the open lower/compact-core estimates. -/
theorem logExpIntegral_bounds_of_satisfiesLDP
    (h : Stage1Instances.THM_M_1061.SatisfiesLDP mu a I)
    {F : X -> Real} {B : Real} (hB : forall x, |F x| <= B) :
    forall n,
      (-B : EReal) <= Stage1Instances.THM_M_1061.LogExpIntegral mu a F n ∧
        Stage1Instances.THM_M_1061.LogExpIntegral mu a F n <= (B : EReal) := by
  intro n
  letI : IsProbabilityMeasure (mu n) := probabilityMeasure_of_satisfiesLDP h n
  exact ⟨logExpIntegral_lower_bound (speed_pos_of_satisfiesLDP h n) hB,
    logExpIntegral_upper_bound (speed_pos_of_satisfiesLDP h n) hB⟩

/-- The order-theoretic terminal step of Varadhan's lemma: matching lower and
upper bounds on an `EReal` sequence force convergence.  `EReal` is a complete
linear order, so the boundedness side conditions of mathlib's generic
liminf/limsup convergence theorem are automatic. -/
theorem tendsto_of_variational_liminf_limsup
    {v : Nat -> EReal} {s : EReal}
    (hlower : s <= liminf v atTop)
    (hupper : limsup v atTop <= s) :
    Tendsto v atTop (nhds s) :=
  tendsto_of_le_liminf_of_limsup_le hlower hupper

omit [TopologicalSpace X] in
/-- Exact `M1061-T-LIMIT-MERGE` specialization for the frozen logarithmic
integral and variational value.  This is a real proof body for the terminal
composition step; it deliberately does not manufacture either analytic bound. -/
theorem logExpIntegral_tendsto_of_bounds
    (mu : Nat -> Measure X) (a : Nat -> Real)
    (I : X -> ENNReal) (F : X -> Real)
    (hlower :
      (⨆ x : X, (F x : EReal) - (I x : EReal)) <=
        liminf (Stage1Instances.THM_M_1061.LogExpIntegral mu a F) atTop)
    (hupper :
      limsup (Stage1Instances.THM_M_1061.LogExpIntegral mu a F) atTop <=
        ⨆ x : X, (F x : EReal) - (I x : EReal)) :
    Tendsto (Stage1Instances.THM_M_1061.LogExpIntegral mu a F) atTop
      (nhds (⨆ x : X, (F x : EReal) - (I x : EReal))) :=
  tendsto_of_variational_liminf_limsup hlower hupper

#check probabilityMeasure_of_satisfiesLDP
#check speed_pos_of_satisfiesLDP
#check speed_tendsto_zero_of_satisfiesLDP
#check basic_boundaries_of_satisfiesLDP
#check closed_upper_of_satisfiesLDP
#check open_lower_of_satisfiesLDP
#check lowerSemicontinuous_of_isGoodRateFunction
#check compact_sublevel_of_isGoodRateFunction
#check logExpIntegral_upper_bound
#check logExpIntegral_lower_bound
#check logExpIntegral_bounds_of_satisfiesLDP
#check tendsto_of_variational_liminf_limsup
#check logExpIntegral_tendsto_of_bounds

#print axioms probabilityMeasure_of_satisfiesLDP
#print axioms speed_pos_of_satisfiesLDP
#print axioms speed_tendsto_zero_of_satisfiesLDP
#print axioms basic_boundaries_of_satisfiesLDP
#print axioms closed_upper_of_satisfiesLDP
#print axioms open_lower_of_satisfiesLDP
#print axioms lowerSemicontinuous_of_isGoodRateFunction
#print axioms compact_sublevel_of_isGoodRateFunction
#print axioms logExpIntegral_upper_bound
#print axioms logExpIntegral_lower_bound
#print axioms logExpIntegral_bounds_of_satisfiesLDP
#print axioms tendsto_of_variational_liminf_limsup
#print axioms logExpIntegral_tendsto_of_bounds

end Stage1Instances.THM_M_1061.Proof
