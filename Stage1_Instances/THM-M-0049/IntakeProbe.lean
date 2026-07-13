import Mathlib.LinearAlgebra.Matrix.Rank

/-!
# THM-M-0049 discovery-only intake probe

These checks authenticate pinned matrix-rank and finite-dimensional linear-map interfaces and
verify that one candidate Frobenius triple-product proposition shape elaborates. They do not
select a canonical source claim, declare or prove the inequality, or give proof credit to adjacent
two-factor and zero-product results.
-/

#check Matrix.rank
#check Matrix.rank_mul_le_left
#check Matrix.rank_mul_le_right
#check Matrix.rank_mul_le
#check Matrix.rank_eq_finrank_range_toLin
#check Matrix.rank_add_rank_le_card_of_mul_eq_zero
#check LinearMap.rank_comp_le_left
#check LinearMap.rank_comp_le_right
#check LinearMap.rank_comp_le
#check LinearMap.finrank_range_add_finrank_ker

-- Conventional source-family shape only; not the canonical target.
#check fun {m n p q : Type} [Fintype n] [Fintype p] [Fintype q]
    {K : Type} [Field K]
    (A : Matrix m n K) (B : Matrix n p K) (C : Matrix p q K) =>
  (A * B).rank + (B * C).rank <= B.rank + ((A * B) * C).rank

#print axioms Matrix.rank_mul_le_left
#print axioms Matrix.rank_mul_le_right
#print axioms Matrix.rank_add_rank_le_card_of_mul_eq_zero

