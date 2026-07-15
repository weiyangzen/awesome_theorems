import Mathlib.AlgebraicGeometry.Morphisms.Proper
import Mathlib.AlgebraicGeometry.Morphisms.Smooth

/-!
# THM-M-0115 statement-infrastructure probe

This module checks only the base-field scheme, smoothness, and properness
substrate available in the pinned dependency closure. It deliberately does not
declare a Grothendieck-Riemann-Roch target: the closure has no concrete combined
API for quasi-projective varieties, `K_0`, rational Chow homology, the two
pushforwards, Chern characters, tangent bundles, Todd classes, and cap products.
Abstract stand-ins for those notions would encode a different theorem.
-/

open CategoryTheory
open AlgebraicGeometry

namespace Stage1Instances.THMM0115.StatementProbe

universe u

#check Scheme
#check Scheme.Spec
#check Scheme.Hom.IsOver
#check @IsProper
#check @Smooth

/-- The part of the frozen domain that the pinned native substrate can express.
This boundary omits quasi-projectivity and every GRR-specific object and map, so
it is not the canonical target. -/
def SmoothProperOverFieldBoundary
    (k : Type u) [Field k]
    (X Y : Scheme.{u})
    [X.Over (Scheme.Spec.obj (Opposite.op (.of k)))]
    [Y.Over (Scheme.Spec.obj (Opposite.op (.of k)))]
    (f : X ⟶ Y) [f.IsOver (Scheme.Spec.obj (Opposite.op (.of k)))] : Prop :=
  Smooth (X ↘ Scheme.Spec.obj (Opposite.op (.of k))) ∧
    Smooth (Y ↘ Scheme.Spec.obj (Opposite.op (.of k))) ∧ IsProper f

#check SmoothProperOverFieldBoundary

end Stage1Instances.THMM0115.StatementProbe
