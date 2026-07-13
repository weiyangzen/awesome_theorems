import «ObligationTree»
import Mathlib.Util.AssertNoSorry
import Mathlib.Util.PrintSorries

/-!
# THM-M-1237 differential validation probe

This module deliberately imports neither `Proof` nor its local counterexample
body. It independently rebuilds the singleton countermodel for the frozen
`ValueEstimateFamily`. The result corroborates a proof-architecture failure;
it is not a counterexample to the exact existential root.
-/

noncomputable section

open MeasureTheory Filter
open scoped ENNReal NNReal Topology

namespace Stage1Rev56.THMM1237.Validation

open Stage1Rev56.THMM1237
open Stage1Rev56.THMM1237.ObligationTree

abbrev ProbeSpace := Space 1

private def oneOnNullDomain : W1pData ({0} : Set ProbeSpace) 2 where
  function := 1
  weakGradient := 0
  functionMemLp := by
    rw [Measure.restrict_singleton']
    simp
  gradientMemLp := MemLp.zero
  isWeakDerivative := by
    intro i phi _hphi
    rw [Measure.restrict_singleton']
    simp [spatialDerivative]

private def zeroExtension : ExtensionData oneOnNullDomain where
  extendedFunction := 0
  extendedGradient := 0
  agreesOnDomain := by
    rw [Measure.restrict_singleton']
    simp
  functionMemLp := MemLp.zero
  gradientMemLp := MemLp.zero
  isWeakDerivative := by
    intro i phi _hphi
    simp [spatialDerivative]
  operatorBound := 0
  normBound := by
    rw [Measure.restrict_singleton']
    simp [oneOnNullDomain]

/-- Independent kernel refutation of the frozen universally quantified value
estimate. The exact root still asks only for one jointly selected representative
and constant and is not refuted by this declaration. -/
theorem independentlyRefutedValueEstimateFamily : ¬ ValueEstimateFamily := by
  intro value
  have impossible := value 1 (by norm_num) ({0} : Set ProbeSpace)
    (measurableSet_singleton 0) Bornology.isBounded_singleton
    2 (1 / 2 : ℝ≥0) (by norm_num) (by norm_num)
    oneOnNullDomain zeroExtension 1 (Eventually.of_forall (fun _ => rfl))
    0 0 (by simp)
  norm_num at impossible

assert_no_sorry independentlyRefutedValueEstimateFamily
#print sorries independentlyRefutedValueEstimateFamily
#print axioms independentlyRefutedValueEstimateFamily

end Stage1Rev56.THMM1237.Validation
