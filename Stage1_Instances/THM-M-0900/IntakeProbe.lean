import Mathlib.Data.Finset.Powerset

/-!
# THM-M-0900 discovery-only intake probe

These checks authenticate adjacent pinned finite-subset and binomial-coefficient APIs. They do not
define a combinatorial design, resolve the catalog identity, or state THM-M-0900.
-/

#check Finset.powersetCard
#check Finset.mem_powersetCard
#check Finset.card_powersetCard
#check Finset.powersetCard_nonempty
#check Nat.choose
