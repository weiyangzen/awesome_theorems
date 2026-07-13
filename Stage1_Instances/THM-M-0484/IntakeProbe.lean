import Mathlib.NumberTheory.LucasLehmer

/-!
# THM-M-0484 discovery-only intake probe

These checks authenticate the exact-topic Lucas-Lehmer definitions and both correctness directions
in the manifest-pinned mathlib. The final example only checks that the two library directions
compose under the shared lower bound `3 <= p`. It is not the canonical statement-phase declaration,
a source-fidelity certificate, an anchor audit, or accepted proof credit.
-/

#check mersenne
#check LucasLehmer.s
#check LucasLehmer.sZMod
#check LucasLehmer.sMod
#check LucasLehmer.lucasLehmerResidue
#check LucasLehmer.LucasLehmerTest
#check lucas_lehmer_sufficiency
#check lucas_lehmer_necessity

#print axioms lucas_lehmer_sufficiency
#print axioms lucas_lehmer_necessity

example (p : Nat) (hp : 3 <= p) :
    LucasLehmer.LucasLehmerTest p <-> Nat.Prime (mersenne p) := by
  constructor
  · exact lucas_lehmer_sufficiency p (by omega)
  · exact lucas_lehmer_necessity p hp

example : Not (LucasLehmer.LucasLehmerTest 2) := by
  norm_num

example : Nat.Prime (mersenne 2) := by
  decide
