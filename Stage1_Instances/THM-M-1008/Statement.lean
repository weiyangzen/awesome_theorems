import Mathlib.Probability.IdentDistribIndep

/-!
# THM-M-1008: exact Hewitt-Savage zero-one statement

This module freezes the path-space formulation of the theorem. It contains no
proof of the zero-one law.
-/

noncomputable section

open MeasureTheory ProbabilityTheory
open scoped ENNReal MeasureTheory ProbabilityTheory

namespace Stage1Instances.THM_M_1008

universe u v

/-- The sample path of a discrete-time process. -/
def processPath {Omega : Type u} {E : Type v} (X : Nat -> Omega -> E)
    (omega : Omega) : Nat -> E :=
  fun n => X n omega

/-- Reindex a path by a permutation of its coordinates. -/
def permutedPath {E : Type v} (sigma : Equiv.Perm Nat) (x : Nat -> E) : Nat -> E :=
  fun n => x (sigma n)

/-- A permutation moves only finitely many coordinates. -/
def HasFiniteSupport (sigma : Equiv.Perm Nat) : Prop :=
  Set.Finite {n | sigma n ≠ n}

/-- A path event is invariant under every finite-support coordinate permutation. -/
def IsSymmetricEvent {E : Type v} (event : Set (Nat -> E)) : Prop :=
  forall sigma : Equiv.Perm Nat, HasFiniteSupport sigma ->
    forall x : Nat -> E, x ∈ event ↔ permutedPath sigma x ∈ event

/-- Exact path-space formulation of the Hewitt-Savage zero-one law. -/
def HewittSavageZeroOneTarget : Prop :=
  forall (Omega : Type u) (E : Type v)
    [MeasurableSpace Omega] [MeasurableSpace E]
    (mu : Measure Omega) [IsProbabilityMeasure mu]
    (X : Nat -> Omega -> E) (event : Set (Nat -> E)),
      iIndepFun X mu ->
      (forall i j : Nat, IdentDistrib (X i) (X j) mu mu) ->
      MeasurableSet event ->
      IsSymmetricEvent event ->
      mu (processPath X ⁻¹' event) = 0 ∨ mu (processPath X ⁻¹' event) = 1

/-- Direct expansion of the selected target, used as a checked transport. -/
def ExpandedSourceShape : Prop :=
  forall (Omega : Type u) (E : Type v)
    [MeasurableSpace Omega] [MeasurableSpace E]
    (mu : Measure Omega) [IsProbabilityMeasure mu]
    (X : Nat -> Omega -> E) (event : Set (Nat -> E)),
      iIndepFun X mu ->
      (forall i j : Nat, IdentDistrib (X i) (X j) mu mu) ->
      MeasurableSet event ->
      (forall sigma : Equiv.Perm Nat, Set.Finite {n | sigma n ≠ n} ->
        forall x : Nat -> E,
          x ∈ event ↔ (fun n => x (sigma n)) ∈ event) ->
      mu {omega | (fun n => X n omega) ∈ event} = 0 ∨
        mu {omega | (fun n => X n omega) ∈ event} = 1

theorem target_iff_expandedSourceShape :
    HewittSavageZeroOneTarget.{u, v} <-> ExpandedSourceShape.{u, v} := by
  rfl

-- Separately elaborated, deliberately non-equivalent structural mutations.
def mutationRemovedIndependence : Prop :=
  forall (Omega : Type u) (E : Type v)
    [MeasurableSpace Omega] [MeasurableSpace E]
    (mu : Measure Omega) [IsProbabilityMeasure mu]
    (X : Nat -> Omega -> E) (event : Set (Nat -> E)),
      (forall i j, IdentDistrib (X i) (X j) mu mu) ->
      MeasurableSet event -> IsSymmetricEvent event ->
      mu (processPath X ⁻¹' event) = 0 ∨ mu (processPath X ⁻¹' event) = 1

def mutationChangedIndexDomain : Prop :=
  forall (Omega : Type u) (E : Type v)
    [MeasurableSpace Omega] [MeasurableSpace E]
    (mu : Measure Omega) [IsProbabilityMeasure mu]
    (X : Int -> Omega -> E), iIndepFun X mu -> True

def mutationChangedBinderScope : Prop :=
  forall (Omega : Type u) (E : Type v)
    [MeasurableSpace Omega] [MeasurableSpace E]
    (mu : Measure Omega) [IsProbabilityMeasure mu],
      exists X : Nat -> Omega -> E, iIndepFun X mu

def mutationAllPermutations : Prop :=
  forall (Omega : Type u) (E : Type v)
    [MeasurableSpace Omega] [MeasurableSpace E]
    (mu : Measure Omega) [IsProbabilityMeasure mu]
    (X : Nat -> Omega -> E) (event : Set (Nat -> E)),
      iIndepFun X mu ->
      (forall i j, IdentDistrib (X i) (X j) mu mu) ->
      MeasurableSet event ->
      (forall sigma : Equiv.Perm Nat, forall x : Nat -> E,
        x ∈ event ↔ permutedPath sigma x ∈ event) ->
      mu (processPath X ⁻¹' event) = 0 ∨ mu (processPath X ⁻¹' event) = 1

/-- The identity permutation satisfies the selected finite-support boundary. -/
theorem identity_hasFiniteSupport : HasFiniteSupport (Equiv.refl Nat) := by
  simp [HasFiniteSupport]

end Stage1Instances.THM_M_1008

set_option pp.explicit true in
#print Stage1Instances.THM_M_1008.HewittSavageZeroOneTarget
