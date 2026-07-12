import Mathlib.Analysis.Calculus.ContDiff.Basic
import Mathlib.Analysis.InnerProductSpace.PiL2

/-!
# THM-M-1133: weak maximum principle for the heat equation

This module freezes the statement selected by the rev-5.6 intake. It defines
the classical cylinder formulation; it does not prove the maximum principle.
-/

noncomputable section

open Set
open scoped BigOperators

namespace Stage1Instances.THM_M_1133

/-- The finite-dimensional real spatial domain used by the target. -/
abbrev Space (n : Nat) := EuclideanSpace Real (Fin n)

/-- The closed space-time cylinder `closure U x [0,T]`. -/
def ClosedCylinder {n : Nat} (U : Set (Space n)) (T : Real) : Set (Space n × Real) :=
  closure U ×ˢ Icc 0 T

/-- The initial face together with the lateral boundary. The terminal interior
face is deliberately not included. -/
def ParabolicBoundary {n : Nat} (U : Set (Space n)) (T : Real) : Set (Space n × Real) :=
  (closure U ×ˢ ({0} : Set Real)) ∪ (frontier U ×ˢ Icc 0 T)

/-- The coordinate Laplacian, expressed using the standard orthonormal basis
of Euclidean space and Fréchet derivatives. -/
def spatialLaplacian {n : Nat} (u : Space n → Real → Real) (x : Space n) (t : Real) : Real :=
  ∑ i : Fin n,
    fderiv Real (fun y => fderiv Real (fun z => u z t) y (EuclideanSpace.single i 1)) x
      (EuclideanSpace.single i 1)

/-- Classical `C2`-in-space, `C1`-in-time caloricity on `U x (0,T]`, with
the forward sign convention `partial_t u - Delta u = 0`. -/
def IsClassicalCaloricOn {n : Nat} (U : Set (Space n)) (T : Real)
    (u : Space n → Real → Real) : Prop :=
  (∀ x ∈ U, ∀ t ∈ Ioc 0 T,
      ContDiffAt Real 2 (fun y => u y t) x ∧
      ContDiffAt Real 1 (fun s => u x s) t) ∧
    ∀ x ∈ U, ∀ t ∈ Ioc 0 T,
      deriv (fun s => u x s) t - spatialLaplacian u x t = 0

/-- Exact target selected at intake: a classical caloric function on a
nonempty bounded spatial cylinder has a global maximizer on its parabolic
boundary. -/
def HeatEquationWeakMaximumPrinciple : Prop :=
  ∀ (n : Nat) (U : Set (Space n)) (T : Real) (u : Space n → Real → Real),
    U.Nonempty → IsOpen U → Bornology.IsBounded U → 0 < T →
    ContinuousOn (fun p : Space n × Real => u p.1 p.2) (ClosedCylinder U T) →
    IsClassicalCaloricOn U T u →
    ∃ p ∈ ParabolicBoundary U T,
      ∀ q ∈ ClosedCylinder U T, u q.1 q.2 ≤ u p.1 p.2

-- Structural mutations are elaborated independently and are not aliases of the root.
def mutationRemovedBoundedness : Prop :=
  ∀ (n : Nat) (U : Set (Space n)) (T : Real) (u : Space n → Real → Real),
    U.Nonempty → IsOpen U → 0 < T →
    ContinuousOn (fun p : Space n × Real => u p.1 p.2) (ClosedCylinder U T) →
    IsClassicalCaloricOn U T u →
    ∃ p ∈ ParabolicBoundary U T,
      ∀ q ∈ ClosedCylinder U T, u q.1 q.2 ≤ u p.1 p.2

def mutationChangedSign : Prop :=
  ∀ (n : Nat) (U : Set (Space n)) (T : Real) (u : Space n → Real → Real),
    U.Nonempty → IsOpen U → Bornology.IsBounded U → 0 < T →
    ContinuousOn (fun p : Space n × Real => u p.1 p.2) (ClosedCylinder U T) →
    (∀ x ∈ U, ∀ t ∈ Ioc 0 T,
      deriv (fun s => u x s) t + spatialLaplacian u x t = 0) →
    ∃ p ∈ ParabolicBoundary U T,
      ∀ q ∈ ClosedCylinder U T, u q.1 q.2 ≤ u p.1 p.2

def mutationTerminalFaceBoundary : Prop :=
  ∀ (n : Nat) (U : Set (Space n)) (T : Real) (u : Space n → Real → Real),
    U.Nonempty → IsOpen U → Bornology.IsBounded U → 0 < T →
    ContinuousOn (fun p : Space n × Real => u p.1 p.2) (ClosedCylinder U T) →
    IsClassicalCaloricOn U T u →
    ∃ p ∈ (ParabolicBoundary U T ∪ (closure U ×ˢ ({T} : Set Real))),
      ∀ q ∈ ClosedCylinder U T, u q.1 q.2 ≤ u p.1 p.2

def mutationChangedBinderScope : Prop :=
  ∀ (n : Nat) (U : Set (Space n)) (T : Real),
    U.Nonempty → IsOpen U → Bornology.IsBounded U → 0 < T →
    ∀ u : Space n → Real → Real,
      ContinuousOn (fun p : Space n × Real => u p.1 p.2) (ClosedCylinder U T) ∧
      IsClassicalCaloricOn U T u ∧
      ∃ p ∈ ParabolicBoundary U T,
        ∀ q ∈ ClosedCylinder U T, u q.1 q.2 ≤ u p.1 p.2

end Stage1Instances.THM_M_1133

set_option pp.explicit true in
#print Stage1Instances.THM_M_1133.HeatEquationWeakMaximumPrinciple
