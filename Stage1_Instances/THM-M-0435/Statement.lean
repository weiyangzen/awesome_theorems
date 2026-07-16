import Mathlib.Algebra.QuaternionBasis
import Mathlib.AlgebraicGeometry.Morphisms.Proper
import Mathlib.AlgebraicGeometry.Morphisms.Smooth
import Mathlib.NumberTheory.NumberField.Basic

/-!
# THM-M-0435 statement-gate probe

The repository record says only "modular curves over quaternion algebras". It
does not select a base field, quaternion algebra, order or level, model, or one
truth-valued conclusion. This module checks the smallest pinned vocabulary
needed to make that ambiguity concrete. It intentionally declares no canonical
target: doing so before an authoritative source selects those data would invent
or substitute mathematics.
-/

open AlgebraicGeometry

universe u

namespace Stage1Instances.THM_M_0435

#check NumberField
#check QuaternionAlgebra
#check QuaternionAlgebra.basisOneIJK
#check Scheme.{u}
#check IsProper
#check SmoothOfRelativeDimension

end Stage1Instances.THM_M_0435
