import Statement

/-!
# THM-M-1006 proof execution

This module implements the algebraic difference-process and horizon-zero leaves of the frozen
BDG obligation tree.  The analytic good-lambda and moment-comparison obligations remain open.
-/

open MeasureTheory

namespace Stage1Instances.THM_M_1006

universe u

/-- The one-step difference process associated with a discrete process. -/
def martingaleDifference (f : Nat -> Ω -> Real) (k : Nat) (ω : Ω) : Real :=
  f (k + 1) ω - f k ω

/-- Finite sums of the difference process telescope to the terminal value minus the initial one. -/
theorem sum_martingaleDifference (f : Nat -> Ω -> Real) (n : Nat) (ω : Ω) :
    (∑ k ∈ Finset.range n, martingaleDifference f k ω) = f n ω - f 0 ω := by
  unfold martingaleDifference
  exact Finset.sum_range_sub (fun k => f k ω) n

/-- A zero-start process is reconstructed pointwise by its finite difference sums. -/
theorem sum_martingaleDifference_of_zero
    (f : Nat -> Ω -> Real) (hf0 : f 0 = 0) (n : Nat) (ω : Ω) :
    (∑ k ∈ Finset.range n, martingaleDifference f k ω) = f n ω := by
  rw [sum_martingaleDifference, hf0]
  simp

/-- The frozen quadratic variation has value zero at horizon zero. -/
theorem quadraticVariation_zero (f : Nat -> Ω -> Real) (ω : Ω) :
    quadraticVariation f 0 ω = 0 := by
  simp [quadraticVariation]

/-- At horizon zero the frozen maximal process is the absolute initial value. -/
theorem maximalProcess_zero (f : Nat -> Ω -> Real) (ω : Ω) :
    maximalProcess f 0 ω = |f 0 ω| := by
  simp [maximalProcess]

/-- Hence both pointwise quantities in the frozen target vanish at horizon zero for a zero-start
process. -/
theorem boundary_zero
    (f : Nat -> Ω -> Real) (hf0 : f 0 = 0) (ω : Ω) :
    maximalProcess f 0 ω = 0 ∧ quadraticVariation f 0 ω = 0 := by
  constructor
  · rw [maximalProcess_zero, hf0]
    simp
  · exact quadraticVariation_zero f ω

#print axioms sum_martingaleDifference
#print axioms sum_martingaleDifference_of_zero
#print axioms quadraticVariation_zero
#print axioms maximalProcess_zero
#print axioms boundary_zero

end Stage1Instances.THM_M_1006
