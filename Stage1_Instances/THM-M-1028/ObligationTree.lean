import Statement

/-!
# THM-M-1028 conditional obligation composition

This module checks only the final composition selected by the frozen
architecture. The continuous-modification and nowhere-differentiability
packages remain explicit premises.
-/

noncomputable section

open MeasureTheory ProbabilityTheory Set Filter

namespace AwesomeTheorems.Stage1.THM_M_1028

universe u

/-- The construction package: produce a continuous coordinatewise modification. -/
def ContinuousModificationPackage : Prop :=
  forall (Omega : Type u) [MeasurableSpace Omega] (P : Measure Omega)
      [IsProbabilityMeasure P] (X : RealProcess Omega),
    (∀ᵐ omega ∂P, X 0 omega = 0) -> HasStandardWienerIncrements X P ->
    exists Y : RealProcess Omega, IsModification X Y P /\
      ∀ᵐ omega ∂P, ContinuousOn (fun t => Y t omega) (Ici (0 : Real))

/-- The analytic package: every continuous Wiener modification is a.e. nowhere differentiable. -/
def NowhereDifferentiabilityPackage : Prop :=
  forall (Omega : Type u) [MeasurableSpace Omega] (P : Measure Omega)
      [IsProbabilityMeasure P] (X Y : RealProcess Omega),
    (∀ᵐ omega ∂P, X 0 omega = 0) -> HasStandardWienerIncrements X P ->
    IsModification X Y P ->
    (∀ᵐ omega ∂P, ContinuousOn (fun t => Y t omega) (Ici (0 : Real))) ->
    ∀ᵐ omega ∂P, NowhereDifferentiableOnNonnegative (fun t => Y t omega)

/-- Checked merge into the exact canonical root, conditional on the two open packages. -/
theorem root_of_path_packages
    (continuous : ContinuousModificationPackage.{u})
    (nowhereDiff : NowhereDifferentiabilityPackage.{u}) :
    Statement.{u} := by
  intro Omega _ P _ X hzero hincrements
  obtain ⟨Y, hmod, hcontinuous⟩ :=
    continuous Omega P X hzero hincrements
  refine ⟨Y, hmod, ?_⟩
  have hnondiff := nowhereDiff Omega P X Y hzero hincrements hmod hcontinuous
  filter_upwards [hcontinuous, hnondiff] with omega hc hn
  exact ⟨hc, hn⟩

#print AwesomeTheorems.Stage1.THM_M_1028.root_of_path_packages
#print axioms AwesomeTheorems.Stage1.THM_M_1028.root_of_path_packages

end AwesomeTheorems.Stage1.THM_M_1028
