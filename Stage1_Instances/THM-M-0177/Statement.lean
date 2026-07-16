import Mathlib.AlgebraicGeometry.Morphisms.Proper
import Mathlib.AlgebraicGeometry.Morphisms.Smooth

/-!
# THM-M-0177 statement boundary

The intake selects the classical Grothendieck-Riemann-Roch formula for a proper
morphism of smooth quasi-projective schemes. The pinned environment does not
provide the concrete K/G-theory, rational Chow theory, characteristic classes,
or pushforwards needed to type that formula. This module therefore checks only
the available geometric boundary. It deliberately declares no canonical GRR
target, abstract replacement model, transport, or mutation fixture.
-/

open CategoryTheory

namespace Stage1Instances.THM_M_0177

open AlgebraicGeometry

universe u

#check Scheme.{u}
#check @IsProper
#check @Smooth

end Stage1Instances.THM_M_0177
