import Mathlib.Combinatorics.Additive.Energy
import Mathlib.Data.Nat.Log
import Mathlib.Data.Real.Basic

/-!
# THM-M-0953 discovery-only intake probe

These checks authenticate pinned finite real sumset, product-set, and multiplicative-energy
interfaces adjacent to a possible future Solymosi sum-product encoding. They do not select
Theorem 2.1, Corollary 2.2, or another source result, and they prove no part of THM-M-0953.
-/

open scoped Combinatorics.Additive Pointwise

noncomputable section

local instance : DecidableEq Real := Classical.decEq Real

variable (A : Finset Real)

#check A + A
#check A * A
#check (A + A).card
#check (A * A).card
#check Finset.mulEnergy A A
#check Finset.mulEnergy_eq_sum_sq' A A
#check Finset.le_card_mul_mul_mulEnergy A A
#check Nat.clog 2 A.card

-- Candidate shape only: its source selection and boundary repair are deliberately uncredited.
#check fun A : Finset Real =>
  (∀ a ∈ A, 0 < a) →
    1 < A.card →
      A.card ^ 4 ≤ 4 * Nat.clog 2 A.card * (A * A).card * (A + A).card ^ 2
