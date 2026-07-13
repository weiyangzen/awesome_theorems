import Mathlib.Combinatorics.Additive.Corner.Roth
import Mathlib.Combinatorics.HalesJewett
import Mathlib.Data.Nat.PrimeFin

/-!
# THM-M-0945 discovery-only intake probe

These checks authenticate pinned prime-infinitude, length-three additive-progression, Roth, and
finite-color homothetic-copy interfaces. They do not define arbitrary finite progressions, state the
Green-Tao root, or provide a proof body for THM-M-0945.
-/

#check Nat.Prime
#check Nat.exists_infinite_primes
#check Nat.infinite_setOf_prime
#check ThreeAPFree
#check roth_3ap_theorem_nat
#check rothNumberNat_isLittleO_id
#check Combinatorics.Line.exists_mono_in_high_dimension
#check Combinatorics.exists_mono_homothetic_copy
