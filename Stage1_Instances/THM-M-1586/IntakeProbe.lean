import Mathlib.Data.Fintype.BigOperators
import Mathlib.InformationTheory.Hamming

/-!
# THM-M-1586 discovery-only intake probe

These checks authenticate pinned finite Hamming-space and cardinality interfaces adjacent to a
possible future Hamming-bound encoding. They do not define a code, select a binary, q-ary, linear,
or asymptotic catalog proposition, or prove THM-M-1586.
-/

#check hammingDist
#check hammingDist_comm
#check hammingDist_triangle
#check hammingDist_le_card_fintype
#check Hamming
#synth Fintype (Hamming (fun _ : Fin 3 => Fin 2))
#check Hamming.dist_eq_hammingDist
#check Fintype.card_fun
#check Nat.choose
