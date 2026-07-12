import Mathlib.Analysis.Calculus.ContDiff.Basic
import Mathlib.Analysis.InnerProductSpace.PiL2

/-!
# THM-M-1133 conditional obligation composition

This file is elaborated together with `Statement.lean` by the scoped validator.
It checks the bridge from the more general subsolution package to the exact
caloric root. The subsolution maximum principle remains an explicit premise.
-/

noncomputable section

open Set

namespace Stage1Instances.THM_M_1133

/-- Classical spatial/time regularity together with the forward heat
subsolution inequality. -/
def IsClassicalSubcaloricOn {n : Nat} (U : Set (Space n)) (T : Real)
    (u : Space n → Real → Real) : Prop :=
  (∀ x ∈ U, ∀ t ∈ Ioc 0 T,
      ContDiffAt Real 2 (fun y => u y t) x ∧
      ContDiffAt Real 1 (fun s => u x s) t) ∧
    ∀ x ∈ U, ∀ t ∈ Ioc 0 T,
      deriv (fun s => u x s) t - spatialLaplacian u x t ≤ 0

/-- The central analytic package exposed by the frozen architecture. -/
def WeakSubsolutionMaximumPrinciple : Prop :=
  ∀ (n : Nat) (U : Set (Space n)) (T : Real) (u : Space n → Real → Real),
    U.Nonempty → IsOpen U → Bornology.IsBounded U → 0 < T →
    ContinuousOn (fun p : Space n × Real => u p.1 p.2) (ClosedCylinder U T) →
    IsClassicalSubcaloricOn U T u →
    ∃ p ∈ ParabolicBoundary U T,
      ∀ q ∈ ClosedCylinder U T, u q.1 q.2 ≤ u p.1 p.2

/-- A caloric function is a subsolution for the same forward sign convention. -/
theorem caloric_isSubcaloric {n : Nat} {U : Set (Space n)} {T : Real}
    {u : Space n → Real → Real} (h : IsClassicalCaloricOn U T u) :
    IsClassicalSubcaloricOn U T u := by
  refine ⟨h.1, ?_⟩
  intro x hx t ht
  exact le_of_eq (h.2 x hx t ht)

/-- Checked composition of the central subsolution package into the exact
intake-selected equality-form root. -/
theorem root_of_subsolutionMaximumPrinciple
    (subsolutionMaximum : WeakSubsolutionMaximumPrinciple) :
    HeatEquationWeakMaximumPrinciple := by
  intro n U T u hU hOpen hBounded hT hContinuous hCaloric
  exact subsolutionMaximum n U T u hU hOpen hBounded hT hContinuous
    (caloric_isSubcaloric hCaloric)

#print axioms caloric_isSubcaloric
#print axioms root_of_subsolutionMaximumPrinciple

end Stage1Instances.THM_M_1133
