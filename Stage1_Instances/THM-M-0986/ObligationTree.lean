import Statement

/-!
# THM-M-0986 conditional obligation composition

This module checks the final semantic composition chosen by the frozen tree.
The strong-law and measurability packages remain explicit inputs, so this is
not a proof of Khinchin's weak law.
-/

noncomputable section

open Filter Finset MeasureTheory
open scoped BigOperators MeasureTheory ProbabilityTheory Topology Function

namespace Stage1Instances.THM_M_0986

universe u

/-- The stronger almost-everywhere convergence package required by the chosen
mathlib-backed route. -/
def StrongLawPackage : Prop :=
  forall (Omega : Type u) [MeasurableSpace Omega]
    (mu : Measure Omega) [IsProbabilityMeasure mu]
    (X : Nat -> Omega -> Real),
      Integrable (X 0) mu ->
      Pairwise ((fun f g => ProbabilityTheory.IndepFun f g mu) on X) ->
      (forall i, ProbabilityTheory.IdentDistrib (X i) (X 0) mu mu) ->
      ∀ᵐ omega ∂mu,
        Tendsto (fun n => empiricalAverage X n omega) atTop (nhds mu[X 0])

/-- Measurability of every empirical average, kept separate because the
almost-everywhere-to-in-measure bridge requires it. -/
def AverageMeasurabilityPackage : Prop :=
  forall (Omega : Type u) [MeasurableSpace Omega]
    (mu : Measure Omega) (X : Nat -> Omega -> Real),
      (forall i, AEStronglyMeasurable (X i) mu) ->
      forall n, AEStronglyMeasurable (empiricalAverage X n) mu

/-- Checked composition from the two substantive packages into the exact
canonical target. -/
theorem root_of_strongLaw_packages
    (strongLaw : StrongLawPackage.{u})
    (averageMeasurable : AverageMeasurabilityPackage.{u}) :
    KhinchinWeakLawTarget.{u} := by
  intro Omega _ mu _ X hint hindep hident
  have hmeas : forall i, AEStronglyMeasurable (X i) mu := fun i =>
    (hident i).aestronglyMeasurable_iff.2 hint.1
  exact tendstoInMeasure_of_tendsto_ae (averageMeasurable Omega mu X hmeas)
    (strongLaw Omega mu X hint hindep hident)

#print axioms root_of_strongLaw_packages

end Stage1Instances.THM_M_0986
