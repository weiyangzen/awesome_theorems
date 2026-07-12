import Mathlib.ModelTheory.Satisfiability

namespace Stage1Instances.THM_M_0646

open Cardinal FirstOrder

universe u v w w'

-- Each command below must be rejected. The validation recipe checks for a nonzero Lean exit.

-- Removed hypothesis: the pinned theorem cannot be used without an `Infinite M` instance.
example (L : Language.{u, v}) (M : Type w') [L.Structure M] (κ : Cardinal.{w})
    (h0 : ℵ₀ ≤ κ)
    (hL : Cardinal.lift.{w} L.card ≤ Cardinal.lift.{max u v} κ) :=
  L.exists_elementarilyEquivalent_card_eq M κ h0 hL

-- Changed domain: a natural number is not the target cardinal binder.
#check FirstOrder.Language.exists_elementarilyEquivalent_card_eq
  (κ := (3 : Nat))

-- Changed binder scope: the structure binder cannot precede the carrier it structures.
#check fun (L : Language.{u, v}) [L.Structure M] (M : Type w') => M

-- Boundary mutation: a finite target cardinal cannot satisfy the required infinitude bound.
example : (ℵ₀ : Cardinal.{w}) ≤ 0 := by simp

end Stage1Instances.THM_M_0646
