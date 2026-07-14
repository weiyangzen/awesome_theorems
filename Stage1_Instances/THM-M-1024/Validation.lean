import Statement

/-!
# THM-M-1024 differential validation probes

This module deliberately does not import `Proof` or `ObligationTree`. It
independently reconstructs selected exponent-normalization subresults and the
conditional package-to-root composition from the frozen statement. The
forward, converse, and uniqueness packages remain explicit premises, so this
module is not a proof of the Levy-Khintchine representation theorem.
-/

noncomputable section

open Filter MeasureTheory Set TopologicalSpace
open scoped ENNReal Topology

namespace Stage1Instances.THM_M_1024.Validation

open Stage1Instances.THM_M_1024

/-- A separately defined copy of the frozen compensated jump integrand. -/
noncomputable def directCompensatedIntegrand {d : Nat}
    (u x : Space d) : Complex :=
  Complex.exp (Complex.I * ((@inner Real _ _ u x : Real) : Complex)) - 1
    - Complex.I * ((@inner Real _ _ u x : Real) : Complex) *
      if ‖x‖ ≤ 1 then 1 else 0

@[simp]
theorem directCompensatedIntegrand_zero_left {d : Nat} (x : Space d) :
    directCompensatedIntegrand 0 x = 0 := by
  simp [directCompensatedIntegrand]

/-- Independent check of the normalization of the frozen exponent at zero. -/
theorem directLevyExponent_zero {d : Nat} (data : LevyTriplet d) :
    levyExponent data 0 = 0 := by
  simp [levyExponent]

/-- Independent measurability check for the copied compensated integrand. -/
theorem directMeasurableCompensatedIntegrand {d : Nat} (u : Space d) :
    Measurable (directCompensatedIntegrand u) := by
  unfold directCompensatedIntegrand
  apply Measurable.sub
  · exact (((measurable_const.mul (by fun_prop)).cexp).sub measurable_const)
  · exact (measurable_const.mul (by fun_prop)).mul
      (measurable_const.ite
        (isClosed_le continuous_norm continuous_const).measurableSet
        measurable_const)

/-- Direct reconstruction of the conditional root adapter. None of the three
mathematical packages is supplied by this validation module. -/
theorem directConditionalRoot
    (forward : forall (d : Nat) (mu : Measure (Space d)),
      InfinitelyDivisible mu -> exists data : LevyTriplet d, Represents mu data)
    (converse : forall (d : Nat) (mu : Measure (Space d)),
      (exists data : LevyTriplet d, Represents mu data) -> InfinitelyDivisible mu)
    (unique : forall (d : Nat) (mu : Measure (Space d)) (a b : LevyTriplet d),
      Represents mu a -> Represents mu b -> a = b) :
    LevyKhintchineTarget := by
  intro d mu
  constructor
  · intro hdiv
    obtain ⟨data, hdata⟩ := forward d mu hdiv
    exact ⟨data, hdata, fun other hother => unique d mu other data hother hdata⟩
  · rintro ⟨data, hdata, _⟩
    exact converse d mu ⟨data, hdata⟩

#print axioms directCompensatedIntegrand_zero_left
#print axioms directLevyExponent_zero
#print axioms directMeasurableCompensatedIntegrand
#print axioms directConditionalRoot

end Stage1Instances.THM_M_1024.Validation
