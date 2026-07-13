import Statement

/-!
# THM-M-1029 differential validation probe

This module deliberately does not import `Proof` or `ObligationTree`. It
reconstructs the strict-positive-time to exact-root adapter directly from the
frozen statement. The strict increment law remains an explicit premise.
-/

noncomputable section

open MeasureTheory ProbabilityTheory
open scoped NNReal ProbabilityTheory

namespace Stage1Instances.THM_M_1029.Validation

universe u

/-- A separately expressed strict-positive-time increment premise. -/
def DirectStrictIncrementLaw : Prop :=
  forall (Omega : Type u) [MeasurableSpace Omega]
    (P : Measure Omega) [IsProbabilityMeasure P]
    (F : Filtration Time (inferInstance : MeasurableSpace Omega))
    (X : RealProcess Omega),
      Martingale X F P ->
      Martingale (QuadraticCompensated X) F P ->
      forall {s t : Time}, s < t ->
        Indep (F s)
            (MeasurableSpace.comap
              (fun omega => X t omega - X s omega) (borel Real)) P /\
          HasLaw (fun omega => X t omega - X s omega)
            (gaussianReal 0 (t - s)) P

/-- Direct differential reconstruction of the conditional root adapter. -/
theorem exactRootOfDirectStrictIncrementLaw
    (hstrict : DirectStrictIncrementLaw.{u}) :
    LevyMartingaleCharacterizationTarget.{u} := by
  intro Omega _ P _ F X hcontinuous hzero hmartingale hquadratic
  refine ⟨hcontinuous, hzero, ?_⟩
  intro s t hst
  rcases hst.eq_or_lt with rfl | hlt
  · constructor
    · have hbot : Indep (F s) (⊥ : MeasurableSpace Omega) P :=
        indep_bot_right (μ := P) (F s)
      simpa only [sub_self, MeasurableSpace.comap_const] using hbot
    · constructor
      · simpa only [sub_self] using
          (aemeasurable_const : AEMeasurable (fun _ : Omega => (0 : Real)) P)
      · simp [Measure.map_const]
  · exact hstrict Omega P F X hmartingale hquadratic hlt

#print axioms exactRootOfDirectStrictIncrementLaw

end Stage1Instances.THM_M_1029.Validation
