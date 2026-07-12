import Mathlib.RingTheory.Nullstellensatz

/-!
# THM-M-0026 discovery-only intake probe

These checks authenticate pinned multivariable-polynomial, zero-locus, vanishing-ideal, and
Nullstellensatz declarations adjacent to the catalog claim. They do not freeze the canonical target,
perform the later anchor audit, or grant proof credit to `THM-M-0026`.
-/

open Ideal
open MvPolynomial

#check MvPolynomial
#check MvPolynomial.zeroLocus
#check MvPolynomial.vanishingIdeal
#check MvPolynomial.mem_zeroLocus_iff
#check MvPolynomial.mem_vanishingIdeal_iff
#check MvPolynomial.mem_vanishingIdeal_singleton_iff
#check MvPolynomial.eq_vanishingIdeal_singleton_of_isMaximal
#check MvPolynomial.isMaximal_iff_eq_vanishingIdeal_singleton
#check MvPolynomial.vanishingIdeal_zeroLocus_eq_radical
#check MvPolynomial.IsPrime.vanishingIdeal_zeroLocus
