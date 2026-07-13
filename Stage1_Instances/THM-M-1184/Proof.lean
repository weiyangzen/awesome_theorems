import ObligationTree
import Mathlib.MeasureTheory.Measure.Prod

/-!
# THM-M-1184 proof-phase bodies

This module closes the product-coupling construction and the complete
weak-duality branch for the frozen signed-real interface. The reverse-duality
package remains an explicit premise of the final composition theorem below.
-/

noncomputable section

open MeasureTheory Set

namespace Stage1Instances.THM_M_1184

universe u v

variable {X : Type u} {Y : Type v}
  [MetricSpace X] [MeasurableSpace X] [BorelSpace X] [CompactSpace X]
  [MetricSpace Y] [MeasurableSpace Y] [BorelSpace Y] [CompactSpace Y]

/-- The independent product probability measure is a coupling of its factors. -/
def productCoupling (mu : ProbabilityMeasure X) (nu : ProbabilityMeasure Y) :
    Coupling mu nu where
  plan := ⟨(mu : Measure X).prod (nu : Measure Y), by infer_instance⟩
  fst_marginal := by simp
  snd_marginal := by simp

/-- The first marginal identity transports integrals of continuous functions. -/
theorem integral_fst_of_coupling {mu : ProbabilityMeasure X} {nu : ProbabilityMeasure Y}
    (gamma : Coupling mu nu) {f : X -> Real} (hf : Continuous f) :
    (∫ z, f z.1 ∂(gamma.plan : Measure (X × Y))) =
      ∫ x, f x ∂(mu : Measure X) := by
  rw [← gamma.fst_marginal]
  exact (integral_map measurable_fst.aemeasurable hf.aestronglyMeasurable).symm

/-- The second marginal identity transports integrals of continuous functions. -/
theorem integral_snd_of_coupling {mu : ProbabilityMeasure X} {nu : ProbabilityMeasure Y}
    (gamma : Coupling mu nu) {f : Y -> Real} (hf : Continuous f) :
    (∫ z, f z.2 ∂(gamma.plan : Measure (X × Y))) =
      ∫ y, f y ∂(nu : Measure Y) := by
  rw [← gamma.snd_marginal]
  exact (integral_map measurable_snd.aemeasurable hf.aestronglyMeasurable).symm

/-- A feasible potential pair is bounded above by every coupling cost. -/
theorem dualValue_le_primalValue {mu : ProbabilityMeasure X} {nu : ProbabilityMeasure Y}
    {c : X × Y -> Real} (hc : Continuous c) (p : DualPair c) (gamma : Coupling mu nu) :
    DualValue mu nu c p <= PrimalValue c gamma := by
  rw [DualValue, PrimalValue, ← integral_fst_of_coupling gamma p.phi_continuous,
    ← integral_snd_of_coupling gamma p.psi_continuous, ← integral_add]
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

/-- Continuous costs have a constant feasible pair on the nonempty compact product. -/
theorem constantDualPair_nonempty (mu : ProbabilityMeasure X) (nu : ProbabilityMeasure Y)
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

/-- Both objective ranges are nonempty and bounded in the directions used by `sInf`/`sSup`. -/
theorem objectiveRanges_wellFounded (mu : ProbabilityMeasure X) (nu : ProbabilityMeasure Y)
    {c : X × Y -> Real} (hc : Continuous c) :
    (range (PrimalValue (mu := mu) (nu := nu) c)).Nonempty ∧
      (range (DualValue mu nu c)).Nonempty ∧
      BddBelow (range (PrimalValue (mu := mu) (nu := nu) c)) ∧
      BddAbove (range (DualValue mu nu c)) := by
  let gamma := productCoupling mu nu
  let p := Classical.choice (constantDualPair_nonempty mu nu hc)
  refine ⟨⟨PrimalValue c gamma, mem_range_self gamma⟩,
    ⟨DualValue mu nu c p, mem_range_self p⟩, ?_, ?_⟩
  · exact ⟨DualValue mu nu c p, by
      rintro value ⟨gamma', rfl⟩
      exact dualValue_le_primalValue hc p gamma'⟩
  · exact ⟨PrimalValue c gamma, by
      rintro value ⟨p', rfl⟩
      exact dualValue_le_primalValue hc p' gamma⟩

/-- The exact weak-duality package for the frozen target. -/
theorem weakDuality : WeakDualityPackage.{u, v} := by
  intro X Y _ _ _ _ _ _ _ _ mu nu c hc
  obtain ⟨primal_nonempty, dual_nonempty, _, _⟩ := objectiveRanges_wellFounded mu nu hc
  apply csSup_le
  · exact dual_nonempty
  · rintro value ⟨p, rfl⟩
    apply le_csInf
    · exact primal_nonempty
    · rintro value ⟨gamma, rfl⟩
      exact dualValue_le_primalValue hc p gamma

/-- Root composition with only the strong-duality package left explicit. -/
theorem kantorovichDuality_of_reverse
    (reverse : ReverseDualityPackage.{u, v}) :
    KantorovichDualityTarget.{u, v} :=
  root_of_duality_packages weakDuality reverse

#print axioms productCoupling
#print axioms integral_fst_of_coupling
#print axioms integral_snd_of_coupling
#print axioms dualValue_le_primalValue
#print axioms constantDualPair_nonempty
#print axioms objectiveRanges_wellFounded
#print axioms weakDuality
#print axioms kantorovichDuality_of_reverse

end Stage1Instances.THM_M_1184
