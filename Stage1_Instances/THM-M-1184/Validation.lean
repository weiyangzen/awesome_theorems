import Statement
import Mathlib.MeasureTheory.Measure.Prod
import Mathlib.Util.AssertNoSorry
import Mathlib.Util.PrintSorries

/-!
# THM-M-1184 same-worker differential validation

This module deliberately imports neither `Proof` nor `ObligationTree`. It
independently reconstructs the frozen weak-duality package from the statement
definitions. The reverse inequality and the exact root remain open.
-/

noncomputable section

open MeasureTheory Set

namespace Stage1Instances.THM_M_1184.Validation

universe u v

variable {X : Type u} {Y : Type v}
  [MetricSpace X] [MeasurableSpace X] [BorelSpace X] [CompactSpace X]
  [MetricSpace Y] [MeasurableSpace Y] [BorelSpace Y] [CompactSpace Y]

/-- Independent product-plan construction used only by this validation probe. -/
private def validationProductCoupling
    (mu : ProbabilityMeasure X) (nu : ProbabilityMeasure Y) :
    Coupling mu nu where
  plan := ⟨(mu : Measure X).prod (nu : Measure Y), by infer_instance⟩
  fst_marginal := by simp
  snd_marginal := by simp

omit [BorelSpace X] [BorelSpace Y] in
/-- A constant feasible pair, independently reconstructed for the range witness. -/
private theorem validationDualPairNonempty
    (mu : ProbabilityMeasure X) (nu : ProbabilityMeasure Y)
    {c : X × Y -> Real} (hc : Continuous c) : Nonempty (DualPair c) := by
  have hXY : Nonempty (X × Y) := Nonempty.map2 Prod.mk mu.nonempty nu.nonempty
  obtain ⟨z0⟩ := hXY
  obtain ⟨zmin, _, hzmin⟩ := isCompact_univ.exists_isMinOn
    (show Set.univ.Nonempty from ⟨z0, mem_univ _⟩) hc.continuousOn
  exact ⟨
    { phi := fun _ => c zmin
      psi := fun _ => 0
      phi_continuous := continuous_const
      psi_continuous := continuous_const
      feasible := fun x y => by simpa using hzmin (mem_univ (x, y)) }⟩

/-- A validation-only reconstruction of the fixed-plan dual inequality. -/
private theorem validationDualLePrimal
    {mu : ProbabilityMeasure X} {nu : ProbabilityMeasure Y}
    {c : X × Y -> Real} (hc : Continuous c) (p : DualPair c)
    (gamma : Coupling mu nu) :
    DualValue mu nu c p <= PrimalValue c gamma := by
  rw [DualValue, PrimalValue]
  rw [← gamma.fst_marginal,
    integral_map measurable_fst.aemeasurable p.phi_continuous.aestronglyMeasurable]
  rw [← gamma.snd_marginal,
    integral_map measurable_snd.aemeasurable p.psi_continuous.aestronglyMeasurable,
    ← integral_add]
  · exact integral_mono_ae
      ((p.phi_continuous.comp continuous_fst).add
        (p.psi_continuous.comp continuous_snd) |>.integrable_of_hasCompactSupport
          (HasCompactSupport.of_compactSpace _))
      (hc.integrable_of_hasCompactSupport (HasCompactSupport.of_compactSpace c))
      (Filter.Eventually.of_forall fun z : X × Y => p.feasible z.1 z.2)
  · exact (p.phi_continuous.comp continuous_fst).integrable_of_hasCompactSupport
      (HasCompactSupport.of_compactSpace _)
  · exact (p.psi_continuous.comp continuous_snd).integrable_of_hasCompactSupport
      (HasCompactSupport.of_compactSpace _)

/-- Same-worker differential reconstruction of the complete weak inequality. -/
theorem differentialWeakDuality :
    forall (X : Type u) (Y : Type v)
      [MetricSpace X] [MeasurableSpace X] [BorelSpace X] [CompactSpace X]
      [MetricSpace Y] [MeasurableSpace Y] [BorelSpace Y] [CompactSpace Y]
      (mu : ProbabilityMeasure X) (nu : ProbabilityMeasure Y)
      (c : X × Y -> Real), Continuous c ->
        sSup (range (DualValue mu nu c)) <=
          sInf (range (PrimalValue (mu := mu) (nu := nu) c)) := by
  intro X Y _ _ _ _ _ _ _ _ mu nu c hc
  let gamma := validationProductCoupling mu nu
  apply csSup_le
  · obtain ⟨p⟩ := validationDualPairNonempty mu nu hc
    exact ⟨DualValue mu nu c p, mem_range_self p⟩
  · rintro value ⟨p, rfl⟩
    apply le_csInf
    · exact ⟨PrimalValue c gamma, mem_range_self gamma⟩
    · rintro value ⟨gamma', rfl⟩
      exact validationDualLePrimal hc p gamma'

assert_no_sorry differentialWeakDuality
#print sorries differentialWeakDuality
#print axioms differentialWeakDuality

end Stage1Instances.THM_M_1184.Validation
