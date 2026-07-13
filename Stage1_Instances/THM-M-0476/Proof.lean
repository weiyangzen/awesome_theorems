import ObligationTree
import Mathlib.Util.AssertNoSorry
import Mathlib.Util.PrintSorries

/-!
# THM-M-0476 proof execution

This module installs the exact pinned Wilson proof body at the frozen natural-prime target. It also
supplies every leaf in the frozen proof graph and checks the complete factorial-to-units
composition independently. The direct wrapper and expanded composition share upstream bodies and
do not receive duplicate proof credit.
-/

namespace Stage1Instances.THM_M_0476.Proof

open Finset Nat
open scoped Nat
open Stage1Instances.THM_M_0476
open Stage1Instances.THM_M_0476.ObligationTree

/-! Exact pinned bodies for the two audited bridge interfaces. -/

/-- The exact pinned Wilson body at its `Fact`-premise interface (`M0476-L-WILSON`). -/
theorem factWilsonAnchor_mathlib : FactWilsonAnchor := by
  intro p _
  exact ZMod.wilsons_lemma p

/-- The generalized unit-product body at the frozen interface (`M0476-L-UNITS-PRODUCT`). -/
theorem unitProductIdentity_mathlib : UnitProductIdentity := by
  intro p _
  exact FiniteField.prod_univ_units_id_eq_neg_one

/-! Exact bodies for every leaf in the frozen proof graph. -/

/-- The natural interval product is a factorial (`M0476-L-FACTORIAL-INTERVAL`). -/
theorem factorialIntervalIdentity : FactorialIntervalIdentity := by
  intro n
  exact Finset.prod_Ico_id_eq_factorial n

/-- Natural casting commutes with the interval product (`M0476-T-NAT-CAST-PRODUCT`). -/
theorem natIntervalCastIdentity : NatIntervalCastIdentity := by
  intro p n
  exact Finset.prod_natCast (R := ZMod p) (Finset.Ico 1 (n + 1)) id

/-- The prime endpoint normalization (`M0476-N-PRIME-ENDPOINT`). -/
theorem primeEndpointIdentity : PrimeEndpointIdentity :=
  primeEndpointIdentity_from_prime

/-- Unit representatives lie in the nonzero prime interval (`M0476-B-UNIT-VAL-RANGE`). -/
theorem unitRepresentativeInPrimeRange : UnitRepresentativeInPrimeRange :=
  unitRepresentativeInPrimeRange_from_unit

/-- Unit representatives are injective (`M0476-L-UNIT-VAL-INJECTIVE`). -/
theorem unitRepresentativeInjective : UnitRepresentativeInjective :=
  unitRepresentativeInjective_from_val

/-- Every positive representative below the prime lifts to a unit (`M0476-C-RESIDUE-TO-UNIT`). -/
theorem residueRepresentativeSurjectiveAtEndpoint :
    ResidueRepresentativeSurjectiveAtEndpoint :=
  residueRepresentativeSurjectiveAtEndpoint_from_mk0

/-- Unit coercion agrees with the cast of its representative (`M0476-T-REPRESENTATIVE-COE`). -/
theorem representativeCastAgreement : RepresentativeCastAgreement :=
  representativeCastAgreement_from_natCast_val

/-- Inverse-fixed units are exactly one and negative one (`M0476-L-INVERSE-FIXED-POINTS`). -/
theorem inverseFixedPointClassification : InverseFixedPointClassification :=
  inverseFixedPointClassification_from_units

/-! Checked child-to-parent composition along the complete frozen proof graph. -/

/-- Compose the factorial and cast leaves (`M0476-N-FACTORIAL-PRODUCT`). -/
theorem factorialProduct : FactorialProductBridge :=
  factorialProduct_of_identities factorialIntervalIdentity natIntervalCastIdentity

/-- Compose all representative-to-unit leaves (`M0476-C-RESIDUE-UNITS-BIJECTION`). -/
theorem residueUnitsProduct : ResidueUnitsProductBridge :=
  residueUnitsProduct_of_components primeEndpointIdentity unitRepresentativeInPrimeRange
    unitRepresentativeInjective residueRepresentativeSurjectiveAtEndpoint
    representativeCastAgreement

/-- Pair all units except negative one with their inverses (`M0476-C-INVERSE-PAIRING`). -/
theorem unitEraseNegOneProduct : UnitEraseNegOneProduct :=
  unitEraseProduct_of_inversion inverseFixedPointClassification

/-- Insert negative one back into the paired product (`M0476-T-INSERT-NEGONE`). -/
theorem unitProductIdentity_expanded : UnitProductIdentity :=
  unitProductIdentity_of_erase unitEraseNegOneProduct

/-- Coerce the expanded unit product into `ZMod p` (`M0476-T-UNITS-COE-NEGONE`). -/
theorem unitsProductBridge : UnitsProductBridge :=
  unitsProductBridge_of_components unitProductIdentity_expanded

/-- Compose the three mathematical bridges at the exact `Fact` interface (`M0476-T-COMPOSE`). -/
theorem factWilsonAnchor_expanded : FactWilsonAnchor :=
  factWilsonAnchor_of_bridges factorialProduct residueUnitsProduct unitsProductBridge

/-- Transport the expanded `Fact` interface to the canonical target (`M0476-S-FACT-TRANSPORT`). -/
theorem wilsonTheorem_after_factTransport : WilsonTheoremTarget :=
  root_of_factWilsonAnchor factWilsonAnchor_expanded

/-- The exact canonical root through every frozen proof-graph child. -/
theorem wilsonTheorem_via_frozen_composition : WilsonTheoremTarget :=
  root_of_composedTarget wilsonTheorem_after_factTransport

/-- The exact canonical root through the pinned `ZMod.wilsons_lemma` body. -/
theorem wilsonTheorem : WilsonTheoremTarget :=
  root_of_composedTarget (root_of_factWilsonAnchor factWilsonAnchor_mathlib)

assert_no_sorry ZMod.wilsons_lemma
assert_no_sorry FiniteField.prod_univ_units_id_eq_neg_one
assert_no_sorry Finset.prod_Ico_id_eq_factorial
assert_no_sorry Finset.prod_natCast
assert_no_sorry factWilsonAnchor_mathlib
assert_no_sorry unitProductIdentity_mathlib
assert_no_sorry factorialIntervalIdentity
assert_no_sorry natIntervalCastIdentity
assert_no_sorry primeEndpointIdentity
assert_no_sorry unitRepresentativeInPrimeRange
assert_no_sorry unitRepresentativeInjective
assert_no_sorry residueRepresentativeSurjectiveAtEndpoint
assert_no_sorry representativeCastAgreement
assert_no_sorry inverseFixedPointClassification
assert_no_sorry factorialProduct
assert_no_sorry residueUnitsProduct
assert_no_sorry unitEraseNegOneProduct
assert_no_sorry unitProductIdentity_expanded
assert_no_sorry unitsProductBridge
assert_no_sorry factWilsonAnchor_expanded
assert_no_sorry wilsonTheorem_after_factTransport
assert_no_sorry wilsonTheorem_via_frozen_composition
assert_no_sorry wilsonTheorem

#print sorries ZMod.wilsons_lemma
#print sorries FiniteField.prod_univ_units_id_eq_neg_one
#print sorries Finset.prod_Ico_id_eq_factorial
#print sorries Finset.prod_natCast
#print sorries factWilsonAnchor_mathlib
#print sorries unitProductIdentity_mathlib
#print sorries factorialIntervalIdentity
#print sorries natIntervalCastIdentity
#print sorries primeEndpointIdentity
#print sorries unitRepresentativeInPrimeRange
#print sorries unitRepresentativeInjective
#print sorries residueRepresentativeSurjectiveAtEndpoint
#print sorries representativeCastAgreement
#print sorries inverseFixedPointClassification
#print sorries factorialProduct
#print sorries residueUnitsProduct
#print sorries unitEraseNegOneProduct
#print sorries unitProductIdentity_expanded
#print sorries unitsProductBridge
#print sorries factWilsonAnchor_expanded
#print sorries wilsonTheorem_after_factTransport
#print sorries wilsonTheorem_via_frozen_composition
#print sorries wilsonTheorem

#print axioms ZMod.wilsons_lemma
#print axioms FiniteField.prod_univ_units_id_eq_neg_one
#print axioms Finset.prod_Ico_id_eq_factorial
#print axioms Finset.prod_natCast
#print axioms factWilsonAnchor_mathlib
#print axioms unitProductIdentity_mathlib
#print axioms factorialIntervalIdentity
#print axioms natIntervalCastIdentity
#print axioms primeEndpointIdentity
#print axioms unitRepresentativeInPrimeRange
#print axioms unitRepresentativeInjective
#print axioms residueRepresentativeSurjectiveAtEndpoint
#print axioms representativeCastAgreement
#print axioms inverseFixedPointClassification
#print axioms factorialProduct
#print axioms residueUnitsProduct
#print axioms unitEraseNegOneProduct
#print axioms unitProductIdentity_expanded
#print axioms unitsProductBridge
#print axioms factWilsonAnchor_expanded
#print axioms wilsonTheorem_after_factTransport
#print axioms wilsonTheorem_via_frozen_composition
#print axioms wilsonTheorem

end Stage1Instances.THM_M_0476.Proof
