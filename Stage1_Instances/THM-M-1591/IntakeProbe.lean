import Mathlib.FieldTheory.Finite.Basic
import Mathlib.InformationTheory.Hamming
import Mathlib.RingTheory.Polynomial.Cyclotomic.Roots

/-!
# THM-M-1591 discovery-only intake probe

These checks authenticate pinned finite-field, polynomial/root-of-unity, and Hamming-distance APIs
adjacent to possible BCH-code encodings. They do not define a BCH code, select designed-distance or
decoder parameters, state the BCH bound, or prove THM-M-1591.
-/

#check hammingDist
#check hammingNorm
#check hammingDist_triangle
#check hammingDist_le_card_fintype
#check Polynomial
#check Polynomial.IsRoot
#check IsPrimitiveRoot
#check IsPrimitiveRoot.isRoot_cyclotomic
#check FiniteField.card
#check FiniteField.pow_card
