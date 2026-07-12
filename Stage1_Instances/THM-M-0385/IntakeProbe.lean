import Mathlib.Combinatorics.Additive.DoublingConst
import Mathlib.Data.ZMod.Basic
import Mathlib.Data.Real.Basic

open scoped Pointwise

noncomputable section

local instance : DecidableEq Real := Classical.decEq Real

variable (A : Finset Real)

#check Finset.image₂ (fun x y : Real => x + y) A A
#check Finset.image₂ (fun x y : Real => x * y) A A
#check (Finset.image₂ (fun x y : Real => x + y) A A).card
#check (Finset.image₂ (fun x y : Real => x * y) A A).card

variable {p : Nat} [Fact p.Prime] (B : Finset (ZMod p))

#check B + B
#check B * B
#check (B + B).card
#check (B * B).card
