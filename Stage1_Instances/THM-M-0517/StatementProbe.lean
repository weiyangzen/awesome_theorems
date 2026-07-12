import Mathlib.RingTheory.Ideal.Span

/-!
# THM-M-0517 statement probe

This file checks only the type of the ideal-equality conclusion expected in a
cyclotomic Iwasawa main-conjecture statement. It is deliberately not the
canonical target: the intake does not yet identify enough source conventions to
define the two sides without substituting abstract parameters for the actual
Iwasawa module and p-adic L-function.
-/

namespace Stage1Instances.THM_M_0517

universe u

/-- The expected conclusion shape after both sides have been constructed in
the same commutative Iwasawa algebra. This is an elaboration probe, not the
Iwasawa main conjecture. -/
def IdealEqualityConclusionShape
    (IwasawaAlgebra : Type u) [CommRing IwasawaAlgebra]
    (classGroupCharacteristicIdeal : Ideal IwasawaAlgebra)
    (normalizedPadicLFunction : IwasawaAlgebra) : Prop :=
  classGroupCharacteristicIdeal = Ideal.span {normalizedPadicLFunction}

end Stage1Instances.THM_M_0517

set_option pp.explicit true in
#print Stage1Instances.THM_M_0517.IdealEqualityConclusionShape
