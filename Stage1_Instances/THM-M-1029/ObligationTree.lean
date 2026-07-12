import Statement

/-!
# THM-M-1029 conditional obligation composition

This module checks the final composition boundary. The increment-law package
remains an explicit premise; no Levy characterization proof is asserted.
-/

noncomputable section

open MeasureTheory ProbabilityTheory
open scoped NNReal ProbabilityTheory

namespace Stage1Instances.THM_M_1029

universe u

/-- The output required from the quadratic-variation and exponential-martingale route. -/
def IncrementLawPackage : Prop :=
  forall (Omega : Type u) [MeasurableSpace Omega]
    (P : Measure Omega) [IsProbabilityMeasure P]
    (F : Filtration Time (inferInstance : MeasurableSpace Omega))
    (X : RealProcess Omega),
      Martingale X F P ->
      Martingale (QuadraticCompensated X) F P ->
      forall {s t : Time}, s <= t ->
        Indep (F s)
            (MeasurableSpace.comap (fun omega => X t omega - X s omega) (borel Real)) P /\
          HasLaw (fun omega => X t omega - X s omega)
            (gaussianReal 0 (t - s)) P

/-- Checked composition of the analytic increment package into the exact root. -/
theorem root_of_incrementLawPackage
    (incrementLaws : IncrementLawPackage.{u}) :
    LevyMartingaleCharacterizationTarget.{u} := by
  intro Omega _ P _ F X hcontinuous hzero hmartingale hquadratic
  refine ⟨hcontinuous, hzero, ?_⟩
  intro s t hst
  exact incrementLaws Omega P F X hmartingale hquadratic hst

#print axioms root_of_incrementLawPackage

end Stage1Instances.THM_M_1029
