import Statement

/-!
# THM-M-0325 proof execution

This module implements elementary, reusable proof bodies at the scalar and
Hilbert-form boundary of the frozen Grothendieck architecture. It does not
construct the still-missing Krivine transform or random-rounding package and
therefore does not prove `GrothendieckInequalityTarget`.
-/

noncomputable section

open scoped BigOperators RealInnerProductSpace

namespace Stage1Instances.THM_M_0325

universe u

/-- The scalar hypothesis applies directly to any two unit-polydisc families. -/
theorem scalarUnitBoundedBy_apply {m n : Type u} [Fintype m] [Fintype n]
    {A : m -> n -> Real} {C : Real} (hA : ScalarUnitBoundedBy A C)
    (s : m -> Real) (t : n -> Real)
    (hs : forall i, abs (s i) <= 1) (ht : forall j, abs (t j) <= 1) :
    abs (ScalarMatrixForm A s t) <= C := by
  exact hA s t hs ht

/-- Sign-valued scalar families satisfy the unit-polydisc side conditions. -/
theorem scalarUnitBoundedBy_of_abs_eq_one {m n : Type u}
    [Fintype m] [Fintype n] {A : m -> n -> Real} {C : Real}
    (hA : ScalarUnitBoundedBy A C) (s : m -> Real) (t : n -> Real)
    (hs : forall i, abs (s i) = 1) (ht : forall j, abs (t j) = 1) :
    abs (ScalarMatrixForm A s t) <= C := by
  apply hA s t
  · intro i
    exact (hs i).le
  · intro j
    exact (ht j).le

/-- Every scalar unit-polydisc bound is nonnegative. -/
theorem nonneg_of_scalarUnitBoundedBy {m n : Type u} [Fintype m] [Fintype n]
    {A : m -> n -> Real} {C : Real} (hA : ScalarUnitBoundedBy A C) :
    0 <= C := by
  simpa [ScalarMatrixForm] using hA (fun _ => 0) (fun _ => 0)
    (fun _ => by norm_num) (fun _ => by norm_num)

/-- The scalar form of the zero matrix vanishes. -/
theorem scalarMatrixForm_zero {m n : Type u} [Fintype m] [Fintype n]
    (s : m -> Real) (t : n -> Real) :
    ScalarMatrixForm (fun _ _ => 0) s t = 0 := by
  simp [ScalarMatrixForm]

/-- The Hilbert form of the zero matrix vanishes. -/
theorem hilbertMatrixForm_zero {m n : Type u} [Fintype m] [Fintype n]
    (H : Type u) [NormedAddCommGroup H] [InnerProductSpace Real H]
    (x : m -> H) (y : n -> H) :
    HilbertMatrixForm (fun _ _ => 0) H x y = 0 := by
  simp [HilbertMatrixForm]

/-- The zero matrix has every nonnegative scalar unit-polydisc bound. -/
theorem zero_scalarUnitBoundedBy {m n : Type u} [Fintype m] [Fintype n]
    {C : Real} (hC : 0 <= C) :
    ScalarUnitBoundedBy (fun (_ : m) (_ : n) => 0) C := by
  intro s t hs ht
  simpa [ScalarMatrixForm] using hC

/-- The zero matrix has every nonnegative Hilbert unit-ball bound. -/
theorem zero_hilbertUnitBoundedBy {m n : Type u} [Fintype m] [Fintype n]
    {C : Real} (hC : 0 <= C) :
    HilbertUnitBoundedBy (fun (_ : m) (_ : n) => 0) C := by
  intro H _ _ x y hx hy
  simpa [HilbertMatrixForm] using hC

/-- A single real inner product of unit-ball vectors has absolute value at most one. -/
theorem abs_real_inner_le_one_of_norm_le_one
    {H : Type u} [NormedAddCommGroup H] [InnerProductSpace Real H]
    {x y : H} (hx : norm x <= 1) (hy : norm y <= 1) :
    abs (@inner Real H _ x y) <= 1 := by
  calc
    abs (@inner Real H _ x y) <= norm x * norm y := abs_real_inner_le_norm x y
    _ <= 1 * 1 := mul_le_mul hx hy (norm_nonneg y) (by norm_num)
    _ = 1 := by norm_num

/-- Each coefficient-inner-product term is bounded by the coefficient magnitude on unit balls. -/
theorem abs_matrix_inner_term_le {m n : Type u} [Fintype m] [Fintype n]
    (A : m -> n -> Real) (H : Type u)
    [NormedAddCommGroup H] [InnerProductSpace Real H]
    (x : m -> H) (y : n -> H)
    (hx : forall i, norm (x i) <= 1) (hy : forall j, norm (y j) <= 1)
    (i : m) (j : n) :
    abs (A i j * inner Real (x i) (y j)) <= abs (A i j) := by
  rw [abs_mul]
  exact mul_le_of_le_one_right (abs_nonneg (A i j))
    (abs_real_inner_le_one_of_norm_le_one (hx i) (hy j))

/-- The Hilbert matrix form is controlled by the coefficient `l1` sum on unit balls. -/
theorem abs_hilbertMatrixForm_le_sum_abs {m n : Type u}
    [Fintype m] [Fintype n] (A : m -> n -> Real)
    (H : Type u) [NormedAddCommGroup H] [InnerProductSpace Real H]
    (x : m -> H) (y : n -> H)
    (hx : forall i, norm (x i) <= 1) (hy : forall j, norm (y j) <= 1) :
    abs (HilbertMatrixForm A H x y) <= ∑ i, ∑ j, abs (A i j) := by
  calc
    abs (HilbertMatrixForm A H x y)
        <= ∑ i, abs (∑ j, A i j * @inner Real H _ (x i) (y j)) := by
          simpa [HilbertMatrixForm] using
            (Finset.abs_sum_le_sum_abs
              (fun i => ∑ j, A i j * @inner Real H _ (x i) (y j)) Finset.univ)
    _ <= ∑ i, ∑ j, abs (A i j * @inner Real H _ (x i) (y j)) := by
          apply Finset.sum_le_sum
          intro i hi
          simpa using
            (Finset.abs_sum_le_sum_abs
              (fun j => A i j * @inner Real H _ (x i) (y j)) Finset.univ)
    _ <= ∑ i, ∑ j, abs (A i j) := by
          apply Finset.sum_le_sum
          intro i hi
          apply Finset.sum_le_sum
          intro j hj
          exact abs_matrix_inner_term_le A H x y hx hy i j

/-- The coefficient `l1` sum is always a valid Hilbert-unit-ball bound. -/
theorem hilbertUnitBoundedBy_sum_abs {m n : Type u}
    [Fintype m] [Fintype n] (A : m -> n -> Real) :
    HilbertUnitBoundedBy A (∑ i, ∑ j, abs (A i j)) := by
  intro H _ _ x y hx hy
  exact abs_hilbertMatrixForm_le_sum_abs A H x y hx hy

#print axioms scalarUnitBoundedBy_apply
#print axioms scalarUnitBoundedBy_of_abs_eq_one
#print axioms nonneg_of_scalarUnitBoundedBy
#print axioms scalarMatrixForm_zero
#print axioms hilbertMatrixForm_zero
#print axioms zero_scalarUnitBoundedBy
#print axioms zero_hilbertUnitBoundedBy
#print axioms abs_real_inner_le_one_of_norm_le_one
#print axioms abs_matrix_inner_term_le
#print axioms abs_hilbertMatrixForm_le_sum_abs
#print axioms hilbertUnitBoundedBy_sum_abs

end Stage1Instances.THM_M_0325
