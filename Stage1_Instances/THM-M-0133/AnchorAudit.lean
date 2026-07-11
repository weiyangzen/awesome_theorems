import Mathlib.NumberTheory.FLT.Three
import Mathlib.NumberTheory.FLT.Four
import Mathlib.NumberTheory.FLT.Polynomial
import FltRegular.FltRegular

/-!
# THM-M-0133 immutable anchor probes

These probes elaborate the strongest root-relevant declarations in the pinned
Lake closure. None is an unconditional proof of the frozen FLT root.
-/

#check FermatLastTheorem
#check FermatLastTheorem.of_odd_primes
#check fermatLastTheoremThree
#check fermatLastTheoremFour
#check fermatLastTheoremWith'_polynomial
#check flt_regular

#print axioms FermatLastTheorem.of_odd_primes
#print axioms fermatLastTheoremThree
#print axioms fermatLastTheoremFour
#print axioms fermatLastTheoremWith'_polynomial
#print axioms flt_regular
