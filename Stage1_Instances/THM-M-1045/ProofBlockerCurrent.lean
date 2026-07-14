import Statement

/-!
# THM-M-1045 current-base proof obstruction

The frozen target treats the Paley-Wiener pairing as arbitrary measurable data.  Replacing that
field by the constant-one map preserves all Wiener-law fields, but the zero-direction density
branch then contradicts the Radon-Nikodym derivative of a probability measure with itself.
-/

noncomputable section

open MeasureTheory ProbabilityTheory
open scoped ENNReal NNReal

namespace Stage1Instances.THM_M_1045

/-- Preserve every Wiener-law premise while replacing the unconstrained pairing by a constant. -/
def currentConstantOnePairing (W : WienerData) : WienerData where
  measure := W.measure
  isProbability := W.isProbability
  startsAtZero := W.startsAtZero
  coordinateAEMeasurable := W.coordinateAEMeasurable
  finiteDimensionalGaussian := W.finiteDimensionalGaussian
  incrementLaw := W.incrementLaw
  paleyWienerIntegral := fun _ _ => 1
  paleyWienerMeasurable := fun _ => measurable_const

/-- Translation by the zero path leaves the frozen path measure unchanged. -/
theorem translatedMeasure_zero (W : WienerData) :
    translatedMeasure W.measure (0 : WienerPath) = W.measure := by
  calc
    translatedMeasure W.measure 0 = W.measure.map id := by
      rw [translatedMeasure]
      exact Measure.map_congr (by filter_upwards with x; simp [translate])
    _ = W.measure := Measure.map_id

/-- Every advertised Wiener datum refutes the exact frozen root. -/
theorem no_target_of_wienerData (W : WienerData) : ¬ CameronMartinTarget := by
  letI : IsProbabilityMeasure W.measure := W.isProbability
  intro target
  have badDensity :=
    (target (currentConstantOnePairing W) (0 : WienerPath)).2.1
      (0 : NNReal -> Real) (by simp) (by simp)
  have hself : W.measure.rnDeriv W.measure =ᵐ[W.measure] fun _ => (1 : ENNReal) :=
    Measure.rnDeriv_self W.measure
  have hbad : W.measure.rnDeriv W.measure =ᵐ[W.measure]
      fun _ => ENNReal.ofReal (Real.exp 1) := by
    rw [translatedMeasure_zero] at badDensity
    convert badDensity using 1
    funext x
    simp [density, currentConstantOnePairing, cameronMartinEnergy]
  obtain ⟨x, hx⟩ := (hself.symm.trans hbad).exists
  have hgt : (1 : ENNReal) < ENNReal.ofReal (Real.exp 1) := by
    simpa only [ENNReal.one_lt_ofReal] using (Real.one_lt_exp_iff.mpr zero_lt_one)
  exact hgt.ne hx

#print axioms no_target_of_wienerData

end Stage1Instances.THM_M_1045
