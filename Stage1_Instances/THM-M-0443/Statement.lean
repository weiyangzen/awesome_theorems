import Mathlib.AlgebraicGeometry.EllipticCurve.Reduction
import Mathlib.NumberTheory.Padics.Complex
import Mathlib.NumberTheory.Padics.PadicIntegers

/-!
# THM-M-0443 statement boundary probe

The repository record says only "Mazur-Tate theorem" and "the p-adic L-function of an elliptic
curve". It does not select an exact proposition. This module therefore checks only pinned object
interfaces shared by the unresolved interpretations. It deliberately declares no canonical
Mazur-Tate target, transport, or mutation fixture.
-/

namespace Stage1Instances.THM_M_0443

#check WeierstrassCurve
#check WeierstrassCurve.IsElliptic
#check WeierstrassCurve.HasGoodReduction
#check WeierstrassCurve.HasMultiplicativeReduction
#check PadicInt
#check PadicComplex

end Stage1Instances.THM_M_0443
