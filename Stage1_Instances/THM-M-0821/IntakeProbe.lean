import Mathlib.Combinatorics.SetFamily.LYM

/-!
# THM-M-0821 discovery-only intake probe

These checks authenticate the pinned Sperner upper-bound candidate and the middle-layer APIs needed
to compare it with the source paper. They do not freeze the canonical target, audit the terminal
proof body, supply the source equality classification, or prove THM-M-0821.
-/

#check IsAntichain.sperner
#check Finset.powersetCard
#check Finset.card_powersetCard
#check Finset.slice
#check Set.sized_powersetCard
#check Nat.choose
#check Nat.choose_le_middle
#check Nat.choose_symm
