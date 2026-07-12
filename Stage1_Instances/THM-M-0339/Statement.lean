import Mathlib.Analysis.InnerProductSpace.PiL2

open scoped BigOperators

namespace Stage1.THM_M_0339

/-- The exact finite-dimensional partition statement of MSS, Corollary 1.5.

`color i = j` is the labeled part `S_j`.  Thus the fibers of `color` are automatically a
partition of `Fin m`, including the empty parts permitted by the source statement.
-/
def MSSPartitionStatement : Prop :=
  ∀ (d m r : ℕ) (δ : ℝ),
    0 < r →
    0 ≤ δ →
    ∀ u : Fin m → EuclideanSpace ℂ (Fin d),
      (∑ i, InnerProductSpace.rankOne ℂ (u i) (u i)) =
          ContinuousLinearMap.id ℂ (EuclideanSpace ℂ (Fin d)) →
      (∀ i, ‖u i‖ ^ 2 ≤ δ) →
      ∃ color : Fin m → Fin r,
        ∀ j : Fin r,
          ‖∑ i with color i = j, InnerProductSpace.rankOne ℂ (u i) (u i)‖ ≤
            (1 / Real.sqrt r + Real.sqrt δ) ^ 2

#print MSSPartitionStatement

end Stage1.THM_M_0339
