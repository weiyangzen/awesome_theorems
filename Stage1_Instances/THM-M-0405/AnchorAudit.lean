import Mathlib.NumberTheory.LucasLehmer
import Mathlib.NumberTheory.LucasPrimality
import Mathlib.Algebra.LinearRecurrence

/-!
# THM-M-0405 anchor-audit probes

These checks identify nearby declarations in the pinned mathlib revision.  None
has the Lucas/Lehmer primitive-divisor type frozen in `Statement.lean`.
-/

#check LucasLehmer.LucasLehmerTest
#check LucasLehmer.lucasLehmerResidue
#check lucas_lehmer_sufficiency
#check lucas_lehmer_necessity
#check lucas_primality
#check reverse_lucas_primality
#check LinearRecurrence
