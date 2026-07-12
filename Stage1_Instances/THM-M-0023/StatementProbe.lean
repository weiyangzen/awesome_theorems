import Mathlib.RingTheory.Ideal.Span

/-!
# THM-M-0023 statement probe

This file checks only the type of the ideal-equality conclusion expected in a
cyclotomic Iwasawa main-conjecture statement. It is not the canonical target:
the available repository record does not fix the source conventions needed to
define the Iwasawa module and the normalized cyclotomic p-adic L-function.
-/

namespace Stage1Instances.THM_M_0023

universe u

/-- The expected conclusion after both arithmetic sides have been constructed
in the same commutative Iwasawa algebra. This definition supplies conclusion-
shape evidence only. -/
def IdealEqualityConclusionShape
    (IwasawaAlgebra : Type u) [CommRing IwasawaAlgebra]
    (classGroupCharacteristicIdeal : Ideal IwasawaAlgebra)
    (normalizedPadicLFunction : IwasawaAlgebra) : Prop :=
  classGroupCharacteristicIdeal = Ideal.span {normalizedPadicLFunction}

end Stage1Instances.THM_M_0023

set_option pp.explicit true in
#print Stage1Instances.THM_M_0023.IdealEqualityConclusionShape
