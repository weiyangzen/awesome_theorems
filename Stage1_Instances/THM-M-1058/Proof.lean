import Statement

/-!
# THM-M-1058 proof-phase refutation

The frozen target is a property of supplied data. The proof task cannot close
that open expression without selecting data or quantifying over them. This
module gives an admissible one-point record that does not satisfy the property,
so the possible universal completion is false. A specialized instance would
instead change the frozen target.
-/

noncomputable section

open MeasureTheory Filter
open scoped ENNReal Topology

namespace Stage1Instances.THM_M_1058

/-- The probability measure may be arbitrary on the one-point space, while the
constant positive rate makes the closed-universe upper bound false. -/
def counterexampleData : LargeDeviationData PUnit where
  measures := fun _ => default
  speed := fun n => (n : Real) + 1
  speed_pos := by
    intro n
    positivity
  speed_tendsto_atTop := by
    exact tendsto_atTop_add_const_right atTop 1 tendsto_natCast_atTop_atTop
  rate := fun _ => 1
  rate_nonnegative := by
    intro x
    positivity
  rate_lowerSemicontinuous := lowerSemicontinuous_const

/-- The frozen data hypotheses do not imply an LDP: on \`Set.univ\`, the scaled
log probability is zero but the negated rate infimum is negative one. -/
theorem not_largeDeviationPrinciple_counterexample :
    Not (LargeDeviationPrinciple PUnit counterexampleData) := by
  intro h
  have hu := h.1 Set.univ isClosed_univ
  simp [scaledLogProbability, rateInf, counterexampleData] at hu
  have hzero_lt_one : (0 : EReal) < 1 := by norm_num
  exact (not_le_of_gt hzero_lt_one) hu

/-- In particular, the frozen data interface cannot support a proof that every
supplied data record satisfies the LDP predicate. -/
theorem not_all_largeDeviationPrinciple :
    Not (forall D : LargeDeviationData PUnit,
      LargeDeviationPrinciple PUnit D) := by
  intro h
  exact not_largeDeviationPrinciple_counterexample (h counterexampleData)

#check not_largeDeviationPrinciple_counterexample
#check not_all_largeDeviationPrinciple
#print axioms not_largeDeviationPrinciple_counterexample
#print axioms not_all_largeDeviationPrinciple

end Stage1Instances.THM_M_1058
