import Mathlib.AlgebraicGeometry.Morphisms.Proper
import Mathlib.AlgebraicGeometry.Morphisms.Smooth

/-!
Elaboration probe for the THM-M-0177 exact-statement blocker.

This checks only the scheme and morphism-property substrate available in the
pinned environment. It deliberately does not introduce abstract stand-ins for
K-theory, Chow groups, Chern characters, Todd classes, or their pushforwards.
Such stand-ins would elaborate a different theorem rather than GRR.
-/

open CategoryTheory

namespace Stage1Instances.THM_M_0177

open AlgebraicGeometry

universe u

#check Scheme
#check @IsProper
#check @Smooth

/-- The pinned substrate can express the properness and smoothness part of the
intended scope for a scheme morphism. This is not the GRR target. -/
def SchemeMorphismBoundary (X Y : Scheme.{u}) (f : X ⟶ Y) : Prop :=
  IsProper f ∧ Smooth f

#check SchemeMorphismBoundary

end Stage1Instances.THM_M_0177
