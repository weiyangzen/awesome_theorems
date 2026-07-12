import Mathlib.Data.Finset.Powerset

/-!
# THM-M-0899 discovery-only intake probe

These checks authenticate adjacent pinned finite-subset and binomial-coefficient APIs. They do not
define a PBD, BIBD, or `t`-design; select design parameters; or state an existence theorem.
-/

#check Finset.powersetCard
#check Finset.mem_powersetCard
#check Finset.card_powersetCard
#check Finset.powersetCard_nonempty
#check Nat.choose
