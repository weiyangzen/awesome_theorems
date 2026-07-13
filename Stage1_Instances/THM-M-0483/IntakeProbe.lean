import Mathlib.NumberTheory.LucasLehmer

/-!
# THM-M-0483 discovery-only intake probe

These commands authenticate nearby Mersenne-primality interfaces in the pinned mathlib snapshot.
They do not select an exact source proposition, establish statement identity, or prove the
repository target. In particular, the general Lucas-Lehmer criterion may belong to the separate
`THM-M-0484` target.
-/

#check mersenne
#check Nat.Prime.of_mersenne
#check LucasLehmer.LucasLehmerTest
#check LucasLehmer.lucasLehmerResidue
#check lucas_lehmer_sufficiency
#check lucas_lehmer_necessity

#print axioms Nat.Prime.of_mersenne
#print axioms lucas_lehmer_sufficiency
#print axioms lucas_lehmer_necessity
