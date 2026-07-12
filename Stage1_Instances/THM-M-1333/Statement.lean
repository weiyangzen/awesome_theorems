import Mathlib.Analysis.Calculus.Deriv.Basic

/-!
# THM-M-1333: exact Peano-existence statement

This module freezes the finite-dimensional local-existence statement only. It
contains no proof of Peano's theorem.
-/

namespace Stage1Instances.THM_M_1333

/-- The finite-dimensional real state space used by the canonical target. -/
abbrev StateSpace (n : Nat) := Fin n -> Real

/-- A curve is a solution within `I` when its graph stays in the vector
field's domain and it has the required derivative within `I`, including at
the endpoints in the one-sided sense. -/
def IsSolutionWithin {n : Nat} (U : Set (Real × StateSpace n))
    (f : Real -> StateSpace n -> StateSpace n) (I : Set Real)
    (x : Real -> StateSpace n) : Prop :=
  ∀ t, t ∈ I -> (t, x t) ∈ U ∧ HasDerivWithinAt x (f t (x t)) I t

/-- The canonical finite-dimensional Peano existence target. A continuous
vector field on an open neighborhood of the initial data has a solution on
some nondegenerate closed interval centered at the initial time. -/
def PeanoExistenceTarget : Prop :=
  ∀ (n : Nat) (U : Set (Real × StateSpace n))
    (f : Real -> StateSpace n -> StateSpace n) (t0 : Real) (x0 : StateSpace n),
      IsOpen U ->
      (t0, x0) ∈ U ->
      ContinuousOn (fun p : Real × StateSpace n => f p.1 p.2) U ->
      ∃ epsilon : Real, 0 < epsilon ∧
        ∃ x : Real -> StateSpace n,
          x t0 = x0 ∧
          IsSolutionWithin U f (Set.Icc (t0 - epsilon) (t0 + epsilon)) x

/-- Fully expanded spelling used to check the selected solution encoding. -/
def ExpandedTarget : Prop :=
  ∀ (n : Nat) (U : Set (Real × (Fin n -> Real)))
    (f : Real -> (Fin n -> Real) -> (Fin n -> Real))
    (t0 : Real) (x0 : Fin n -> Real),
      IsOpen U -> (t0, x0) ∈ U ->
      ContinuousOn (fun p : Real × (Fin n -> Real) => f p.1 p.2) U ->
      ∃ epsilon : Real, 0 < epsilon ∧
        ∃ x : Real -> (Fin n -> Real), x t0 = x0 ∧
          ∀ t, t ∈ Set.Icc (t0 - epsilon) (t0 + epsilon) ->
            (t, x t) ∈ U ∧
              HasDerivWithinAt x (f t (x t))
                (Set.Icc (t0 - epsilon) (t0 + epsilon)) t

/-- Checked definitional transport to the fully expanded encoding. -/
theorem peanoExistenceTarget_iff_expandedTarget :
    PeanoExistenceTarget ↔ ExpandedTarget :=
  Iff.rfl

-- Structural mutations elaborate separately and are distinguished by the
-- statement checker; none is credited as an alternate form.
def mutationRemovedContinuity : Prop :=
  ∀ (n : Nat) (U : Set (Real × StateSpace n))
    (f : Real -> StateSpace n -> StateSpace n) (t0 : Real) (x0 : StateSpace n),
      IsOpen U -> (t0, x0) ∈ U ->
      ∃ epsilon : Real, 0 < epsilon ∧
        ∃ x : Real -> StateSpace n, x t0 = x0 ∧
          IsSolutionWithin U f (Set.Icc (t0 - epsilon) (t0 + epsilon)) x

def mutationScalarDomain : Prop :=
  ∀ (U : Set (Real × Real)) (f : Real -> Real -> Real) (t0 x0 : Real),
    IsOpen U -> (t0, x0) ∈ U ->
    ContinuousOn (fun p : Real × Real => f p.1 p.2) U ->
    ∃ epsilon : Real, 0 < epsilon ∧ ∃ x : Real -> Real,
      x t0 = x0 ∧ ∀ t, t ∈ Set.Icc (t0 - epsilon) (t0 + epsilon) ->
        (t, x t) ∈ U ∧ HasDerivWithinAt x (f t (x t))
          (Set.Icc (t0 - epsilon) (t0 + epsilon)) t

def mutationCurveBeforeRadius : Prop :=
  ∀ (n : Nat) (U : Set (Real × StateSpace n))
    (f : Real -> StateSpace n -> StateSpace n) (t0 : Real) (x0 : StateSpace n),
      IsOpen U -> (t0, x0) ∈ U ->
      ContinuousOn (fun p : Real × StateSpace n => f p.1 p.2) U ->
      ∃ x : Real -> StateSpace n, x t0 = x0 ∧
        ∃ epsilon : Real, 0 < epsilon ∧
          IsSolutionWithin U f (Set.Icc (t0 - epsilon) (t0 + epsilon)) x

def mutationAllowsZeroRadius : Prop :=
  ∀ (n : Nat) (U : Set (Real × StateSpace n))
    (f : Real -> StateSpace n -> StateSpace n) (t0 : Real) (x0 : StateSpace n),
      IsOpen U -> (t0, x0) ∈ U ->
      ContinuousOn (fun p : Real × StateSpace n => f p.1 p.2) U ->
      ∃ epsilon : Real, 0 ≤ epsilon ∧
        ∃ x : Real -> StateSpace n, x t0 = x0 ∧
          IsSolutionWithin U f (Set.Icc (t0 - epsilon) (t0 + epsilon)) x

end Stage1Instances.THM_M_1333

set_option pp.explicit true in
#print Stage1Instances.THM_M_1333.PeanoExistenceTarget
