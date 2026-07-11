import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.FieldTheory.IntermediateField.Adjoin.Basic

/-!
# THM-M-0401 exact statement boundary

This module freezes Schmidt's simultaneous approximation theorem in its
product form. It contains statement-level checks only and does not prove the
theorem.
-/

set_option autoImplicit false

noncomputable section

open scoped BigOperators

namespace Stage1Instances.THMM0401

/-- Every coordinate is algebraic over the rationals. -/
def AlgebraicVector (n : Nat) (alpha : Fin n -> Real) : Prop :=
  forall i, IsAlgebraic Rat (alpha i)

/-- Linear independence over `Rat` of `1` together with all coordinates. -/
def RationalIndependenceWithOne (n : Nat) (alpha : Fin n -> Real) : Prop :=
  LinearIndependent Rat (fun j : Option (Fin n) =>
    match j with
    | none => (1 : Real)
    | some i => alpha i)

/-- `d` is the distance from `x` to the nearest integer. -/
def IsNearestIntegerDistance (x d : Real) : Prop :=
  0 <= d ∧
    ∃ m : Int,
      d = |x - (m : Real)| ∧
        ∀ z : Int, d <= |x - (z : Real)|

/-- The exceptional-denominator predicate in the product formulation. -/
def ProductTooGood
    (n : Nat) (alpha : Fin n -> Real) (epsilon : Real) (q : Nat) : Prop :=
  0 < q ∧
    ∃ d : Fin n -> Real,
      (∀ i, IsNearestIntegerDistance ((q : Real) * alpha i) (d i)) ∧
        (∏ i, d i) < Real.rpow (q : Real) (-1 - epsilon)

/-- The exact rev-5.6 formal target for Schmidt's product theorem. -/
def SchmidtSimultaneousApproximationTarget : Prop :=
  ∀ (n : Nat), 0 < n ->
    ∀ alpha : Fin n -> Real,
      AlgebraicVector n alpha ->
      RationalIndependenceWithOne n alpha ->
      ∀ epsilon : Real, 0 < epsilon ->
        Set.Finite {q : Nat | ProductTooGood n alpha epsilon q}

/-- Local restatement of the legacy discovery candidate. -/
def LegacyCanonicalProductStatementShape : Prop :=
  ∀ (n : Nat), 0 < n ->
    ∀ alpha : Fin n -> Real,
      AlgebraicVector n alpha ->
      RationalIndependenceWithOne n alpha ->
      ∀ epsilon : Real, 0 < epsilon ->
        Set.Finite {q : Nat | ProductTooGood n alpha epsilon q}

/-- Checked statement identity with the legacy product-form encoding. -/
theorem target_iff_legacyCanonicalProductStatementShape :
    SchmidtSimultaneousApproximationTarget <->
      LegacyCanonicalProductStatementShape := by
  rfl

/-! The following guarded probes must produce elaboration errors. They ensure
that four common mutations are not definitionally accepted as the frozen
target. No proposition below is asserted or credited as proof evidence. -/

/- Mutation probe: deleting algebraicity changes the target. -/
#guard_msgs (drop error) in
example : SchmidtSimultaneousApproximationTarget =
    (∀ (n : Nat), 0 < n ->
      ∀ alpha : Fin n -> Real,
        RationalIndependenceWithOne n alpha ->
        ∀ epsilon : Real, 0 < epsilon ->
          Set.Finite {q : Nat | ProductTooGood n alpha epsilon q}) := by
  rfl

/- Mutation probe: changing denominators from naturals to integers is rejected. -/
#guard_msgs (drop error) in
example : (Nat -> Prop) = (Int -> Prop) := by
  rfl

/- Mutation probe: moving epsilon outside the dimension binder is rejected. -/
#guard_msgs (drop error) in
example : SchmidtSimultaneousApproximationTarget =
    (∀ epsilon : Real, 0 < epsilon ->
      ∀ (n : Nat), 0 < n ->
        ∀ alpha : Fin n -> Real,
          AlgebraicVector n alpha ->
          RationalIndependenceWithOne n alpha ->
          Set.Finite {q : Nat | ProductTooGood n alpha epsilon q}) := by
  rfl

/- Mutation probe: admitting zero dimension changes the binder boundary. -/
#guard_msgs (drop error) in
example : SchmidtSimultaneousApproximationTarget =
    (∀ (n : Nat),
      ∀ alpha : Fin n -> Real,
        AlgebraicVector n alpha ->
        RationalIndependenceWithOne n alpha ->
        ∀ epsilon : Real, 0 < epsilon ->
          Set.Finite {q : Nat | ProductTooGood n alpha epsilon q}) := by
  rfl

end Stage1Instances.THMM0401

set_option pp.universes true in
set_option pp.explicit true in
set_option pp.all true in
#print Stage1Instances.THMM0401.SchmidtSimultaneousApproximationTarget
