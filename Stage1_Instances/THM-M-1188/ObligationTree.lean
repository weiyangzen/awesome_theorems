import Mathlib.Analysis.InnerProductSpace.Laplacian

/-!
# THM-M-1188 conditional obligation composition

This module gives typed interfaces for the frozen maximum-principle proof route
and checks their exact composition into the canonical target.  The analytic
engine is an explicit premise: this file does not prove the maximum principle.
-/

namespace Stage1Instances.THM_M_1188.ObligationTree

open scoped InnerProductSpace
open Laplacian

abbrev Euclidean (n : Nat) := EuclideanSpace Real (Fin n)

def closedCylinder {n : Nat} (U : Set (Euclidean n)) (T : Real) :
    Set (Euclidean n × Real) :=
  closure U ×ˢ Set.Icc 0 T

def parabolicBoundary {n : Nat} (U : Set (Euclidean n)) (T : Real) :
    Set (Euclidean n × Real) :=
  (closure U ×ˢ ({0} : Set Real)) ∪ (frontier U ×ˢ Set.Icc 0 T)

def IsHeatSubsolution {n : Nat} (U : Set (Euclidean n)) (T : Real)
    (u : Euclidean n × Real → Real) : Prop :=
  ∀ x ∈ U, ∀ t ∈ Set.Ioc 0 T,
    deriv (fun s : Real ↦ u (x, s)) t -
      (@Laplacian.laplacian (Euclidean n → Real) (Euclidean n → Real)
        InnerProductSpace.instLaplacian (fun y : Euclidean n ↦ u (y, t))) x ≤ 0

def HasClassicalHeatRegularity {n : Nat} (U : Set (Euclidean n)) (T : Real)
    (u : Euclidean n × Real → Real) : Prop :=
  ContinuousOn u (closedCylinder U T) ∧
  (∀ t ∈ Set.Ioc 0 T, ContDiffOn Real 2 (fun x : Euclidean n ↦ u (x, t)) U) ∧
  (∀ x ∈ U, ContDiffOn Real 1 (fun t : Real ↦ u (x, t)) (Set.Ioc 0 T))

def BoundaryDominance {n : Nat} (U : Set (Euclidean n)) (T : Real)
    (u : Euclidean n × Real → Real) : Prop :=
  ∃ b ∈ parabolicBoundary U T, ∀ z ∈ closedCylinder U T, u z ≤ u b

def Root : Prop :=
  ∀ (n : Nat), 1 ≤ n → ∀ (U : Set (Euclidean n)), U.Nonempty → IsOpen U →
    Bornology.IsBounded U → ∀ (T : Real), 0 < T →
      ∀ u : Euclidean n × Real → Real,
        HasClassicalHeatRegularity U T u → IsHeatSubsolution U T u →
          BoundaryDominance U T u

/-- Interface produced after compact-extremum, strict-perturbation, interior
exclusion, boundary-identification, and epsilon-removal obligations close. -/
def AnalyticMaximumEngine : Prop :=
  ∀ (n : Nat), 1 ≤ n → ∀ (U : Set (Euclidean n)), U.Nonempty → IsOpen U →
    Bornology.IsBounded U → ∀ (T : Real), 0 < T →
      ∀ u : Euclidean n × Real → Real,
        HasClassicalHeatRegularity U T u → IsHeatSubsolution U T u →
          BoundaryDominance U T u

/-- Exact child-to-root composition.  `engine` remains an open analytic
premise and therefore this theorem gives no proof credit to the root. -/
theorem root_compose (engine : AnalyticMaximumEngine) : Root := by
  intro n hn U hU hopen hbounded T hT u hregular hsub
  exact engine n hn U hU hopen hbounded T hT u hregular hsub

#print axioms root_compose

end Stage1Instances.THM_M_1188.ObligationTree
