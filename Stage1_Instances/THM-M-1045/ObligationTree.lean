import Statement

/-!
# THM-M-1045 conditional obligation composition

The three mathematical branches remain explicit premises.  This file checks only that their
exact conclusions compose to the frozen Cameron-Martin target.
-/

noncomputable section

open MeasureTheory

namespace Stage1Instances.THM_M_1045

def EquivalenceBranch : Prop :=
  forall (W : WienerData) (h : WienerPath),
    Equivalent (translatedMeasure W.measure h) W.measure <-> IsCameronMartinDirection h

def DensityBranch : Prop :=
  forall (W : WienerData) (h : WienerPath) (g : NNReal -> Real),
    MemLp g 2 timeMeasure ->
    (forall t : NNReal, h t = ∫ s in Set.Ioc 0 t, g s ∂timeMeasure) ->
    (translatedMeasure W.measure h).rnDeriv W.measure =ᵐ[W.measure] density W g

def SingularityBranch : Prop :=
  forall (W : WienerData) (h : WienerPath),
    Not (IsCameronMartinDirection h) ->
    Measure.MutuallySingular (translatedMeasure W.measure h) W.measure

/-- Exact conditional composition; none of the three branch packages is asserted here. -/
theorem root_of_branch_packages
    (equivalence : EquivalenceBranch)
    (densityFormula : DensityBranch)
    (singularity : SingularityBranch) : CameronMartinTarget := by
  intro W h
  exact ⟨equivalence W h, densityFormula W h, singularity W h⟩

#print axioms root_of_branch_packages

end Stage1Instances.THM_M_1045
