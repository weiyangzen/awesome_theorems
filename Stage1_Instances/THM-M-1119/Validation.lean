import Statement
import Mathlib.MeasureTheory.Constructions.SimpleGraph
import Mathlib.MeasureTheory.Measure.Dirac
import Mathlib.Util.AssertNoSorry
import Mathlib.Util.PrintSorries

/-!
# THM-M-1119 differential validation probes

This module deliberately imports neither `ObligationTree` nor `Proof`. It
independently reconstructs two elementary proof-phase ingredients from the
frozen statement. It does not prove either one-half threshold inequality or
the exact Kesten root.
-/

namespace Stage1Instances.THM_M_1119.Validation

open MeasureTheory
open Stage1Instances.THM_M_1119

/-- Validation-local coordinatewise inclusion of open bonds. -/
def ConfigurationLE (configuration configuration' : Configuration) : Prop :=
  forall edge, configuration edge = true -> configuration' edge = true

/-- No-proof-import reconstruction that opening bonds enlarges the open graph. -/
theorem differentialOpenGraphMono {configuration configuration' : Configuration}
    (h : ConfigurationLE configuration configuration') :
    openGraph configuration <= openGraph configuration' := by
  intro v w adjacent
  rw [openGraph, SimpleGraph.fromEdgeSet_adj] at adjacent ⊢
  exact ⟨⟨adjacent.1.1, h ⟨s(v, w), adjacent.1.1⟩ adjacent.1.2⟩,
    adjacent.2⟩

private theorem differentialBernoulliZeroEqPureFalse :
    PMF.bernoulli (0 : NNReal) (by norm_num) = PMF.pure false := by
  ext state
  cases state <;> simp [PMF.pure_apply]

/-- No-proof-import reconstruction of the closed endpoint product measure. -/
theorem differentialBondMeasureZeroEqDirac :
    bondMeasure (0 : NNReal) (by norm_num) = Measure.dirac (fun _ => false) := by
  rw [bondMeasure]
  have coordinates :
      (fun _ : Bond => (PMF.bernoulli (0 : NNReal) (by norm_num)).toMeasure) =
        (fun _ : Bond => Measure.dirac false) := by
    funext _
    rw [differentialBernoulliZeroEqPureFalse]
    exact PMF.toMeasure_pure false
  rw [coordinates, Measure.infinitePi_dirac]

assert_no_sorry differentialOpenGraphMono
assert_no_sorry differentialBondMeasureZeroEqDirac

#print sorries differentialOpenGraphMono
#print sorries differentialBondMeasureZeroEqDirac
#print axioms differentialOpenGraphMono
#print axioms differentialBondMeasureZeroEqDirac

end Stage1Instances.THM_M_1119.Validation
