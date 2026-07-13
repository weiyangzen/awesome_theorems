import Mathlib.Analysis.SpecialFunctions.BinaryEntropy
import Mathlib.Combinatorics.Additive.AP.Three.Defs
import Mathlib.Data.Fintype.BigOperators
import Mathlib.Data.ZMod.Basic

/-!
# THM-M-0959 discovery-only intake probe

These checks authenticate pinned interfaces adjacent to possible Croot-Lev-Pach
statements. They do not select a numbered source result, define the CLP entropy
constant, or prove the polynomial lemma, coset bound, or exponential upper bound.
-/

#check ThreeAPFree
#check ThreeAPFree.prod
#check Fintype.card_pi_const
#check ZMod
#check ZMod.card
#check Real.binEntropy
#check Real.binEntropy_continuous
#check Real.binEntropy_le_log_two
