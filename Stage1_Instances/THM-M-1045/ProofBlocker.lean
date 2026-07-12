import Statement

/-!
# Machine-checked proof-phase blocker for THM-M-1045

The frozen target quantifies over a `paleyWienerIntegral` carrying only a measurability field.
Replacing that field by the constant one function preserves every `WienerData` premise, while the
density branch at the zero direction then asserts that the Radon-Nikodym derivative is the constant
`exp 1`.  Its integral cannot be one under a probability measure.  Thus the target would make
`WienerData` empty rather than prove the Cameron-Martin theorem.
-/

noncomputable section

open MeasureTheory ProbabilityTheory
open scoped ENNReal NNReal

namespace Stage1Instances.THM_M_1045

/-- Change only the unconstrained statement-level Paley-Wiener field to the constant one map. -/
def constantOnePairing (W : WienerData) : WienerData where
  measure := W.measure
  isProbability := W.isProbability
  startsAtZero := W.startsAtZero
  coordinateAEMeasurable := W.coordinateAEMeasurable
  finiteDimensionalGaussian := W.finiteDimensionalGaussian
  incrementLaw := W.incrementLaw
  paleyWienerIntegral := fun _ _ => 1
  paleyWienerMeasurable := fun _ => measurable_const

/-- The frozen root implies an impossible density identity for every inhabitant of `WienerData`. -/
theorem target_forces_bad_zero_density (target : CameronMartinTarget) (W : WienerData) :
    (translatedMeasure W.measure (0 : WienerPath)).rnDeriv W.measure =ᵐ[W.measure]
      fun _ => ENNReal.ofReal (Real.exp 1) := by
  have densityBranch := (target (constantOnePairing W) (0 : WienerPath)).2.1
  have result := densityBranch (0 : NNReal -> Real) (by simp) (by simp)
  convert result using 1
  funext x
  simp [density, constantOnePairing, cameronMartinEnergy]

end Stage1Instances.THM_M_1045
