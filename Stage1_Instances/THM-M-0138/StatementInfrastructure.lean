import Mathlib.Algebra.Lie.UniversalEnveloping
import Mathlib.AlgebraicGeometry.Modules.Sheaf

/-!
Kernel-checked infrastructure probe for the THM-M-0138 statement gate.

The pinned library does not expose the flag variety of a semisimple complex Lie algebra, its
twisted differential-operator sheaf, or the required central-character module block. Accordingly
this file does not declare a canonical Beilinson-Bernstein target. It checks only the two concrete
library surfaces that are adjacent to such a future target.
-/

namespace Stage1Instances.THM_M_0138.StatementInfrastructure

universe u v

/-- The pinned universal-enveloping-algebra constructor, without choosing a Lie algebra. -/
abbrev EnvelopingAlgebraCarrier (k : Type u) (g : Type v)
    [CommRing k] [LieRing g] [LieAlgebra k g] : Type (max u v) :=
  UniversalEnvelopingAlgebra k g

/-- Ordinary module sheaves on a pinned mathlib scheme; these are not twisted D-modules. -/
abbrev OrdinaryModuleSheaves (X : AlgebraicGeometry.Scheme.{u}) : Type (u + 1) :=
  X.Modules

#check UniversalEnvelopingAlgebra
#check AlgebraicGeometry.Scheme.Modules
#check CategoryTheory.Functor.IsEquivalence

end Stage1Instances.THM_M_0138.StatementInfrastructure
