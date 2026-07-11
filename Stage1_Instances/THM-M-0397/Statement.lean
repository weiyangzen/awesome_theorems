import Mathlib.Analysis.SpecialFunctions.Complex.Log
import Mathlib.FieldTheory.AlgebraicClosure

/-!
# THM-M-0397: Baker method (statement boundary)

This module freezes the method-level claim: a Baker lower bound, together with
a problem-specific reduction to a computable height ball, yields an explicit
finite list containing exactly the solutions.  It does not assert a Baker
lower bound for any particular logarithmic form or a reduction for any
particular Diophantine equation.
-/

noncomputable section

open scoped BigOperators

namespace Stage1Rev56.THMM0397

universe u

/-- Algebraic targets, chosen logarithms, and integer coefficients for a linear form. -/
structure LinearLogData where
  n : Nat
  alpha : Fin n -> Complex
  logarithm : Fin n -> Complex
  coefficient : Fin n -> Int
  alpha_ne_zero : forall i, Not (alpha i = 0)
  alpha_algebraic : forall i, IsAlgebraic Rat (alpha i)
  exp_logarithm : forall i, Complex.exp (logarithm i) = alpha i

/-- The linear form in chosen logarithms used by the application. -/
def linearForm (L : LinearLogData) : Complex :=
  Finset.univ.sum fun i : Fin L.n =>
    (L.coefficient i : Complex) * L.logarithm i

/-- A concrete strict lower-bound assertion for a nonzero logarithmic linear form. -/
def HasBakerLowerBound (L : LinearLogData) (lowerBound : Real) : Prop :=
  Not (linearForm L = 0) -> lowerBound < norm (linearForm L)

/--
All problem-specific data required after the logarithmic lower-bound theorem.

`heightBall` is executable finite-search data.  `heightBall_spec` says it lists
exactly the objects up to the indicated height.  `reduce_solution` is the
mathematical Baker-method bridge: the selected lower bound forces every
Diophantine solution into the chosen search ball.
-/
structure Application where
  Solution : Type u
  instDecidableEq : DecidableEq Solution
  isSolution : Solution -> Prop
  instDecidableSolution : DecidablePred isSolution
  height : Solution -> Nat
  searchBound : Nat
  heightBall : Nat -> Finset Solution
  heightBall_spec : forall B x, x ∈ heightBall B <-> height x <= B
  logData : LinearLogData
  lowerBound : Real
  reduce_solution :
    HasBakerLowerBound logData lowerBound ->
      forall x, isSolution x -> height x <= searchBound

attribute [instance] Application.instDecidableEq
attribute [instance] Application.instDecidableSolution

/-- The executable list obtained by filtering the bounded height ball. -/
def solutionList (A : Application) : Finset A.Solution :=
  (A.heightBall A.searchBound).filter A.isSolution

/--
The selected exact Baker-method target.

For every specified application, a proof of its concrete Baker lower bound
makes the executable list `solutionList A` extensionally equal to the full
solution predicate.
-/
def Statement : Prop :=
  forall A : Application.{u},
    HasBakerLowerBound A.logData A.lowerBound ->
      forall x, x ∈ solutionList A <-> A.isSolution x

/-- Checked expansion of all binders, the lower-bound premise, and the conclusion. -/
theorem statement_iff_expanded :
    Statement.{u} <->
      forall A : Application.{u},
        (Not (linearForm A.logData = 0) ->
          A.lowerBound < norm (linearForm A.logData)) ->
        forall x, x ∈ (A.heightBall A.searchBound).filter A.isSolution <->
          A.isSolution x := by
  unfold Statement HasBakerLowerBound solutionList
  rfl

/-- Boundary check: list membership entails both bounded height and the equation. -/
theorem mem_solutionList_iff (A : Application) (x : A.Solution) :
    x ∈ solutionList A <-> A.height x <= A.searchBound ∧ A.isSolution x := by
  simp [solutionList, A.heightBall_spec]

#check Statement

end Stage1Rev56.THMM0397
